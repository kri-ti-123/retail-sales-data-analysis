# 🛒 Retail Store Sales Analysis

## 📋 Problem Statement
This project analyzes retail store sales data to identify revenue patterns,
customer behavior, and business insights. The dataset contains ~12,500
transactions with intentional data quality issues (missing values, duplicates)
that were cleaned using systematic approaches.

## 📊 Dataset
- **Source:** [Kaggle - Retail Store Sales (Dirty)](https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning)
- **Size:** 12,575 transactions
- **Categories:** 8 product categories (Food, Beverages, Furniture, Patisserie, Butchers, Milk Products, Electric Household Essentials, Computers & Electric Accessories)
- **Timeline:** 2022-2025

## 🛠️ Approach
1. **Data Cleaning** — Missing value imputation using price-quantity-total formula logic, duplicate removal, feature engineering
2. **Exploratory Data Analysis** — 9 business questions answered with visualizations and insights
3. **Interactive Dashboard** — Streamlit-based dashboard with filters, KPIs, and interactive charts

## 💡 Key Insights
- *(Update these after running your EDA notebook)*
- Weekend sales show different patterns compared to weekday sales
- Category-wise revenue distribution reveals top-performing segments
- Payment method preferences vary across categories
- Discount transactions show distinct spending patterns

## 🔗 Live Dashboard
🌐 [Click here to view the live dashboard](https://your-app.streamlit.app)
*(Update this link after deployment)*

## 📸 Screenshots
*(Add chart screenshots from the images/ folder after running EDA)*

## 🖥️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas & NumPy | Data manipulation & cleaning |
| Matplotlib & Seaborn | Static visualizations |
| Plotly | Interactive charts |
| Streamlit | Dashboard framework |

## 📁 Project Structure
```
retail-sales-data-analysis/
├── data/
│   ├── retail_store_sales.csv          (raw dataset)
│   └── cleaned_retail_sales.csv        (cleaned dataset)
├── notebooks/
│   ├── 01_data_cleaning.py             (data cleaning code)
│   └── 02_eda_analysis.py              (EDA + charts)
├── dashboard/
│   └── app.py                          (Streamlit dashboard)
├── images/                             (chart screenshots)
├── requirements.txt
└── README.md
```

## 🚀 How to Run Locally
```bash
git clone https://github.com/your-username/retail-sales-data-analysis.git
cd retail-sales-data-analysis
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 👩‍💻 Author
**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
