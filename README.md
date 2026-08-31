# AI-Powered Travel Sentiment and Trend Analytics Platform

## Project Overview

The **AI-Powered Travel Sentiment and Trend Analytics Platform** is a data analytics project focused on analyzing hotel and travel reviews using **Python, data analysis, and Natural Language Processing (NLP)** techniques.

The project aims to transform unstructured traveler reviews into meaningful insights related to:

- Tourist sentiment
- Travel and destination trends
- Seasonal travel patterns
- Budget-related preferences
- Safety-related insights

The final goal is to develop an interactive analytics platform that combines data processing, NLP, analysis, visualization, and dashboarding.

---

## Objectives

- Analyze hotel and travel reviews using data analytics and NLP.
- Identify sentiment expressed in traveler reviews.
- Discover travel-related patterns and trends.
- Explore destination and seasonal travel patterns.
- Extract potential budget and safety-related insights.
- Present insights through meaningful visualizations and interactive dashboards.

---

## Dataset

This project uses the **515K Hotel Reviews Data in Europe** dataset from Kaggle.

**Dataset Source:**  
https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe

### Dataset Information

| Stage | Rows | Columns |
|---|---:|---:|
| Original Dataset | 515,738 | 17 |
| After Data Cleaning | 515,212 | 17 |
| After NLP Preprocessing | 515,212 | 19 |

The dataset contains information including:

- Hotel Name
- Hotel Address
- Review Date
- Reviewer Nationality
- Positive Review
- Negative Review
- Reviewer Score
- Average Hotel Score
- Review Tags
- Geographic Location

---

## Project Structure

## Project Structure

travel-sentiment-analytics/
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_data_preprocessing.ipynb
│
├── src/
│   ├── preprocessing/
│   └── utils/
│
├── .gitignore
├── README.md
└── requirements.txt

---

## Data Processing Workflow

Raw Hotel Reviews Dataset
          │
          ▼
   Data Collection
          │
          ▼
    Data Cleaning
          │
          ▼
   Cleaned Dataset
          │
          ▼
  NLP Preprocessing
          │
          ▼
  Processed Dataset
          │
          ▼
Exploratory Data Analysis
          │
          ▼
  Sentiment Analysis
          │
          ▼
 Travel Trend Analysis
          │
          ▼
 Data Visualization
          │
          ▼
 Interactive Dashboard

---

## Completed Work

### Data Collection

- Selected the 515K Hotel Reviews Data in Europe dataset.
- Loaded and inspected the dataset.
- Examined dataset dimensions and column information.
- Checked data types and missing values.

### Data Cleaning

The following cleaning operations were performed:

- Checked and removed duplicate records.
- Analyzed missing values.
- Converted `Review_Date` to datetime format.
- Converted `days_since_review` from text to numerical format.
- Created a combined `Review_Text` column using positive and negative reviews.
- Handled missing review text.
- Cleaned review text by:
  - Converting text to lowercase
  - Removing URLs
  - Removing HTML tags
  - Removing extra whitespace
  - Removing punctuation

### NLP Preprocessing

The cleaned review text was further processed using NLP techniques:

- Tokenization
- Stopword removal
- Preservation of important negation words such as `no`, `not`, `nor`, and `never`
- Lemmatization
- Creation of processed review text

A `Processed_Review` column was created to store the final preprocessed review text.

---

## Project Progress

- [x] Data Collection
- [x] Data Cleaning
- [x] Data Preprocessing
- [ ] Exploratory Data Analysis (EDA)
- [ ] Sentiment Analysis
- [ ] Travel Trend Analysis
- [ ] Seasonal Pattern Analysis
- [ ] Budget and Safety Insights
- [ ] Data Visualization
- [ ] Interactive Dashboard

---

## Technologies Used

### Current Technologies

- Python
- Pandas
- NumPy
- NLTK
- Jupyter Notebook
- Visual Studio Code
- Git
- GitHub

Additional technologies may be added as the project progresses.

---

## Setup and Installation

### 1. Clone the Repository

git clone <repository-url>

### 2. Navigate to the Project Directory

cd travel-sentiment-analytics

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Dataset Setup

The original dataset is not included in this repository because of its large file size.

Download the dataset from Kaggle and place the required dataset file inside:

data/raw/

The dataset source is available in the Dataset section above.

---

## Future Work

The next stages of the project include:

- Exploratory Data Analysis (EDA)
- Sentiment analysis
- Travel and destination trend analysis
- Seasonal pattern analysis
- Budget-related analysis
- Safety-related analysis
- Data visualization
- Interactive dashboard development

---

## Author

**Krishna Gondaliya**