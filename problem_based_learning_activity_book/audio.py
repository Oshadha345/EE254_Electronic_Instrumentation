"""
realtime_audio_vis.py

Real-time audio playback + oscilloscope + spectrum using sounddevice + pyqtgraph.

Usage:
    python realtime_audio_vis.py
"""

import sys
import threading
import numpy as np
import sounddevice as sd
from scipy.signal import get_window
from scipy.fft import rfft, rfftfreq
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import soundfile as sf  # for robust audio file reading

AUDIO_FILE = "log sweep.wav"   # <- change to your file

# Playback / analysis parameters
BLOCKSIZE = 1024            # frames per callback (smaller -> lower latency)
PLOT_HOP = 512              # how many samples to advance per UI update (controls update rate)
FFT_SIZE = 4096             # window size for FFT (power of two recommended)
WINDOW_TYPE = "hann"        # window for FFT

# UI update interval (ms). We will compute based on PLOT_HOP and sample rate below
# but also cap to a reasonable minimum/maximum later.

class AudioPlayerRealtime(QtWidgets.QMainWindow):
    def __init__(self, audio_file):
        super().__init__()
        self.setWindowTitle("Realtime Audio: Oscilloscope + Spectrum")
        self.audio_file = audio_file

        # load audio (soundfile handles many sample types)
        data, self.fs = sf.read(self.audio_file, always_2d=True)
        data = data.astype(np.float32)
        # use first channel for display/playback for simplicity (mono). Keep dtype float32
        self.audio = data[:, 0].astype(np.float32)
        self.total_frames = len(self.audio)

        # position shared between audio callback and UI thread
        self.pos = 0
        self.pos_lock = threading.Lock()
        self.stream = None
        self.playing = False

        # window for FFT
        self.fft_size = FFT_SIZE
        self.win = get_window(WINDOW_TYPE, self.fft_size, fftbins=True)

        # build UI
        self._build_ui()

        # timer used to update plots
        # compute update interval from hop size
        update_seconds = PLOT_HOP / self.fs
        update_ms = int(max(10, min(200, update_seconds * 1000)))  # clamp between 10ms and 200ms
        self.timer = QtCore.QTimer()
        self.timer.setInterval(update_ms)
        self.timer.timeout.connect(self.update_plots)

        # start playback
        self.start_audio()

    def _build_ui(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        w.setLayout(layout)
        self.setCentralWidget(w)

        # PyQtGraph plot widgets
        pg.setConfigOptions(antialias=True)
        p1 = pg.PlotWidget(title="Oscilloscope (time domain)")
        p1.setLabel('bottom', "Time", units='s')
        p1.setLabel('left', "Amplitude")
        p1.showGrid(x=True, y=True)
        self.scope_plot = p1.plot(pen='y')
        layout.addWidget(p1)

        p2 = pg.PlotWidget(title="Spectrum (magnitude)")
        p2.setLabel('bottom', "Frequency", units='Hz')
        p2.setLabel('left', "Magnitude")
        p2.showGrid(x=True, y=True)
        self.spectrum_plot = p2.plot(pen='c')
        layout.addWidget(p2)

        # status bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # keyboard shortcut to stop (Esc)
        quit_shortcut = QtWidgets.QShortcut(QtCore.Qt.Key_Escape, self)
        quit_shortcut.activated.connect(self.close)

        # close event will stop stream
    def start_audio(self):
        """Open sounddevice OutputStream with callback and start timer."""
        def callback(outdata, frames, time, status):
            if status.output_underflow:
                # underflow occurred; fill zeros to keep timing
                outdata.fill(0)
                return
            # copy frames from the audio buffer into outdata
            with self.pos_lock:
                start = self.pos
                end = start + frames
                if end <= self.total_frames:
                    outdata[:] = self.audio[start:end, np.newaxis]
                    self.pos = end
                else:
                    # end of audio -> fill remaining then zeros
                    n_available = max(0, self.total_frames - start)
                    if n_available > 0:
                        outdata[:n_available, 0] = self.audio[start:start+n_available]
                    if n_available < frames:
                        outdata[n_available:] = 0
                    self.pos = self.total_frames  # mark finished

        try:
            self.stream = sd.OutputStream(
                samplerate=self.fs,
                channels=1,
                blocksize=BLOCKSIZE,
                dtype='float32',  # use float32; widely supported by Windows audio drivers
                callback=callback,
                finished_callback=self.on_stream_finished
            )
            self.stream.start()
            self.playing = True
            self.timer.start()
            self.status.showMessage(f"Playing {self.audio_file} — press Esc or close window to stop")
        except Exception as e:
            self.status.showMessage(f"ERROR starting audio: {e}")
            raise

    def on_stream_finished(self):
        # called by sounddevice when stream finishes
        self.playing = False
        QtCore.QTimer.singleShot(0, self.close)

    def update_plots(self):
        """Called by QTimer in the main GUI thread to update scope and spectrum."""
        with self.pos_lock:
            # choose analysis center so we don't step backward if audio is still buffering
            cur_pos = self.pos

        if cur_pos <= 0:
            return

        # Build scope window: show last N samples (use fft_size or some seconds)
        scope_len = min(self.fft_size, cur_pos)
        start = max(0, cur_pos - scope_len)
        scope_segment = self.audio[start: start + scope_len]

        t = np.arange(len(scope_segment)) / self.fs
        # update scope plot: show normalized amplitude
        self.scope_plot.setData(t, scope_segment)

        # For spectrum, take the last fft_size samples (zero-pad if not enough)
        if len(scope_segment) < self.fft_size:
            buffer = np.zeros(self.fft_size, dtype=np.float64)
            buffer[-len(scope_segment):] = scope_segment
        else:
            buffer = scope_segment[-self.fft_size:].copy()

        # apply window and compute rfft
        buffer *= self.win
        Y = rfft(buffer)
        mag = np.abs(Y) / (self.fft_size/2)  # scale factor for single-sided amplitude approx
        freqs = rfftfreq(self.fft_size, d=1.0/self.fs)

        self.spectrum_plot.setData(freqs, mag)

        # stop if we've reached the end
        if cur_pos >= self.total_frames:
            self.timer.stop()
            # let sounddevice call finished callback; schedule close soon
            # but close after a short delay so user sees final frame
            QtCore.QTimer.singleShot(300, self.close)

    def closeEvent(self, event):
        """Stop audio stream cleanly on window close."""
        if self.timer.isActive():
            self.timer.stop()
        if self.stream is not None and self.stream.active:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    player = AudioPlayerRealtime(AUDIO_FILE)
    player.resize(900, 600)
    player.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()