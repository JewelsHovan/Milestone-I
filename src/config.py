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

DISEASE_CATEGORY_MAPPING = {
    # ICD-10 mappings
    'Certain infectious and parasitic diseases': 'Infectious & Parasitic',
    'Neoplasms': 'Neoplasms',
    'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism': 'Blood & Immune System',
    'Endocrine, nutritional and metabolic diseases': 'Endocrine & Metabolic',
    'Mental and behavioural disorders': 'Mental & Behavioral',
    'Diseases of the nervous system': 'Nervous System',
    'Diseases of the eye and adnexa': 'Eye & Adnexa',
    'Diseases of the ear and mastoid process': 'Ear & Mastoid',
    'Diseases of the circulatory system': 'Circulatory System',
    'Diseases of the respiratory system': 'Respiratory System',
    'Diseases of the digestive system': 'Digestive System',
    'Diseases of the skin and subcutaneous tissue': 'Skin & Subcutaneous',
    'Diseases of the musculoskeletal system and connective tissue': 'Musculoskeletal & Connective',
    'Diseases of the genitourinary system': 'Genitourinary System',
    'Pregnancy, childbirth and the puerperium': 'Pregnancy & Childbirth',
    'Certain conditions originating in the perinatal period': 'Perinatal Conditions',
    'Congenital malformations, deformations and chromosomal abnormalities': 'Congenital & Chromosomal',
    'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified': 'Symptoms & Abnormal Findings',
    'Injury, poisoning and certain other consequences of external causes': 'Injury & Poisoning',
    'External causes of morbidity and mortality': 'External Causes',
    'Factors influencing health status and contact with health services': 'Health Factors & Services',
    'Codes for special purposes': 'Special Purposes',
    
    # ICD-9 mappings
    'Infectious And Parasitic Diseases': 'Infectious & Parasitic',
    'Neoplasms': 'Neoplasms',
    'Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders': 'Endocrine & Metabolic',
    'Diseases Of Blood And Blood-Forming Organs': 'Blood & Immune System',
    'Mental Disorders': 'Mental & Behavioral',
    'Diseases Of The Nervous System And Sense Organs': 'Nervous System',
    'Diseases Of The Circulatory System': 'Circulatory System',
    'Diseases Of The Respiratory System': 'Respiratory System',
    'Diseases Of The Digestive System': 'Digestive System',
    'Diseases Of The Genitourinary System': 'Genitourinary System',
    'Complications Of Pregnancy, Childbirth, And The Puerperium': 'Pregnancy & Childbirth',
    'Diseases Of The Skin And Subcutaneous Tissue': 'Skin & Subcutaneous',
    'Diseases Of The Musculoskeletal System And Connective Tissue': 'Musculoskeletal & Connective',
    'Congenital Anomalies': 'Congenital & Chromosomal',
    'Certain Conditions Originating In The Perinatal Period': 'Perinatal Conditions',
    'Symptoms, Signs, And Ill-Defined Conditions': 'Symptoms & Abnormal Findings',
    'Injury And Poisoning': 'Injury & Poisoning'
}