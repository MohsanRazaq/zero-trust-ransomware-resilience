![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-v1.0-success)
![Security](https://img.shields.io/badge/Focus-Ransomware%20Resilience-red)

# Mini Zero Trust Ransomware Resilience System

## Overview

A lightweight ransomware resilience prototype built in Python using behavioral monitoring, suspicious extension detection, automated containment, backup recovery, and incident reporting.

The system monitors protected directories in real time, detects ransomware-like behavior patterns, automatically locks protected assets during suspicious activity, and supports backup restoration for recovery testing.

This project was developed as an educational cybersecurity engineering project focused on defensive security architecture and ransomware resilience concepts.

## Features

- Real-time filesystem monitoring using Watchdog
- Behavioral ransomware activity detection
- Suspicious extension detection (.locked, .encrypted, etc.)
- Automated folder lockdown and containment
- Versioned backup system
- Backup restoration workflow
- Threat report generation
- Modular layered architecture
- Attack simulation testing framework
- Persistent activity logging

## Architecture

```text
[Filesystem Event]
        ↓
[Monitor Layer]
        ↓
[Detection Engine]
        ↓
[Containment Engine]
        ↓
[Backup & Recovery]
        ↓
[Threat Reporting]
```
The system follows a layered defensive workflow architecture. Filesystem events are collected through real-time monitoring, analyzed by behavioral and extension-based detection logic, and responded to through automated containment and recovery mechanisms. Threat reports and persistent logs are generated to support incident tracking and forensic visibility.

## Project Structure

```text
zero-trust-ransomware-resilience/
│
├── src/
│   ├── main.py
│   ├── monitor.py
│   ├── detector.py
│   ├── response.py
│   ├── backup_manager.py
│   ├── recovery.py
│   ├── reporter.py
│   └── logger.py
│
├── tests/
│   └── attack_simulator.py
│
├── protected/
├── backup/
├── logs/
│
├── README.md
├── requirements.txt
└── .gitignore
```
- `main.py` initializes the monitoring engine and coordinates system execution.
- `monitor.py` handles filesystem event monitoring.
- `detector.py` contains behavioral and extension-based threat detection logic.
- `response.py` manages containment and lockdown operations.
- `backup_manager.py` handles backup generation and versioning.
- `recovery.py` restores protected files after containment events.
- `reporter.py` generates incident and threat reports.
- `logger.py` provides centralized logging functionality.
- `attack_simulator.py` simulates ransomware-like attacks for testing purposes.
## Installation

### 1. Clone Repository

```bash
git clone https://github.com/MohsanRazaq/zero-trust-ransomware-resilience
cd zero-trust-ransomware-resilience
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
## Usage

### Start Monitoring System

```bash
python3 src/main.py
```

The monitoring engine will observe the `protected/` directory in real time and respond to suspicious ransomware-like behavior.

### Stop Monitoring & Recover Files

Press:

```text
CTRL + C
```

Then enter:

```text
mohsan
```

to unlock protected files and restore backups.

## Attack Simulation

The project includes a dedicated ransomware attack simulation script for testing defensive workflows.

### Run Attack Simulator

```bash
python3 tests/attack_simulator.py
```

### Available Simulations

#### 1. Mass Modification Attack

Simulates ransomware-like rapid file modifications to trigger behavioral detection and automated containment.

#### 2. Suspicious Extension Attack

Simulates ransomware-style file renaming using suspicious extensions such as:

```text
.locked
.encrypted
.crypt
```

This triggers extension-based threat detection, incident reporting, and automated folder lockdown.

## Threat Reporting

When suspicious ransomware-like activity is detected, the system automatically generates structured threat reports inside:

```text
logs/threat_report.log
```

### Example Report

```text
==================================================
Incident Timestamp : 2026-05-16 18:21:21
Attack Type        : Suspicious Extension Detection
Affected Path      : protected/victim.txt.locked
Response Action    : Folder Lockdown
==================================================
```

Threat reports provide:
- incident visibility
- attack traceability
- forensic logging
- containment tracking
## Recovery Workflow

When suspicious ransomware-like activity is detected, the system automatically switches the protected directory into a secure read-only state to prevent further file modification attempts.

The recovery workflow includes:

- Unlocking protected assets
- Restoring versioned backups
- Preserving incident logs
- Recovering protected files after containment

### Recovery Process

1. Stop monitoring using:

```text
CTRL + C
```

2. Enter recovery key:

```text
mohsan
```

3. The system will:
   - unlock the protected directory
   - restore backup files
   - resume normal file access

This workflow simulates a simplified ransomware containment and recovery lifecycle.

## Screenshots

### Monitoring Engine

[Monitoring](screenshots/monitoring.png)

### Behavioral Detection & Containment

[Behavior Detection](screenshots/behavior_detection.png)

### Suspicious Extension Detection

[Extension Detection](screenshots/extension_detection.png)

### Threat Reporting

[Threat Report](screenshots/threat_report.png)

### Recovery Workflow

[Recovery](screenshots/recovery.png)


## Future Improvements

When suspicious ransomware-like activity is detected, the system automatically switches the protected directory into a secure read-only state to prevent further file modification attempts.

The recovery workflow includes:

- Unlocking protected assets
- Restoring versioned backups
- Preserving incident logs
- Recovering protected files after containment

### Recovery Process

1. Stop monitoring using:

```text
CTRL + C
```

2. Enter recovery key:

```text
mohsan
```

3. The system will:
   - unlock the protected directory
   - restore backup files
   - resume normal file access

This workflow simulates a simplified ransomware containment and recovery lifecycle.
## Disclaimer

This project was developed strictly for educational and defensive cybersecurity purposes.

The ransomware simulation components are designed only to demonstrate behavioral detection, containment, recovery, and resilience concepts within controlled testing environments.

Do not use this project against systems, files, or environments without proper authorization.