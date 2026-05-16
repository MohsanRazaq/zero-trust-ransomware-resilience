![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-v1.0-success)
![Security](https://img.shields.io/badge/Focus-Ransomware%20Resilience-red)

# Ransomware Resilience Detection System

## Overview

A lightweight ransomware resilience prototype built in Python using behavioral monitoring,
suspicious extension detection, automated containment, backup recovery, and incident reporting.

The system monitors protected directories in real time, detects ransomware-like behavior
patterns, automatically locks protected assets during suspicious activity, and supports
backup restoration for recovery testing.

This project was developed as an educational cybersecurity engineering project focused on
defensive security architecture and ransomware resilience concepts.

> **Note on "Zero Trust":** This prototype implements the *least-privilege* pillar of Zero
> Trust by setting read-only permissions (`chmod 0o444`) on protected files during lockdown.
> Full Zero Trust architecture additionally requires identity-based access control, network
> micro-segmentation, and continuous authentication — those are listed under
> [Future Improvements](#future-improvements) below.

---

## Features

- Real-time filesystem monitoring using Watchdog
- Behavioral ransomware activity detection (sliding-window mass-modification)
- Suspicious extension detection (`.locked`, `.encrypted`, `.crypt`, `.enc`)
- Automated folder lockdown and containment
- Versioned backup system with automatic pruning (max 3 versions per file)
- Read-only backup protection (backups are `chmod 0o444` after write)
- Backup restoration workflow with path-traversal protection
- Threat report generation
- Modular layered architecture
- Attack simulation testing framework
- Persistent activity logging
- Environment-variable-based recovery key (no hardcoded credentials)

---

## Architecture

```text
[Filesystem Event]
        ↓
[Monitor Layer]        monitor.py
        ↓
[Detection Engine]     detector.py
        ↓
[Containment Engine]   response.py
        ↓
[Backup & Recovery]    backup_manager.py  /  recovery.py
        ↓
[Threat Reporting]     reporter.py  /  logger.py
```

The system follows a layered defensive workflow architecture. Filesystem events are collected
through real-time monitoring, analyzed by behavioral and extension-based detection logic, and
responded to through automated containment and recovery mechanisms. Threat reports and
persistent logs are generated to support incident tracking and forensic visibility.

---

## Project Structure

```text
zero-trust-ransomware-resilience/
│
├── src/
│   ├── main.py            # Entry point; coordinates monitoring and recovery
│   ├── constants.py       # Single source of truth for all config values
│   ├── monitor.py         # Filesystem event monitoring (Watchdog)
│   ├── detector.py        # Behavioral and extension-based threat detection
│   ├── response.py        # Containment and lockdown operations
│   ├── backup_manager.py  # Versioned backup creation and pruning
│   ├── recovery.py        # File restoration after containment
│   ├── reporter.py        # Structured threat report generation
│   └── logger.py          # Centralized activity logging
│
├── tests/
│   └── attack_simulator.py
│
├── protected/             # Directory being monitored (gitignored)
├── backup/                # Versioned backups (gitignored)
├── logs/                  # Activity and threat logs (gitignored)
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MohsanRazaq/zero-trust-ransomware-resilience
cd zero-trust-ransomware-resilience
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your recovery key

The recovery key is **not** stored in the source code. Set it as an environment variable
before running the system:

```bash
export RECOVERY_KEY="your-strong-secret-here"
```

> Never commit this value. Add `.env` to `.gitignore` if you store it in a file.

---

## Usage

### Start the monitoring system

```bash
python3 src/main.py
```

The monitoring engine will observe the `protected/` directory in real time and respond to
suspicious ransomware-like behavior.

### Stop monitoring and recover files

1. Press `Ctrl + C`
2. Enter your `RECOVERY_KEY` when prompted (3 attempts allowed)
3. The system will unlock the protected directory and restore backups automatically

---

## Attack Simulation

The project includes a dedicated simulation script for testing defensive workflows.

```bash
python3 tests/attack_simulator.py
```

### Available simulations

**1. Mass Modification Attack**
Simulates ransomware-like rapid file modifications to trigger behavioral detection
and automated containment (threshold: 5 modifications in 10 seconds).

**2. Suspicious Extension Attack**
Simulates ransomware-style file renaming using extensions such as `.locked`,
`.encrypted`, `.crypt`. Triggers extension-based detection, threat reporting,
and automated folder lockdown.

---

## Threat Reporting

When suspicious activity is detected, a structured report is appended to:

```text
logs/threat_report.log
```

Example report:

```text
==================================================
Incident Timestamp : 2026-05-16 18:21:21
Attack Type        : Suspicious Extension Detection
Affected Path      : protected/victim.txt.locked
Response Action    : Folder Lockdown
==================================================
```

---

## Recovery Workflow

When a threat is detected, the system sets the protected directory to read-only (`0o555`)
and individual files to `0o444` to prevent further modification.

Recovery steps:

1. Stop monitoring: `Ctrl + C`
2. Enter recovery key at the prompt
3. The system will:
   - unlock the protected directory (`0o755` / `0o644`)
   - restore the latest backup of each file
   - preserve all incident logs

---

## Security Design Decisions

| Decision | Reason |
|---|---|
| Recovery key stored as env var | Prevents credentials appearing in source code or git history |
| Key compared with `hmac.compare_digest()` | Prevents timing-based brute-force attacks |
| 3-attempt lockout on recovery | Slows down local brute-force attempts |
| Backups set `chmod 0o444` after write | Prevents ransomware or accidents from overwriting safety copies |
| Max 3 backup versions per file | Caps disk usage; stops disk-fill attacks before containment triggers |
| `os.path.basename()` on restore paths | Prevents path-traversal (e.g. `../../etc/passwd` filenames) |
| `threading.Lock()` around deque writes | Prevents race conditions between the Watchdog thread and detection logic |
| Single `constants.py` for all config | Eliminates duplicate `SUSPICIOUS_EXTENSIONS` lists drifting out of sync |

---

## Future Improvements

- [ ] Identity-based access control (MFA before unlock)
- [ ] Network micro-segmentation integration
- [ ] File entropy analysis for detecting in-progress encryption
- [ ] Configurable detection thresholds via a config file
- [ ] Process-level attribution (which PID triggered mass modifications)
- [ ] Email / webhook alerts on lockdown events
- [ ] Unit test coverage for detection and recovery logic

---

## Disclaimer

This project was developed strictly for educational and defensive cybersecurity purposes.

The ransomware simulation components are designed only to demonstrate behavioral detection,
containment, recovery, and resilience concepts within controlled testing environments.

Do not use this project against systems, files, or environments without explicit authorization.