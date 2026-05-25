![Python](https://img.shields.io/badge/Python-3.x-blue)
![Focus](https://img.shields.io/badge/Focus-Defensive%20Security-red)
![Architecture](https://img.shields.io/badge/Architecture-Event%20Driven-orange)
![Detection](https://img.shields.io/badge/Detection-Behavioral%20Analysis-yellow)
![Security](https://img.shields.io/badge/Security-Ransomware%20Resilience-darkred)
![Status](https://img.shields.io/badge/Status-v1.0-success)
![Learning](https://img.shields.io/badge/Purpose-Security%20Engineering-informational)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)

# Zero-Trust Ransomware Resilience


A Python-based defensive security engineering project focused on ransomware behavior detection, automated containment, backup resilience, and recovery workflow simulation.

---

# Why I Built This

While studying cybersecurity, I noticed most ransomware discussions focus heavily on the attacker side — encryption, payloads, exploitation — but much less on how defenders actually detect and contain ransomware activity in real systems.

After reading about incidents like the Colonial Pipeline ransomware attack, I became interested in understanding the defender’s perspective:

* How can suspicious activity be detected early?
* What happens operationally during containment?
* How do backup and recovery systems actually work?
* What defensive engineering decisions matter most?

Instead of building another basic security script, I wanted to simulate a lightweight ransomware resilience pipeline that combines:

* behavioral monitoring
* automated containment
* backup protection
* recovery workflows
* incident reporting

The goal was not to create a production EDR, but to deeply understand how defensive security systems behave internally.

---

# How It Works (Simple Explanation)

The system continuously monitors a protected folder in real time.

If it notices ransomware-like behavior — such as:

* rapid mass file modifications
* suspicious encrypted file extensions
* abnormal file activity

it automatically:

1. locks the protected files into read-only mode
2. prevents further modifications
3. creates threat logs and reports
4. allows controlled recovery using protected backups

In simple terms:

```text id="6nb"
Filesystem Activity
        ↓
Threat Detection
        ↓
Folder Lockdown
        ↓
Backup Recovery
        ↓
Threat Reporting
```

The project simulates how defensive security systems try to slow down ransomware damage before files are fully destroyed.

---

# What The System Detects

## 1. Behavioral Ransomware Activity

Detects rapid mass file modifications within a short time window.

Possible indicators:

* automated encryption behavior
* mass file rewriting
* ransomware propagation activity

---

## 2. Suspicious File Extensions

Detects extensions commonly associated with ransomware:

* `.locked`
* `.encrypted`
* `.crypt`
* `.enc`

Possible indicators:

* encrypted victim files
* ransomware renaming behavior
* post-encryption activity

---

# Core Features

* Real-time filesystem monitoring using Watchdog
* Behavioral ransomware detection
* Sliding-window activity analysis
* Suspicious extension detection
* Automated folder lockdown
* Read-only containment (`chmod`)
* Versioned backup system
* Backup pruning protection
* Backup restoration workflow
* Threat report generation
* Persistent activity logging
* Environment-variable-based recovery authentication

---

# Project Architecture

```text id="0vb"
[Filesystem Event]
        ↓
[Monitor Layer]        monitor.py
        ↓
[Detection Engine]     detector.py
        ↓
[Containment Engine]   response.py
        ↓
[Backup & Recovery]    backup_manager.py / recovery.py
        ↓
[Threat Reporting]     reporter.py / logger.py
```

The architecture follows a layered defensive workflow model where each component handles a separate operational responsibility.

This separation helped me better understand:

* event-driven systems
* detection pipelines
* containment workflows
* recovery orchestration

---

# Hardest Problem I Solved

The hardest challenge was designing the containment and recovery workflow safely.

Initially, I only locked the top-level protected directory. Later I discovered nested folders could still create traversal and permission issues during recovery operations.

Another difficult issue was balancing:

* automated lockdown
  vs
* safe recovery access

I learned that filesystem permissions are much more complex operationally than they first appear, especially when recursive traversal and restoration workflows are involved.

I also struggled with telemetry consistency while tracking integrity events and backup versions across multiple file operations.

---

# What Surprised Me Most

I was surprised by how much defensive cybersecurity depends on handling operational edge cases rather than simply detecting attacks.

Some examples:

* race conditions between monitoring events
* duplicate filesystem notifications
* backup version conflicts
* recursive permission failures
* malformed event sequences
* recovery-state synchronization problems

I also realized modern defensive systems rely heavily on:

* telemetry pipelines
* behavioral heuristics
* state management
* operational resilience

rather than simple “virus detection.”

---

# Security Design Decisions

| Decision                                     | Reason                                                        |
| -------------------------------------------- | ------------------------------------------------------------- |
| Recovery key stored as environment variable  | Prevents secrets from appearing in source code or Git history |
| `hmac.compare_digest()` for key verification | Helps mitigate timing-based brute-force attacks               |
| 3-attempt recovery lockout                   | Slows repeated unauthorized unlock attempts                   |
| Read-only backup protection (`0o444`)        | Helps preserve recovery copies from accidental overwrite      |
| Backup version pruning                       | Prevents uncontrolled disk consumption                        |
| `os.path.basename()` during restore          | Helps prevent path traversal abuse                            |
| Layered architecture separation              | Improves maintainability and debugging clarity                |
| Centralized configuration/constants          | Prevents duplicated configuration drift                       |

---

# Project Structure

```text id="8zb"
zero-trust-ransomware-resilience/
│
├── src/
│   ├── main.py
│   ├── constants.py
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

---

# Attack Simulation

The project includes controlled ransomware simulation scripts for testing:

* mass file modification behavior
* suspicious extension attacks
* containment response workflows
* recovery validation

This helped me better understand how detection thresholds and operational response timing affect defensive systems.

---

# Recovery Workflow

When suspicious activity is detected, the system:

1. locks the protected directory
2. converts files into read-only mode
3. preserves backups
4. logs incident details

Recovery requires:

* stopping monitoring manually
* entering the recovery key
* restoring backups safely

This simulates basic incident-response containment and restoration behavior.

---

# What I Learned

This project taught me much more than Python syntax.

The biggest lessons were:

* event-driven architecture
* defensive systems thinking
* telemetry handling
* behavioral detection design
* filesystem permissions
* operational edge cases
* resilience engineering

Most importantly, I learned that real security engineering is often about:

* reliability
* state management
* failure handling
* operational workflows

not just detecting attacks.

---

# What’s Next

The next major improvement is redesigning the system into a more mature Zero Trust architecture.

Planned improvements:

* entropy-based encryption detection
* process-level attribution using `psutil`
* MFA-based recovery access
* encrypted backups
* signed backup integrity verification
* tamper-resistant audit logging
* Flask-based monitoring dashboard
* JWT-authenticated recovery workflows

I also want to redesign parts of the detection pipeline to improve modularity and reduce architecture coupling between monitoring, detection, and response layers.

---

# Disclaimer

This project was built strictly for educational and defensive cybersecurity purposes.

The ransomware simulation components exist only to demonstrate:

* behavioral detection
* containment logic
* backup resilience
* recovery engineering

within controlled testing environments.

Do not use this project against systems or environments without explicit authorization.
