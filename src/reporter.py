from datetime import datetime
import os

def generate_threat_report(
    attack_type,
    affected_path,
    response_action
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    report=f""" 
==================================================
Incident Timestamp : {timestamp}
Attack Type        : {attack_type}
Affected Path      : {affected_path}
Response Action    : {response_action}
==================================================
    """
    with open("logs/threat_report.log", "a") as f:
        f.write(report)
    print("[REPORT] Threat report generated")