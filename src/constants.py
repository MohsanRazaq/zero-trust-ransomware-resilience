SUSPICIOUS_EXTENSIONS = [
    ".locked",
    ".encrypted",
    ".crypt",
    ".enc",
]

BACKUP_DIR = "backup"
PROTECTED_DIR = "protected"
LOG_DIR = "logs"

MAX_BACKUP_VERSIONS = 3          # keep only 3 versions per file
DETECTION_WINDOW_SECONDS = 10    # sliding window for mass-mod detection
DETECTION_THRESHOLD = 5          # modifications that trigger lockdown
ALERT_COOLDOWN_SECONDS = 10      # min seconds between repeated alerts
ENTROPY_SCORE_THREASHOLD=7.5