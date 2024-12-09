import streamlit as st
import pandas as pd
import plotly.express as px

# Setting page configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)

# @st.cache_data
# def load_data():
#     df_customers = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Customers.csv')
#     df_order_items = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_OrderItems.csv')
#     df_orders = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Orders.csv')
#     df_payments = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Payments.csv')
#     df_products = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Products.csv')
#     return df_customers, df_order_items, df_orders, df_payments, df_products

@st.cache_data
def load_data():
    processed_df_customers = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Customers.csv')
    processed_df_order_items = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_OrderItems.csv')
    processed_df_orders = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Orders.csv')
    processed_df_payments = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Payments.csv')
    processed_df_products = pd.read_csv('/Users/graceshan/Yushin-huishan-dashboard/Case Study/Ecommerce Order Dataset/processed_df_Products.csv')
    return processed_df_customers, processed_df_order_items, processed_df_orders, processed_df_payments, processed_df_products

# Load datasets
processed_df_customers, processed_df_order_items, processed_df_orders, processed_df_payments, processed_df_products = load_data()

# Merge datasets for a comprehensive view
processed_df_orders = processed_df_orders.merge(processed_df_customers, on="customer_id")
processed_df_order_items = processed_df_order_items.merge(processed_df_products, on="product_id")
processed_df_order_details = processed_df_orders.merge(processed_df_order_items, on="order_id")
processed_df_order_details = processed_df_order_details.merge(processed_df_payments, on="order_id")

# Sidebar Filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect(
    "Select Product Categories:",
    options=processed_df_order_details['product_category_name'].unique(),
    default=processed_df_order_details['product_category_name'].unique()
)
state_filter = st.sidebar.multiselect(
    "Select Customer States:",
    options=processed_df_order_details['customer_state'].unique(),
    default=processed_df_order_details['customer_state'].unique()
)
date_range = st.sidebar.date_input(
    "Select Order Date Range:",
    [pd.to_datetime(processed_df_order_details['order_purchase_timestamp'].min()),
     pd.to_datetime(processed_df_order_details['order_purchase_timestamp'].max())]
)

# Apply filters
filtered_data = processed_df_order_details[
    (processed_df_order_details['product_category_name'].isin(category_filter)) &
    (processed_df_order_details['customer_state'].isin(state_filter)) &
    (processed_df_orders['order_purchase_timestamp'] == pd.to_datetime(processed_df_orders['order_purchase_timestamp']))
]
# Page Title
st.title("📊 E-Commerce Dashboard")

# Key Metrics
st.subheader("Key Metrics")
total_revenue = filtered_data['payment_value'].sum()
total_orders = filtered_data['order_id'].nunique()
average_order_value = filtered_data['payment_value'].mean()
total_customers = filtered_data['customer_id'].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Total Orders", total_orders)
kpi3.metric("Average Order Value", f"${average_order_value:,.2f}")
kpi4.metric("Unique Customers", total_customers)

# Visualizations
st.subheader("Revenue by Product Category")
category_revenue = filtered_data.groupby('product_category_name')['payment_value'].sum().reset_index()
fig_category_revenue = px.bar(
    category_revenue,
    x="product_category_name",
    y="payment_value",
    title="Revenue by Product Category",
    labels={"payment_value": "Revenue", "product_category_name": "Category"},
    text_auto=True
)
st.plotly_chart(fig_category_revenue, use_container_width=True)

st.subheader("Orders by State")
state_orders = filtered_data.groupby('customer_state')['order_id'].nunique().reset_index()
fig_state_orders = px.bar(
    state_orders,
    x="customer_state",
    y="order_id",
    title="Orders by State",
    labels={"order_id": "Number of Orders", "customer_state": "State"},
    text_auto=True
)
st.plotly_chart(fig_state_orders, use_container_width=True)

st.subheader("Sales Trend Over Time")
filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
sales_trend = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum().reset_index()
sales_trend.columns = ['Month', 'Revenue']
sales_trend['Month'] = sales_trend['Month'].dt.to_timestamp()
fig_sales_trend = px.line(
    sales_trend,
    x="Month",
    y="Revenue",
    title="Monthly Sales Trend",
    labels={"Month": "Month", "Revenue": "Revenue"}
)
st.plotly_chart(fig_sales_trend, use_container_width=True)

# Data Table
st.subheader("Detailed Data Table")
st.dataframe(filtered_data)

# Download Filtered Data
st.sidebar.header("Download Data")
csv_data = filtered_data.to_csv(index=False)
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_ecommerce_data.csv",
    mime="text/csv"
)

# Footer
st.sidebar.info("Built with Streamlit | E-Commerce Dashboard 🛒 by Yu Shin & Hui Shan")