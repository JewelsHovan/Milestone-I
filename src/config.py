import os

# Base directory for data files
BASE_DATA_DIR = os.path.join("..", "Data")

# File paths
FILE_PATHS = {
    'edstays': os.path.join(BASE_DATA_DIR, "ED", "edstays.csv"),
    'admissions': os.path.join(BASE_DATA_DIR, "HOSP", "admissions.csv"),
    'transfers': os.path.join(BASE_DATA_DIR, "HOSP", "transfers.csv"),
    'diagnosis': os.path.join(BASE_DATA_DIR, "ED", "diagnosis.csv"),
    'triage': os.path.join(BASE_DATA_DIR, "ED", "triage.csv"),
    'vitalsigns': os.path.join(BASE_DATA_DIR, "ED", "vitalsign.csv"),
    'medrecon': os.path.join(BASE_DATA_DIR, "ED", "medrecon.csv"),
    'patients': os.path.join(BASE_DATA_DIR, "HOSP", "patients.csv"),
    'disease_categories': os.path.join(BASE_DATA_DIR, "disease_categories.csv")
}

# Other configurations
CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'validation_size': 0.2,
}

# API keys (consider using environment variables for sensitive information)
API_KEYS = {
    'openai': os.environ.get('OPENAI_API_KEY'),
    'perplexity': os.environ.get('PERPLEXITY_API_KEY'),
}