# Travel Sentiment & Trend Analytics Platform

AI-powered analytics platform that analyzes tourist reviews to surface sentiment,
trending destinations, seasonal patterns, budget signals, and safety concerns —
presented through an interactive dashboard.

> Status: Week 1-2 — dataset exploration in progress.

## Project structure

travel-sentiment-analytics/
├── data/
│   ├── raw/            Original downloaded dataset — never edited directly
│   ├── cleaned/         Cleaned, human-readable text after preprocessing
│   ├── processed/       Numeric/vectorized data, ML-ready
│   └── external/        Supplementary datasets
├── notebooks/           Numbered exploration notebooks (01_..., 02_..., etc.)
├── src/
│   ├── preprocessing/   Reusable text cleaning functions
│   └── utils/           Shared helper functions
└── requirements.txt

More folders (app/, models/, dashboard/, reports/) will be added as the
project reaches those phases.

## Setup

pip install -r requirements.txt

## Dataset

(To be filled in once dataset is finalized — source, download link, license.)