import csv
from pathlib import Path

DATASET_FILE = Path(__file__).resolve().parent / "dataset.csv"

def log_ml_features(velocity, entropy, is_malicious):
    file_exists = DATASET_FILE.exists()
    with open(DATASET_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["velocity", "entropy", "is_malicious"])
        writer.writerow([velocity, entropy, is_malicious])