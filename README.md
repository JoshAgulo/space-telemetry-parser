# Space Mission Telemetry Parser

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A professional command-line tool for parsing and analyzing spacecraft mission telemetry data. This project demonstrates industry best practices including modular Python code, Docker containerization, and comprehensive error handling.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Locally with Python](#running-locally-with-python)
  - [Running with Docker](#running-with-docker)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project parses XML data containing information about active space missions, including:

- **Mission metadata**: Launch dates, destinations, agencies
- **Scientific instruments**: Names, types, power consumption, operational status
- **Telemetry data**: Temperature readings, radiation levels, position data
- **Communication metrics**: Signal strength, data rates, light-time delays

The parser extracts this data, displays a formatted report, and optionally exports it to JSON format for further analysis.

---

## Features

- **XML Parsing**: Robust parsing with comprehensive error handling
- **Command-Line Interface**: Professional CLI using `argparse`
- **Modular Design**: Clean, reusable functions following best practices
- **JSON Export**: Convert XML data to JSON with a single flag
- **Docker Support**: Fully containerized for consistent cross-platform execution
- **Type Hints**: Modern Python with type annotations for better code clarity
- **Documentation**: Well-commented code with docstrings

---

## Prerequisites

### For Local Python Execution:
- **Python 3.9 or higher** ([Download](https://www.python.org/downloads/))
  
  Verify installation:
  ```bash
  python --version
  ```

### For Docker Execution:
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
  
  Verify installation:
  ```bash
  docker --version
  ```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JoshAgulo/space-telemetry-parser.git
cd space-telemetry-parser
```

### 2. (Optional) Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: This project uses only Python standard library modules, so no external packages are required.*

---

## Usage

### Running Locally with Python

#### Basic Usage

Parse the sample mission data:

```bash
python parse_data.py data/missions.xml
```

#### Export to JSON

Parse and export data to JSON:

```bash
python parse_data.py data/missions.xml --export output.json
```

#### Using Your Own Data

```bash
python parse_data.py /path/to/your/data.xml
```

#### Help and Version

```bash
# Display help
python parse_data.py --help

# Display version
python parse_data.py --version
```

---

### Running with Docker

Docker containers provide an isolated, reproducible environment for running applications.

#### 1. Build the Docker Image

Build the container image (only needed once, or after code changes):

```bash
docker build -t space-telemetry-parser .
```

**What this does**: Creates a self-contained package with Python and your script.

#### 2. Run with Volume Mounts

**What is a Volume Mount?**

A volume mount connects a folder on your computer to a folder inside the Docker container. This lets the containerized application access your local files.

**Syntax**:
```
-v /path/on/your/computer:/path/in/container
```

**Example - Parse the sample data**:

```bash
# Windows (PowerShell)
docker run --rm -v ${PWD}/data:/app/data space-telemetry-parser

# macOS/Linux
docker run --rm -v $(pwd)/data:/app/data space-telemetry-parser
```

**What this does**:
- `--rm`: Automatically remove the container after it finishes
- `-v $(pwd)/data:/app/data`: Mounts your local `data` folder into the container
- The script reads from `/app/data/missions.xml` inside the container

**Example - Export JSON to your local machine**:

```bash
# Windows (PowerShell)
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}:/app/output space-telemetry-parser /app/data/missions.xml --export /app/output/results.json

# macOS/Linux
docker run --rm -v $(pwd)/data:/app/data -v $(pwd):/app/output space-telemetry-parser /app/data/missions.xml --export /app/output/results.json
```

**What this does**:
- Mounts `data` folder for reading XML
- Mounts current directory for writing JSON output
- The exported `results.json` appears in your local folder

---

## Project Structure

```
space-telemetry-parser/
├── data/
│   └── missions.xml          # Sample XML dataset (5 space missions)
├── parse_data.py             # Main Python script
├── Dockerfile                # Docker container configuration
├── requirements.txt          # Python dependencies (empty - uses stdlib)
├── .gitignore                # Files to exclude from Git
├── .dockerignore             # Files to exclude from Docker builds
└── README.md                 # This file
```

---

## Technical Details

### Architecture

The application follows a **modular architecture** with clear separation of concerns:

1. **Parsing Layer** (`parse_xml_file`): Handles file I/O and XML parsing with error handling
2. **Data Extraction Layer** (`extract_mission_data`): Transforms XML into structured Python dictionaries
3. **Presentation Layer** (`display_mission_summary`): Formats and displays data to the console
4. **Export Layer** (`export_to_json`): Converts data to JSON format

### Key Technologies

- **Python 3.11**: Modern Python with type hints and pathlib
- **xml.etree.ElementTree**: Standard library XML parsing
- **argparse**: Professional command-line interface
- **Docker**: Container platform for reproducible deployments

### Design Patterns

- **Separation of Concerns**: Each function has a single, well-defined responsibility
- **Error Handling**: Try-except blocks with informative error messages
- **Type Annotations**: Modern Python style with type hints for clarity
- **Documentation**: Comprehensive docstrings following Google style

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Josh Agulo**
- GitHub: [@JoshAgulo](https://github.com/JoshAgulo)
- Email: agulo.joshclarence@gmail.com

---

## Acknowledgments

- Mission data inspired by real NASA, ESA, and CSA missions
- Built as a portfolio demonstration project
- Showcases professional Python development practices

---

