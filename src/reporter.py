import os
from datetime import datetime

from constants import LOG_DIR


def generate_threat_report(
    attack_type: str,
    affected_path: str,
    response_action: str,
    entropy: float,
    velocity: int,
    THREAT_SCORE:int
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(LOG_DIR, exist_ok=True)

    report = f"""
==================================================
Incident Timestamp : {timestamp}
Attack Type        : {attack_type}
Affected Path      : {affected_path}
Response Action    : {response_action}
THREAT_SCORE       : {THREAT_SCORE}
FORENSIC ANALYTICS:
--------------------------------------------------
Peak Shannon Entropy : {entropy:.2f} / 8.00
Modification Velocity: {velocity} files in window
==================================================
"""
    with open(f"{LOG_DIR}/threat_report.log", "a") as f:
        f.write(report)

    print("[REPORT] Threat report generated")