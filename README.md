# **Milestone I: Hospital Efficiency and Patient Flow Analysis**

## **Project Overview**

This project focuses on visualizing hospital inefficiencies by analyzing patient stays in the Emergency Department (ED) and Intensive Care Unit (ICU) using the MIMIC-IV dataset. Our goal is to identify correlations between the severity of medical conditions and patient length of stay. By understanding these relationships, we aim to discover patterns of resource overuse or potential bottlenecks in hospital operations, particularly those leading to unnecessary extended stays. Minimizing these inefficiencies could help hospitals better allocate resources, improve patient care, and reduce healthcare costs.

In addition to the MIMIC-IV data, we are incorporating external datasets to enrich our analysis. This integration allows us to extract insights that would not be possible using any one dataset in isolation.

## **Team Members**

- **Jewels Hovan** (jhovan)
- **Liu Liu** (luvul)
- **George Mathew** (ggmathew)

## **Datasets**

We are working with publicly available datasets from the **MIMIC-IV** database and external sources.

### **Primary Dataset: MIMIC-IV Clinical Database**

- **Description**: Contains comprehensive clinical data for hospital admissions, including patient demographics, diagnoses, procedures, medications, and vital signs.
- **Size**: Various tables totaling over 550,000 records.
- **Access Method**: Accessible through PhysioNet with appropriate credentials.
- **Source**: [MIMIC-IV Clinical Database](https://mimic.mit.edu/docs/iv/)

### **External Datasets**

#### 1. **ICD-10 Classification Data**

- **Description**: A dataset mapping ICD-10 codes to disease descriptions and hierarchical categories. Enables grouping of diagnoses into broader categories for analysis.
- **Size**: Comprehensive coverage of ICD-10 codes.
- **Access Method**: Generated via web scraping from the World Health Organization (WHO) ICD-10 website.
- **Source**: [WHO ICD-10 Classification](https://icd.who.int/browse10/2010/en)

#### 2. **National Insurance Data**

- **Description**: Medicare enrollment and claims data providing state and county-level statistics on insurance coverage and healthcare utilization.
- **Size**: Data from 2013 onwards; varies by report.
- **Access Method**: Available through the Centers for Medicare & Medicaid Services (CMS).
- **Source**: [CMS Medicare Enrollment Reports](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment)

#### 3. **Boston Demographics and Socioeconomic Data**

- **Description**: City-level demographic data, including age distribution, income levels, and other socioeconomic indicators for Boston residents.
- **Size**: Varies by dataset.
- **Access Method**: Publicly available through city and state data portals.
- **Source**: [Boston Open Data](https://data.boston.gov/)

## **Project Objectives**

- **Visualize Patient Flow**: Create detailed flow diagrams to illustrate patient pathways from ED admission through ICU stays and discharge.
- **Resource Utilization Analysis**: Analyze resource usage to identify bottlenecks and inefficiencies in patient management, including time-series analyses of bed occupancy rates.
- **Integrate External Data**: Merge MIMIC-IV data with external datasets to explore associations between hospital data and broader socioeconomic factors.
- **Assess Insurance Impact**: Investigate how insurance type and coverage levels correlate with patient outcomes, length of stay, and resource utilization.
- **Disease Categorization**: Utilize ICD-10 classifications to group diagnoses, facilitating higher-level analyses of disease patterns.

## **Data Cleaning and Manipulation**

- **Outlier Removal**: Identify and address extreme outliers in physiological measurements to improve data quality.
- **Handling Missing Data**: Use imputation techniques or model-based methods to handle missing values.
- **Feature Engineering**:
  - **Time Intervals**: Calculate durations between key events (e.g., ED arrival to ICU transfer).
  - **Risk Scores**: Develop patient risk scores based on vital signs and diagnoses.
  - **Disease Grouping**: Map ICD-10 codes to broader categories using the scraped classification data.
  - **Cost Estimation**: Estimate treatment costs by integrating average procedure and medication prices.
- **Data Integration**:
  - **Merging Datasets**: Align MIMIC-IV data with external datasets using common keys (e.g., ICD codes, demographics).
  - **Aggregation**: Aggregate data to match granularity levels when merging (e.g., age groups, disease categories).
- **Text Data Processing**: Apply NLP techniques to process textual fields like chief complaints and pain descriptions.

## **Analysis Plan**

We will employ a variety of analytical techniques:

- **Descriptive Statistics**: Summarize key variables to validate data integrity and understand baseline characteristics.
- **Correlation and Hypothesis Testing**: Examine relationships between variables such as disease severity, length of stay, insurance coverage, and socioeconomic factors.
- **Comparative Analysis**: Compare hospital data against national or state-level statistics to identify unique patterns or deviations.
- **Survival Analysis**: Utilize time-to-event models to evaluate factors influencing patient length of stay.
- **Cost Analysis**: Analyze the financial aspects of patient care in relation to outcomes and resource utilization.

## **Visualizations**

1. **Sankey Diagrams**: Visualize patient flow through hospital departments, highlighting transitions and bottlenecks.
2. **Heatmaps**: Display temporal patterns in bed occupancy and resource utilization.
3. **Disease Distribution Charts**: Use bar and pie charts to represent the prevalence of disease categories.
4. **Geospatial Maps**: Map patient data to visualize geographic patterns within Boston.
5. **Correlation Matrices**: Illustrate relationships between multiple variables, including external factors.

## **Ethical Considerations**

- **Patient Privacy**: Adhere strictly to HIPAA regulations and data use agreements. Use de-identified data and ensure no re-identification risks.
- **Data Integrity**: Be cautious with date and time data, as MIMIC-IV includes date shifts for privacy. Align temporal analyses appropriately.
- **Bias Mitigation**: Identify and correct for biases related to demographics or socioeconomic status in both data collection and analysis.

## **Contributions**

- **Jewels Hovan**:
  - Data cleaning and preprocessing, including handling of outliers and missing values.
  - Web scraping and compilation of ICD-10 classification data.
  - Development of visualizations such as Sankey diagrams and disease distribution charts.

- **Liu Liu**:
  - Research and integration of external datasets, focusing on demographics and socioeconomic factors.
  - Comparative analysis between hospital data and external statistics.
  - Resource utilization analysis and associated visualizations.

- **George Mathew**:
  - Exploration and integration of insurance data.
  - Analysis of the impact of insurance coverage on patient outcomes and resource use.
  - Creation of visualizations related to insurance and socioeconomic data.

## **Changelog**

- **2023.10.05**:
  - **Updated**: Incorporated external datasets into the project scope.
  - **Added**: New objectives related to external data integration and insurance impact analysis.
  - **Revised**: Data cleaning section to include new feature engineering efforts.
  - **Expanded**: Contributions to reflect team members' current roles.
  - **Polished**: Improved document formatting and clarity.

- **2022.07.27.1.CT**: Initial project proposal for SIADS 593.
- **2021.07.24.1.AW**: Adjusted title, added numbered sections, simplified headings, and edited text.

## **Future Work**

- **Advanced Modeling**: Implement machine learning models (e.g., tree ensembles) that do not rely on normal distribution assumptions to predict patient outcomes.
- **Further Data Collection**: Continue exploring additional external datasets, such as weather or seasonal flu data, to assess their impact on patient flow.
- **Deep Dive Analyses**: Investigate specific findings in more detail, such as the effect of socioeconomic status on disease prevalence within Boston.

## **References**

- [MIMIC-IV Documentation](https://mimic.mit.edu/docs/iv/)
- [WHO ICD-10 Classification](https://icd.who.int/browse10/2010/en)
- [CMS Medicare Enrollment Reports](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment)
- [Boston Open Data](https://data.boston.gov/)

---

*Note: This README reflects the current progress and ideas discussed by the team. It will be updated as the project evolves.*