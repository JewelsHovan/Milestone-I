# Progress Tracker

## 1. Project Overview

This project focuses on analyzing electronic health records (EHR) from the MIMIC dataset to explore patient data, predict acuity levels, collect disease statistics, and analyze patient flow within healthcare facilities. The primary objectives include data preprocessing, exploratory data analysis (EDA), building and interpreting classification models, scraping disease categories, and understanding patient transfer patterns.

## 2. Project Structure

The project is organized as follows:

- **`src/`**: Contains all the source code modules and packages.
  - **`__init__.py`**: Indicates that `src` is a Python package.
  - **`data/`**
    - **`data_merger.py`**: Functions to merge and aggregate data from various sources.
  - **`notebooks/`**
    - **`__init__.py`**: Initializes the notebooks package.
    - **Jupyter Notebooks**: Used for exploratory data analysis and prototyping.
  - **`preprocessing/`**
    - **`__init__.py`**: Initializes the preprocessing package.
    - **`admissions_preprocessor.py`**: Preprocesses `admissions.csv`, handling missing values and feature engineering for admission data.
    - **`ed_stay_preprocessor.py`**: Processes `edstays.csv`, including time conversions and calculation of Length of Stay (LOS) in the Emergency Department.
    - **`triage_preprocessor.py`**: Preprocesses `triage.csv`, standardizing vital signs and other triage assessment data.
    - **`diagnosis_preprocessor.py`**: Handles preprocessing of `diagnosis.csv`, mapping ICD codes to broader disease categories using `disease_categories.csv`.
  - **`utils/`**
    - **`__init__.py`**: Initializes the utils package.
    - **Utility Functions**: Common helper functions used across different modules, such as data loading and transformations.

- **Project Documentation and Notebooks**:
  - **`README.md`**: Provides a comprehensive overview of the project, datasets used, objectives, and team contributions.
  - **`Progress.md`**: Tracks the project's progress, milestones, and next steps.
  - **`DataCollection.ipynb`**: Notebook for collecting external data, such as disease statistics, through web scraping and API integrations.
  - **`EDA.ipynb`**: Exploratory Data Analysis notebook for initial data exploration and visualization.
  - **`Classification-Interpretation.ipynb`**: Notebook for building classification models and interpreting their outputs.
  - **`FlowAnalysis.ipynb`**: Analyzes patient flow and transfer patterns within the hospital.

## 3. Data Collection

### a. Downloading MIMIC Data

- **Datasets Acquired:**
  - `edstays.csv` (Emergency Department Stays)
  - `admissions.csv` (Hospital Admissions)
  - `transfers.csv` (Patient Transfers)
  - `diagnosis.csv` (Diagnosis Information)
  - `triage.csv` (Triage Data)
  - `vitalsign.csv` (Vital Signs)
  - `medrecon.csv` (Medication Reconciliation)
  - `patients.csv` (Patient Demographics)

### b. Web Scraping ICD Codes

