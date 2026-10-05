# AI-Powered Travel Sentiment and Trend Analytics Platform

## Project Overview

The **AI-Powered Travel Sentiment and Trend Analytics Platform** is a data analytics and Natural Language Processing (NLP) project focused on extracting meaningful insights from hotel and traveler reviews.

The project transforms large-scale unstructured review data into structured information that can be analyzed to understand:

* Traveler sentiment
* Review and travel trends
* Destination patterns
* Seasonal review activity
* Trip-type behavior
* Reviewer and hotel-related patterns

The project follows a complete data analytics workflow, from data collection and cleaning to NLP preprocessing, exploratory analysis, sentiment analysis, and travel trend analysis.

---

## Objectives

* Analyze a large-scale hotel review dataset using Python and data analytics techniques.
* Clean and prepare raw review data for analysis.
* Apply NLP preprocessing techniques to traveler reviews.
* Analyze traveler sentiment using VADER sentiment analysis.
* Identify travel, destination, and review activity trends.
* Explore seasonal and time-based patterns.
* Generate meaningful insights from traveler behavior and review data.
* Prepare structured analytical datasets for downstream visualization and analytics.

---

## Dataset

This project uses the **515K Hotel Reviews Data in Europe** dataset from Kaggle.

**Dataset Source:**
https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe

### Dataset Information

| Stage                   |    Rows | Columns |
| ----------------------- | ------: | ------: |
| Original Dataset        | 515,738 |      17 |
| After Data Cleaning     | 515,212 |      17 |
| After NLP Preprocessing | 515,212 |      19 |

The dataset contains information including:

* Hotel Name
* Hotel Address
* Review Date
* Reviewer Nationality
* Positive Review
* Negative Review
* Reviewer Score
* Average Hotel Score
* Review Tags
* Geographic Location

The original and intermediate datasets are not included in the repository because of their large file sizes.

---

## Project Structure

```text
travel-sentiment-analytics/
│
├── data/
│   └── raw/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_preprocessing.ipynb
│   ├── 04_Exploratory_Data_Analysis.ipynb
│   ├── 05_Sentiment_Analysis.ipynb
│   └── 06_Trend_Analysis.ipynb
│
├── .gitignore
├── README.md
└── requirements.txt
```

Large cleaned, processed, and analysis-ready CSV files are excluded from GitHub because of their file sizes and are maintained locally for project development.

---

## Data Processing Workflow

```text
Raw Hotel Reviews Dataset
          │
          ▼
   Data Collection
          │
          ▼
    Data Cleaning
          │
          ▼
   Cleaned Review Data
          │
          ▼
   NLP Preprocessing
          │
          ▼
  Processed Review Data
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
   Analytical Insights
```

---

# Completed Work

## 1. Data Collection

* Selected the 515K Hotel Reviews Data in Europe dataset.
* Loaded and inspected the dataset using Python.
* Examined dataset dimensions and column information.
* Checked data types and missing values.

## 2. Data Cleaning

The following data cleaning operations were performed:

* Checked and removed duplicate records.
* Analyzed missing values.
* Converted `Review_Date` to datetime format.
* Converted `days_since_review` from text to numerical format.
* Created a combined `Review_Text` column using positive and negative reviews.
* Handled missing review text.
* Cleaned review text by:

  * Converting text to lowercase
  * Removing URLs
  * Removing HTML tags
  * Removing extra whitespace
  * Removing punctuation

After cleaning, the dataset contained **515,212 records**.

## 3. NLP Preprocessing

The cleaned review text was further processed using NLP techniques:

* Tokenization
* Stopword removal
* Preservation of important negation words such as `no`, `not`, `nor`, and `never`
* Lemmatization
* Creation of processed review text

A `Processed_Review` column was created to store the final preprocessed review text.

## 4. Exploratory Data Analysis

Exploratory analysis was performed to understand the structure and major patterns within the dataset.

Key areas analyzed include:

* Hotel and destination distribution
* Country and city-level review activity
* Reviewer nationality
* Reviewer scores
* Review dates and yearly trends
* Monthly review activity
* Trip types
* Travel-related patterns

### Key Dataset Findings

* **1,492 hotels** are represented in the dataset.
* Reviews cover **227 reviewer nationalities**.
* The dataset spans from **August 2015 to August 2017**.
* London has the highest number of reviews among the analyzed cities.
* Leisure travel represents the largest trip-type category.

## 5. Sentiment Analysis

VADER sentiment analysis was applied to the cleaned review text.

A total of **515,212 reviews** were analyzed.

### Sentiment Distribution

| Sentiment |     Reviews | Percentage |
| --------- | ----------: | ---------: |
| Positive  |     369,929 |     71.80% |
| Negative  |     108,653 |     21.09% |
| Neutral   |      36,630 |      7.11% |
| **Total** | **515,212** |   **100%** |

The results indicate that the majority of reviews express positive sentiment.

## 6. Travel Trend Analysis

Time-based and travel-related analysis was performed to identify patterns in review activity.

Key areas include:

* Yearly review trends
* Monthly review activity
* Destination-level activity
* Trip-type distribution
* Seasonal patterns
* Reviewer score patterns

### Key Trend Finding

The highest monthly review activity occurred in **August 2016**, with **27,252 reviews**.

### Trip Type Distribution

| Trip Type |     Reviews |
| --------- | ----------: |
| Leisure   |     417,355 |
| Business  |      82,853 |
| Unknown   |      15,004 |
| **Total** | **515,212** |

Leisure travel is the dominant trip type in the dataset.

---

## Project Progress

* [x] Data Collection
* [x] Data Cleaning
* [x] NLP Preprocessing
* [x] Exploratory Data Analysis
* [x] Sentiment Analysis
* [x] Travel Trend Analysis
* [x] Seasonal Pattern Analysis
* [x] Analytical Dataset Preparation

Further visualization and application development are being maintained separately from this repository.

---

## Technologies Used

### Data Analytics and NLP

* Python
* Pandas
* NumPy
* NLTK
* VADER Sentiment Analysis
* Jupyter Notebook

### Development and Version Control

* Visual Studio Code
* Git
* GitHub

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Krishnaaa0811/travel-sentiment-analytics.git
```

### 2. Navigate to the Project Directory

```bash
cd travel-sentiment-analytics
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Dataset Setup

The original dataset is not included in this repository because of its large file size.

Download the dataset from Kaggle and place the required dataset file inside:

```text
data/raw/
```

The dataset source is provided in the Dataset section above.

---

## Author

**Krishna Gondaliya**
