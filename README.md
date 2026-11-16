# 06_Social_Media_Analytics_Dashboard_with_Python_Scrap

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red.svg)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap)

## 📌 Project Overview
**06_Social_Media_Analytics_Dashboard_with_Python_Scrap** is a full-stack Python data intelligence application that ingests, cleans, classifies, and visualizes social media data across 5 major platforms: **Twitter/X, LinkedIn, Instagram, Reddit, and YouTube**.

Developed by **Rajneesh Chaubey** (B.Tech Information Technology, ABES Engineering College).

**Official GitHub Repository:**  
👉 **[https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap](https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap)**

---

## 🏗️ System Architecture

```text
[ Web Scraping Layer ]
  ├── BeautifulSoup4 + Requests (Static HTML)
  ├── Selenium WebDriver (Dynamic Feeds)
  └── PRAW API / Snscrape
           │
           ▼
[ NLP Preprocessing Pipeline (nlp_processor.py) ]
  ├── Regex Noise Removal (URLs, Emojis, Symbols)
  ├── Tokenization & Lowercasing
  └── VADER / Lexicon Polarity Scoring (-1.0 to +1.0)
           │
           ▼
[ Analytics & Feature Engineering ]
  ├── Engagement Rate: ((Likes + Comments + Shares) / Views) * 100
  ├── Sentiment Categorization (Positive / Neutral / Negative)
  └── Hashtags & Mentions Frequency Extraction
           │
           ▼
[ Interactive UI Dashboard (app.py) ]
  ├── KPI Metrics Scorecards
  ├── Plotly Interactive Charts (Donut, Bar, Time Series)
  └── Dynamic Platform & Date Filtered CSV Exporter
```

---

## 🚀 Quick Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap.git
cd 06_Social_Media_Analytics_Dashboard_with_Python_Scrap
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Data Scraper (Optional to regenerate data)
```bash
python scraper.py
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## 📁 Repository Structure
```text
06_Social_Media_Analytics_Dashboard_with_Python_Scrap/
├── app.py                                # Streamlit dashboard web application
├── scraper.py                            # Multi-platform Python scraping engine
├── nlp_processor.py                      # Text preprocessing & sentiment classification
├── requirements.txt                      # Project dependencies
├── dataset.csv                           # 500 records conforming to programme shape
├── data_dictionary.csv                   # Comprehensive 25-feature data dictionary
├── dataset_generation_prompt.docx        # Prompt engineering specification doc
├── project_brief.docx                    # Executive project brief with GitHub link
├── project_synopsis_template.docx        # Academic synopsis with architecture
└── README.md                             # Project documentation and setup guide
```
