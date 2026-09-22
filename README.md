# 🛒 Retail Store Sales Analysis

## 📋 Problem Statement
This project analyzes retail store sales data to identify revenue patterns, customer behavior, and business insights. The dataset contained ~12,500 transactions with real-world data quality issues (missing values, inconsistent records) that were systematically cleaned before analysis.

## 📊 Dataset
- **Source:** [Kaggle - Retail Store Sales (Dirty)](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)
- **Original size:** 12,575 transactions, 11 columns
- **After cleaning:** 11,971 transactions, 14 columns (with engineered features)
- **Categories:** Food, Beverages, Furniture, Patisserie, Butchers, Milk Products, Electric Household Essentials, Computers & Electric Accessories

## 🛠️ Approach
1. **Data Cleaning** — Missing value recovery using Price-Quantity-Total formula logic, missing Item recovery via Category-Price mapping, duplicate/invalid record checks, feature engineering (Day of Week, Month, Year)
2. **Exploratory Data Analysis** — 7 business questions answered with visualizations and written insights
3. **Interactive Dashboard** — Streamlit-based dashboard with category/location filters, live KPIs, and interactive Plotly charts

## 💡 Key Insights
- Revenue is fairly balanced across all 8 categories (₹1.8L–₹2.08L range) — no single category dominates
- Sales are consistent throughout the week, with Friday highest (₹2.33L) and Monday lowest (₹2.13L)
- Payment method usage is nearly evenly split: Cash (34%), Digital Wallet (33%), Credit Card (33%)
- January's higher revenue is driven by transaction volume (1,295 vs ~950 average), not higher average spending
- Best-selling items by quantity vs highest-revenue items are mostly different — high-volume items (beverages, milk) drive footfall, premium items (furniture) drive profit

## 🔗 Live Dashboard
🌐 [Click here to view the live dashboard](https://retail-sales-data-analysisgit-j8eggibxtssnn78mlhmcbj.streamlit.app/)

## 🖥️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas & NumPy | Data cleaning & manipulation |
| Matplotlib & Seaborn | Static visualizations (EDA) |
| Plotly | Interactive charts (Dashboard) |
| Streamlit | Dashboard framework |

## 📁 Project Structure

retail-sales-data-analysis/
├── data/
│ ├── retail_store_sales.csv (raw dataset)
│ └── cleaned_retail_sales.csv (cleaned dataset)
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ └── 02_eda_analysis.ipynb
├── dashboard/
│ └── app.py (Streamlit dashboard)
├── requirements.txt
└── README.md


## 🚀 How to Run Locally
```bash
git clone https://github.com/kri-ti-123/retail-sales-data-analysis.git
cd retail-sales-data-analysis
pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```