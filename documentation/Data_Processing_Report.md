
# MIMIC Data Preprocessing Report

This document outlines the data manipulation and cleaning processes applied to various tables in the MIMIC dataset.

## 1. Diagnosis Table

Function: `preprocess_diagnosis()`

- Separated ICD-9 and ICD-10 codes into different dataframes
- Processed ICD-9 codes:
  - Extracted category codes from ICD-9 codes
  - Merged with ICD-9 codes reference table
- Processed ICD-10 codes:
  - Extracted category codes and letter codes from ICD-10 codes
  - Merged with ICD-10 codes reference table
- Combined ICD-9 and ICD-10 dataframes
- Applied a custom disease category mapping
- Filled missing subcategories with 'Other'
- Converted relevant columns to category dtype
- Dropped unnecessary columns

## 2. Admissions Table

Function: `preprocess_admissions()`

- Converted date columns to datetime format
- Computed length of stay for each admission
- Mapped race values to standardized categories
- Filled missing discharge locations with 'Unknown'
- Converted categorical columns to category dtype
- Dropped 'admit_provider_id' column
- Added 'is_dead' column based on presence of death time
- Imputed missing values for insurance, marital status, language, and admission location using mode

## 3. Patients Table

Function: `preprocess_patients()`

- Converted 'dod' (date of death) to datetime format
- Converted 'anchor_year_group' and 'gender' to category dtype
- Added 'is_dead' column based on presence of date of death

## 4. Transfers Table

Function: `preprocess_transfers()`

- Converted 'intime' and 'outtime' to datetime format
- Computed length of stay in hours
- Applied a custom mapping to group care units
- Converted categorical variables to category dtype
- Updated 'outtime' and 'los' for discharge events
- Dropped rows with missing length of stay

## 5. Triage Table

Function: `preprocess_triage()`

- Preprocessed chief complaints using NLP techniques:
  - Tokenization
  - Lemmatization
  - Removal of stopwords and non-alphabetic characters
- Assigned topics to complaints using LDA topic modeling
- Converted acuity and topic to ordinal categories
- Dropped original and processed complaint text columns

## 6. Vital Signs Table

Function: `preprocess_vitalsigns()`

- Cleaned vital signs by applying valid ranges:
  - Temperature: 95.0 - 107.6 °F
  - Heart rate: 20 - 250 bpm
  - Respiratory rate: 4 - 60 breaths/min
  - O2 saturation: 70 - 100%
  - Systolic blood pressure: 50 - 250 mmHg
  - Diastolic blood pressure: 20 - 150 mmHg
- Dropped rows with missing values after cleaning
- Forward-filled missing pain scores

## 7. ED Stays Table

Function: `preprocess_ed_stay()`

- Converted 'intime' and 'outtime' to datetime format
- Computed length of stay for each ED visit
- Mapped race values to standardized categories
- Converted categorical columns to category dtype
- Added 'admitted' column based on presence of hospital admission ID

## 8. ICU Stays Table

Function: `preprocess_icu_stays()`

- Converted 'intime' and 'outtime' to datetime format
- Converted care unit columns to category dtype

## General Preprocessing Steps

- Utilized custom utility functions for common tasks like datetime conversion and length of stay calculation
- Applied consistent naming conventions across tables
- Standardized categorical variables using category dtype for efficiency
- Handled missing values through various strategies (imputation, forward-filling, or dropping) depending on the context