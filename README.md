# Game Analytics: Unlocking Tennis Data with SportRadar API

## 📌 Project Overview

This project focuses on collecting, storing, and analyzing tennis competition data using the **SportRadar API**. The data is stored in a relational **SQL database**, and a **Streamlit** application is developed to visualize trends, rankings, and competition details interactively.

## 🎯 Key Features

- **Event Exploration**: Navigate through competition hierarchies (e.g., ATP Vienna events).
- **Trend Analysis**: Visualize event distribution by type, gender, and level.
- **Performance Insights**: Analyze player participation in singles and doubles events.
- **Decision Support**: Provide data-driven insights for sports event management.

## 🛠️ Tech Stack

- **Languages**: Python
- **Database**: MySQL/PostgreSQL
- **Frontend**: Streamlit
- **API Integration**: SportRadar API

## 📂 Project Structure

```
|-- Game-Analytics-Tennis/
    |-- data/                # SQL Database & Sample Data
    |-- scripts/             # Python Scripts for Data Extraction & Transformation
    |-- analytics.py         # Streamlit Application
    |-- requirements.txt     # Project Dependencies
    |-- README.md            # Project Documentation
    |-- sql_queries.sql      # SQL Queries for Analysis
```

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/your-username/Game-Analytics-Tennis.git
cd Game-Analytics-Tennis
```

### 2️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Database

- Create a MySQL/PostgreSQL database.
- Execute the SQL schema in `sql_queries.sql`.

### 4️⃣ Configure API Access

- Sign up for **SportRadar API** at: [SportRadar Developer](https://developer.sportradar.com/)
- Generate an API key and update the script accordingly.

### 5️⃣ Run Data Collection Script

```sh
python scripts/data_extraction.py
```

### 6️⃣ Launch Streamlit App

```sh
streamlit run app.py
```

## 📊 SQL Queries & Insights

- List all competitions with category names.
- Count the number of competitions per category.
- Find all competitions of type 'doubles'.
- Get competitors ranked in the top 5.

Refer to `sql_queries.sql` for the complete list of queries.


## 🔗 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [SportRadar API Docs](https://developer.sportradar.com/)

---
