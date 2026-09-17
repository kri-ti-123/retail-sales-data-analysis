import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION (Page ki setting)
# ==========================================
# Yeh line sabse pehle aani chahiye. Isse page ka title aur layout set hota hai.
st.set_page_config(page_title='Retail Sales Dashboard', layout='wide', page_icon='🛒')

# ==========================================
# DATA LOADING (Data ko load karna)
# ==========================================
# @st.cache_data ka matlab hai ki data ek baar load hoga aur memory me save ho jayega. 
# Isse app fast chalti hai.
@st.cache_data
def load_data():
    # Hum alag-alag jagah (paths) check karenge jahan file ho sakti hai
    paths_to_check = [
        "data/cleaned_retail_sales.csv",
        "../data/cleaned_retail_sales.csv",
        os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_retail_sales.csv"),
        os.path.join(os.path.dirname(__file__), "data", "cleaned_retail_sales.csv")
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Date column ko datetime format me convert kar rahe hain taaki filters kaam karein
            if 'Transaction Date' in df.columns:
                df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
            return df
            
    # Agar data nahi milta, toh error message ke liye empty dataframe return karte hain
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Data file nahi mili. Kripya check karein ki data/cleaned_retail_sales.csv file sahi jagah par hai.")
    st.stop() # App yahin ruk jayegi

# ==========================================
# HEADER SECTION (Title aur Description)
# ==========================================
st.title("🛒 Retail Sales Dashboard")
st.markdown("Yeh dashboard retail sales data ko analyze karne ke liye banaya gaya hai. Aap left side se filters apply kar sakte hain.")
st.divider() # Ek line draw karne ke liye

# ==========================================
# SIDEBAR FILTERS (Left side me filter options)
# ==========================================
st.sidebar.header("🔍 Filters")
st.sidebar.markdown("Apne hisaab se data filter karein:")

# 1. Category Filter (Multiple categories select karne ka option)
if 'Category' in df.columns:
    categories = df['Category'].dropna().unique()
    selected_categories = st.sidebar.multiselect("Select Category", categories, default=categories)
else:
    selected_categories = []

# 2. Payment Method Filter
if 'Payment Method' in df.columns:
    payments = df['Payment Method'].dropna().unique()
    selected_payments = st.sidebar.multiselect("Select Payment Method", payments, default=payments)
else:
    selected_payments = []

# 3. Location Filter
if 'Location' in df.columns:
    locations = df['Location'].dropna().unique()
    selected_locations = st.sidebar.multiselect("Select Location", locations, default=locations)
else:
    selected_locations = []

# 4. Date Range Filter
if 'Transaction Date' in df.columns:
    min_date = df['Transaction Date'].min()
    max_date = df['Transaction Date'].max()
    if pd.notna(min_date) and pd.notna(max_date):
        selected_dates = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    else:
        selected_dates = []
else:
    selected_dates = []

# 5. Discount Applied Filter (Radio buttons - sirf ek select ho sakta hai)
discount_options = ["All", "True", "False", "Unknown"]
selected_discount = st.sidebar.radio("Discount Applied", discount_options)

# ==========================================
# APPLYING FILTERS (Data ko filter karna)
# ==========================================
# Ab hum upar wale filters ke basis par apne data ko filter karenge
filtered_df = df.copy()

# Date filter apply karna
if len(selected_dates) == 2 and 'Transaction Date' in filtered_df.columns:
    start_date, end_date = selected_dates
    # Start date se end date ke beech ka data filter karein
    filtered_df = filtered_df[(filtered_df['Transaction Date'].dt.date >= start_date) & (filtered_df['Transaction Date'].dt.date <= end_date)]

# Multiselect filters apply karna
if 'Category' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
if 'Payment Method' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Payment Method'].isin(selected_payments)]
if 'Location' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

# Discount filter apply karna
if selected_discount != "All" and 'Discount Applied' in filtered_df.columns:
    if selected_discount == "True":
        filtered_df = filtered_df[filtered_df['Discount Applied'] == True]
    elif selected_discount == "False":
        filtered_df = filtered_df[filtered_df['Discount Applied'] == False]
    else:
        # Unknown ka matlab jahan data missing hai (NaN)
        filtered_df = filtered_df[filtered_df['Discount Applied'].isna()]

# Agar filter ke baad data empty hai, toh warning dikhayein
if filtered_df.empty:
    st.warning("Aapke filters ke hisaab se koi data nahi mila. Kripya filters change karein.")
    st.stop()

# ==========================================
# KPI CARDS (Key Performance Indicators)
# ==========================================
st.subheader("📊 Key Metrics")
# Hum page ko 4 columns me divide kar rahe hain
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = filtered_df['Total Spent'].sum() if 'Total Spent' in filtered_df.columns else 0
total_transactions = filtered_df['Transaction ID'].nunique() if 'Transaction ID' in filtered_df.columns else len(filtered_df)
avg_transaction_value = total_revenue / total_transactions if total_transactions > 0 else 0
unique_customers = filtered_df['Customer ID'].nunique() if 'Customer ID' in filtered_df.columns else 0

# st.metric() se hum numbers ko bade aur sundar tareeqe se dikhate hain
with kpi1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    
with kpi2:
    st.metric(label="Total Transactions", value=f"{total_transactions:,}")
    
with kpi3:
    st.metric(label="Avg Transaction Value", value=f"${avg_transaction_value:,.2f}")
    
with kpi4:
    st.metric(label="Unique Customers", value=f"{unique_customers:,}")

st.divider()

# ==========================================
# ROW 2 CHARTS (Revenue by Category & Monthly Trend)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue by Category")
    if 'Category' in filtered_df.columns and 'Total Spent' in filtered_df.columns:
        # Har category ka total revenue nikal rahe hain
        cat_revenue = filtered_df.groupby('Category')['Total Spent'].sum().reset_index()
        # Plotly Express (px) ka use karke horizontal bar chart banaya
        fig_cat = px.bar(cat_revenue, x='Total Spent', y='Category', orientation='h', 
                         color='Category', title="Category wise Revenue")
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Category or Total Spent data missing")

with col2:
    st.subheader("📅 Monthly Sales Trend")
    if 'Year' in filtered_df.columns and 'Month' in filtered_df.columns and 'Total Spent' in filtered_df.columns:
        # Month aur Year ke hisaab se data group kar rahe hain
        monthly_trend = filtered_df.groupby(['Year', 'Month'])['Total Spent'].sum().reset_index()
        # Month-Year ki string banayenge taaki chart me theek se dikhe
        monthly_trend['Month_Year'] = monthly_trend['Month'].astype(str) + "-" + monthly_trend['Year'].astype(str)
        # Line chart banaya
        fig_trend = px.line(monthly_trend, x='Month_Year', y='Total Spent', markers=True, 
                            title="Sales over Months")
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Month, Year or Total Spent data missing")

st.divider()

# ==========================================
# ROW 3 CHARTS (Payment Method & Day of Week)
# ==========================================
col3, col4 = st.columns(2)

with col3:
    st.subheader("💳 Payment Method Distribution")
    if 'Payment Method' in filtered_df.columns:
        # Kis payment method se kitne transactions hue
        payment_dist = filtered_df['Payment Method'].value_counts().reset_index()
        payment_dist.columns = ['Payment Method', 'Count']
        # Pie chart banaya
        fig_pie = px.pie(payment_dist, values='Count', names='Payment Method', hole=0.3, 
                         title="Payment Methods Used")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Payment Method data missing")

with col4:
    st.subheader("📅 Day of Week Sales Pattern")
    if 'Day of Week' in filtered_df.columns and 'Total Spent' in filtered_df.columns:
        # Kis din kitni sales hui
        day_sales = filtered_df.groupby('Day of Week')['Total Spent'].sum().reset_index()
        # Bar chart banaya
        fig_day = px.bar(day_sales, x='Day of Week', y='Total Spent', color='Day of Week', 
                         title="Sales Pattern by Day")
        st.plotly_chart(fig_day, use_container_width=True)
    else:
        st.info("Day of Week data missing")

st.divider()

# ==========================================
# ROW 4 CHARTS (Top 10 Items & Location-wise)
# ==========================================
col5, col6 = st.columns(2)

with col5:
    st.subheader("🏆 Top 10 Items by Revenue")
    if 'Item' in filtered_df.columns and 'Total Spent' in filtered_df.columns:
        # Sabse zyada revenue wale top 10 items
        top_items = filtered_df.groupby('Item')['Total Spent'].sum().nlargest(10).reset_index()
        fig_items = px.bar(top_items, x='Total Spent', y='Item', orientation='h', color='Item',
                           title="Top 10 High Revenue Items")
        # Sort order ulta kiya taaki highest upar aaye
        fig_items.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_items, use_container_width=True)
    else:
        st.info("Item data missing")

with col6:
    st.subheader("📍 Location-wise Revenue")
    if 'Location' in filtered_df.columns and 'Total Spent' in filtered_df.columns:
        location_sales = filtered_df.groupby('Location')['Total Spent'].sum().reset_index()
        # Donut chart (pie chart with hole)
        fig_loc = px.pie(location_sales, values='Total Spent', names='Location', hole=0.4,
                         title="Revenue by Location")
        st.plotly_chart(fig_loc, use_container_width=True)
    else:
        st.info("Location data missing")

st.divider()

# ==========================================
# DATA TABLE & DOWNLOAD (Data Table dikhana aur download option)
# ==========================================
st.subheader("📁 Filtered Data")
st.markdown("Yeh table upar select kiye gaye filters ke hisaab se data dikha rahi hai.")

# Dataframe display karein
st.dataframe(filtered_df, use_container_width=True)

# CSV me download karne ke liye data convert karein
@st.cache_data
def convert_df(df_to_convert):
    # Data ko utf-8 format me CSV me badal rahe hain
    return df_to_convert.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

# Download button
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_retail_sales.csv',
    mime='text/csv',
)
