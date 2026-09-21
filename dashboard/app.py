# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config (must be first Streamlit command)
st.set_page_config(page_title="Retail Store Sales Dashboard", layout="wide")

# Title
st.title("Retail Store Sales Dashboard")

# Load the cleaned dataset
df = pd.read_csv("data/cleaned_retail_sales.csv")

# Sidebar filters
st.sidebar.header("Filters")

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)
df = df[df['Category'].isin(selected_categories)]

selected_location = st.sidebar.multiselect(
    "Select Location",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)
df = df[df['Location'].isin(selected_location)]

# Key Business Metrics (KPI cards)
st.subheader("Key Business Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{df['Total Spent'].sum():,.0f}")
col2.metric("Total Transactions", len(df))
col3.metric("Avg Transaction Value", f"₹{df['Total Spent'].mean():.2f}")

st.divider()

# Prepare data for all charts
category_revenue = df.groupby('Category')['Total Spent'].sum().sort_values(ascending=False).reset_index()

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_revenue = df.groupby('Day of Week')['Total Spent'].sum().reindex(day_order).reset_index()

payment_counts = df['Payment Method'].value_counts().reset_index()
payment_counts.columns = ['Payment Method', 'Count']

top_items = df.groupby('Item')['Total Spent'].sum().sort_values(ascending=False).head(10).reset_index()

# Charts in a 2x2 grid layout
st.subheader("Sales Analysis")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    fig1 = px.bar(category_revenue, x='Category', y='Total Spent', title='Revenue by Category', color='Category')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    fig2 = px.bar(day_revenue, x='Day of Week', y='Total Spent', title='Revenue by Day of Week')
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig3 = px.pie(payment_counts, names='Payment Method', values='Count', title='Payment Method Distribution')
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    fig4 = px.bar(top_items, x='Item', y='Total Spent', title='Top 10 Items by Revenue', color='Item')
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Raw data sample (collapsible, at the bottom)
with st.expander("View Raw Data Sample"):
    st.write(f"Total rows: {df.shape[0]} | Total columns: {df.shape[1]}")
    st.dataframe(df.head())