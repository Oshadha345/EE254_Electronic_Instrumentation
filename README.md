# EE254 Electronic Instrumentation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Oshadha345/EE254_Electronic_Instrumentation/graphs/commit-activity)
[![made-with-Multisim](https://img.shields.io/badge/Made%20with-Multisim-1f425f.svg)](https://www.ni.com/en-us/shop/electronic-test-instrumentation/application-software-for-electronic-test-and-instrumentation-category/what-is-multisim.html)
[![made-with-Octave](https://img.shields.io/badge/Made%20with-Octave-0790C0.svg)](https://www.gnu.org/software/octave/index)

## 📊 Course Repository for Electronic Instrumentation

This repository contains all materials related to the EE254 Electronic Instrumentation course, including laboratory experiments, simulations, projects, and in-depth studies of operational amplifiers.

## 📑 Table of Contents

- [EE254 Electronic Instrumentation](#ee254-electronic-instrumentation)
  - [📊 Course Repository for Electronic Instrumentation](#-course-repository-for-electronic-instrumentation)
  - [📑 Table of Contents](#-table-of-contents)
  - [🔍 Overview](#-overview)
  - [📂 Repository Structure](#-repository-structure)
  - [🛠️ Tools and Technologies](#️-tools-and-technologies)
  - [⚙️ Setup Instructions](#️-setup-instructions)
    - [Multisim Setup](#multisim-setup)
    - [Octave Setup](#octave-setup)
  - [Course Labs](#course-labs)
  - [🧪 Self-Study Labs](#-self-study-labs)
  - [💻 Simulations](#-simulations)
    - [Multisim Simulations](#multisim-simulations)
    - [Octave Simulations](#octave-simulations)
  - [🚀 Projects](#-projects)
  - [🔌 OP-Amp Studies](#-op-amp-studies)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)

## 🔍 Overview

This repository serves as a comprehensive resource for the EE254 Electronic Instrumentation course. It includes hands-on laboratory exercises, circuit simulations, theoretical analyses, and practical projects that demonstrate the principles and applications of electronic instrumentation systems.

## 📂 Repository Structure

```bash
EE254_Electronic_Instrumentation/
├── labs/                   # Laboratory experiments and reports
├── simulations/            # Simulation files
│   ├── multisim/           # Multisim circuit simulations
│   └── octave/             # Octave/MATLAB analysis scripts
├── projects/               # Course projects
├── op-amp-study/           # In-depth operational amplifier studies
├── docs/                   # Additional documentation and notes
└── README.md               # This file
```


## 🛠️ Tools and Technologies

- **Multisim**: For circuit design and simulation
- **Octave/MATLAB**: For signal processing and data analysis
- **Oscilloscopes**: Tektronix/Keysight for laboratory measurements
- **Signal Generators**: For input signal generation
- **Spectrum Analyzers**: For frequency domain analysis
- **Digital Multimeters**: For electrical measurements

## ⚙️ Setup Instructions

### Multisim Setup
1. Download and install [NI Multisim](https://www.ni.com/en-us/support/downloads/software-products/download.multisim.html)
2. Open `.ms14` files from the `simulations/multisim` directory

### Octave Setup
1. Download and install [GNU Octave](https://www.gnu.org/software/octave/download)
2. Run `.m` files from the `simulations/octave` directory

## Course Labs
This course includes a series of structured laboratory experiments designed to reinforce theoretical concepts through practical application. Each lab is documented with objectives, procedures, and analysis questions to guide students through the learning process.

- Lab 01 : Characteristics of an Op-Amp
- Lab 02 : Application of Op-Amps I  -> Inverting Amplifier, Non-Inverting Amplifier, Differential Amplifier
- Lab 03 : Application of Op-Amps II -> Summing Amplifier, Integrator, Differentiator
  
## 🧪 Self-Study Labs

These self-study labs are designed to be completed using Multisim for simulation and Octave for analysis. They build upon the foundational op-amp concepts and explore advanced topics in signal conditioning, data conversion, and acquisition systems.

- **Lab 04: Active Filters**
    - Design and simulate active filters (Low-pass, High-pass, Band-pass) using op-amps. Analyze their frequency response in Multisim and verify with Octave.

- **Lab 05: Instrumentation Amplifiers**
    - Construct a classic three-op-amp instrumentation amplifier. Investigate its high Common-Mode Rejection Ratio (CMRR) and its application in amplifying small differential signals from sensors.

- **Lab 06: Oscillators and Waveform Generators**
    - Design and simulate various oscillator circuits, such as Wien bridge (sine wave) and astable multivibrator (square/triangle wave) circuits using op-amps.

- **Lab 07: Sensor Signal Conditioning**
    - Interface a simulated sensor (e.g., a temperature sensor or a strain gauge bridge) with a signal conditioning circuit. This includes amplification, filtering, and level shifting to prepare the signal for data conversion.

- **Lab 08: Analog-to-Digital Conversion (ADC)**
    - Simulate a fundamental ADC architecture, such as a flash ADC or a successive-approximation ADC, to understand the process of digitizing an analog signal.

- **Lab 09: Digital-to-Analog Conversion (DAC)**
    - Design and simulate an R-2R ladder DAC to convert digital words back into analog voltage levels. Analyze its resolution and linearity.

- **Lab 10: Basic Data Acquisition (DAQ) System**
    - Integrate the sensor, signal conditioning, and ADC components into a complete, albeit simplified, data acquisition system. Use Octave to post-process the simulated digital output.

Each lab includes objectives, theoretical background, experimental procedures, and analysis questions.

## 💻 Simulations

### Multisim Simulations
Circuit simulations for validating designs before physical implementation.

### Octave Simulations
Signal processing algorithms and data analysis scripts for:
- Filter response analysis
- Noise characterization
- Sensor data processing
- Statistical analysis of measurements

## 🚀 Projects

The `projects` directory contains comprehensive instrumentation projects that integrate multiple concepts from the course. Each project includes design specifications, schematic diagrams, simulation results, and performance analyses.

## 🔌 OP-Amp Studies

The `op-amp-study` directory contains an in-depth exploration of operational amplifiers:
- Basic configurations (inverting, non-inverting, differential)
- Frequency response analysis
- Common-mode rejection ratio (CMRR) measurements
- Slew rate limitations
- Noise characteristics
- Specialized applications in instrumentation

## 🤝 Contributing

Contributions to this repository are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
    <hr>
    <p>
        <b>Oshadha Samarakoon (E/21/345)</b>
        <br>
        <a href="mailto:e21345@eng.pdn.ac.lk">e21345@eng.pdn.ac.lk</a>
    </p>
    <p>
        <b>EE254 Electronic Instrumentation</b>
        <br>
        Department of Electrical and Electronic Engineering
        <br>
        University of Peradeniya
    </p>
</div>