- **Objective:** Extract disease categories and their corresponding ICD-10 codes from the [WHO ICD-10 Browser](https://icd.who.int/browse10/2010/en#/XXII).
- **Tools Used:** Selenium for dynamic content loading and BeautifulSoup for parsing HTML.
- **Process:**
  - Navigated through each ICD-10 chapter.
  - Extracted chapter titles, ICD codes (first 3 characters/digits), and block titles.
  - Stored the scraped data in `disease_categories.csv`.

### c. Collecting Disease Statistics (`DataCollection.ipynb`)

- **Objective:** Gather up-to-date statistics on various disease categories, including prevalence, incidence, mortality, and economic impact.
- **Process:**
  - **Web Scraping:**
    - Extracted disease categories and ICD codes from the WHO ICD-10 Browser.
    - Saved the data into `disease_categories.csv`.
  - **API Integration:**
    - Utilized OpenAI's API (via Perplexity) to fetch statistics for each disease category.
    - Structured prompts to ensure responses are in valid JSON format.
    - Extracted and parsed JSON responses to compile a comprehensive DataFrame.
    - Stored the collected statistics in `disease_data.csv`.

## 4. Data Preprocessing

### a. Preprocessing Modules (`src/preprocessing/`)

- **`admissions_preprocessor.py`**:
  - Processes `admissions.csv`, handling missing values and performing feature engineering related to admission data.
- **`ed_stay_preprocessor.py`**:
  - Preprocesses `edstays.csv`, including time conversions and calculation of ED Length of Stay (`ed_los_hours`).
- **`triage_preprocessor.py`**:
  - Standardizes vital signs and other triage assessment data from `triage.csv`.
- **`diagnosis_preprocessor.py`**:
  - Maps detailed ICD diagnosis codes to broader disease categories using `disease_categories.csv`.

### b. Utility Functions (`src/utils/`)

- **Functions:**
  - `nunique_per_cat(df)`: Returns the number of unique values for each categorical column.
  - `min_max_for_cols(df)`: Prints the minimum and maximum values for numerical columns.
  - Other helper functions for data validation and transformation.

## 5. Exploratory Data Analysis (EDA)

### a. EDA Notebook (`EDA.ipynb`)

- **Data Importing:**
  - Loaded all relevant CSV files into Pandas DataFrames.
- **Initial Exploration:**
  - Utilized `missingno` to visualize missing data patterns.
  - Analyzed unique values and distributions for categorical and numerical features.
- **Data Cleaning:**
  - Converted `intime` and `outtime` columns to datetime formats.
  - Calculated ED Length of Stay (`ed_los_hours`).
  - Mapped detailed race categories to broader groups using `race_mapping`.
- **Visualizations:**
  - Plotted distributions of vital signs and other continuous variables.
  - Explored racial disparities in ED length of stay.
- **Regression Analysis:**
  - Prepared data for regression models to interpret feature impacts on LOS.

## 6. Classification and Model Interpretation

### a. Classification Notebook (`Classification-Interpretation.ipynb`)

- **Data Preparation:**
  - Selected relevant features and target variable (`acuity`) for classification.
  - Split data into training and testing sets (80-20 split).
- **Preprocessing Pipeline:**
  - **Numerical Features:**
    - Imputed missing values using the mean.
    - Standardized features with `StandardScaler`.
  - **Categorical Features:**
    - Imputed missing values using the most frequent category.
    - Applied `OneHotEncoder` to convert categorical variables into numerical format.
- **Model Training:**
  - Trained a `RandomForestClassifier` with 300 estimators and a maximum depth of 4.
- **Model Evaluation:**
  - Achieved train and test accuracy scores of approximately 0.605.
  - Generated a classification report highlighting precision, recall, and F1-scores for each class.
- **Feature Importance:**
  - Identified and visualized the top 10 most important features influencing model predictions.

## 7. Patient Flow Analysis

### a. Flow Analysis Notebook (`FlowAnalysis.ipynb`)

- **Data Loading:**
  - Imported `transfers.csv` and `patients.csv` into DataFrames.
- **Preprocessing:**
  - Converted `intime` and `outtime` columns to datetime formats.
  - Calculated Length of Stay (`los`) for each transfer.
- **Movement Summary:**
  - Grouped data by `subject_id` and `hadm_id` to summarize patient transfers.
  - Computed the number of transfers, total LOS, number of unique care units, and average time per unit.
- **Common Pathways Analysis:**
  - Identified and listed the most frequent patient pathways through various care units.
- **Visualizations:**
  - Plotted the distribution of the number of transfers per patient.
  - Analyzed the relationship between the number of transfers and total LOS using scatter plots.

## 8. Current Status

- **Completed:**
  - **Data Collection:**
    - Acquired all relevant MIMIC datasets.
    - Extracted disease categories and ICD-10 codes via web scraping.
    - Collected detailed disease statistics using API integrations.
  - **Data Preprocessing:**
    - Developed preprocessing modules for admissions, ED stays, triage, and diagnosis data.
    - Implemented utility functions for data validation and transformation.
  - **EDA and Modeling:**
    - Conducted exploratory data analysis with insightful visualizations.
    - Developed and evaluated a Random Forest classification model for predicting patient acuity.
  - **Patient Flow Analysis:**
    - Analyzed patient transfer patterns and their impact on hospital LOS.
    - Visualized common patient pathways and identified potential bottlenecks.
  - **Project Organization:**
    - Structured the codebase with modular design for scalability and maintainability.
    - Documented the project thoroughly in `README.md` and `Progress.md`.

## 9. Next Steps

- **Model Improvement:**
  - Explore hyperparameter tuning and alternative classification algorithms to enhance model performance.
  - Incorporate additional features from the newly collected disease statistics.
- **Integration:**
  - Combine disease statistics with clinical data for more enriched analyses.
  - Analyze correlations between disease prevalence and patient outcomes.
- **Advanced Analytics:**
  - Implement regression models to interpret factors affecting LOS and other key metrics.
  - Conduct longitudinal studies on patient outcomes based on transfer patterns.
- **Reporting:**
  - Compile findings into comprehensive reports and interactive dashboards for stakeholders.
  - Prepare presentations to communicate insights effectively.
- **Automation:**
  - Automate data collection and preprocessing pipelines using scripts in `src/`.
  - Set up scheduled tasks for regular data updates.

## 10. Challenges Encountered

- **Data Quality:**
  - Addressed missing values and outliers in large datasets.
  - Ensured consistency across different data sources.
- **API Limitations:**
  - Managed API rate limits and response formatting issues during data collection.
- **Computational Resources:**
  - Optimized code for performance to handle extensive datasets efficiently.

## 11. Lessons Learned

- **Modular Design:**
  - Creating modular preprocessing scripts enhanced collaboration and code maintainability.
- **Effective Data Integration:**
  - Integrating external data sources added significant value to the analysis.
- **Importance of Documentation:**
  - Thorough documentation facilitated smoother progress tracking and team communication.

---

*Note: This `Progress.md` reflects the latest updates, including the project structure and current progress.*
