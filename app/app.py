import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* ==========================================
   MAIN PAGE
   ========================================== */

.main {
    background-color: #0e1117;
}


/* ==========================================
   SIDEBAR
   ========================================== */

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}

/* Normal sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #111827 !important;
}


/* ==========================================
   DROPDOWN BOXES
   ========================================== */

/* The actual dropdown container */
section[data-testid="stSidebar"]
div[data-baseweb="select"]
> div {
    background-color: #111827 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}


/* EVERYTHING inside dropdown = WHITE */
section[data-testid="stSidebar"]
div[data-baseweb="select"]
* {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


/* Selected dropdown text */
section[data-testid="stSidebar"]
div[data-baseweb="select"]
div[role="button"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


/* Dropdown arrow */
section[data-testid="stSidebar"]
div[data-baseweb="select"]
svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}


/* ==========================================
   DROPDOWN MENU WHEN OPENED
   ========================================== */

div[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}


/* ==========================================
   DATE INPUT
   ========================================== */

section[data-testid="stSidebar"]
[data-testid="stDateInput"] input {
    background-color: #111827 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}


/* Date input text */
section[data-testid="stSidebar"]
[data-testid="stDateInput"] input[type="text"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


/* Calendar icon */
section[data-testid="stSidebar"]
[data-testid="stDateInput"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}


/* ==========================================
   KPI CARDS
   ========================================== */

.metric-card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #64748b !important;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a !important;
}


/* ==========================================
   DATA TABLE
   ========================================== */

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}


/* ==========================================
   MAIN HEADINGS
   ========================================== */

.main h1,
.main h2,
.main h3 {
    color: #ffffff !important;
}


/* ==========================================
   SELECT BOX BORDER
   ========================================== */

div[data-baseweb="select"] {
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD DATA
# ==========================================

sales_df = pd.read_csv(
    "data/cleaned_online_retail.csv"
)

sales_df["InvoiceDate"] = pd.to_datetime(
    sales_df["InvoiceDate"]
)


customer_df = pd.read_csv(
    "data/customer_segments.csv"
)


# ==========================================
# 4. TITLE
# ==========================================

st.title("📊 E-Commerce Customer Analytics")

st.markdown(
    """
    **Customer segmentation and purchase behavior analysis**
    
    This dashboard analyzes customer purchasing patterns,
    revenue trends, products, and customer segments using
    RFM analysis and KMeans clustering.
    """
)


# ==========================================
# 5. SIDEBAR
# ==========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Customer Analysis",
        "Product Analysis",
        "Segmentation",
        "Business Insights"
    ]
)


# ==========================================
# FILTERS
# ==========================================

st.sidebar.divider()

st.sidebar.subheader("🔎 Filters")


# ==========================================
# COUNTRY FILTER
# ==========================================

countries = ["All"] + sorted(
    sales_df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Country",
    countries
)


# ==========================================
# SEGMENT FILTER
# ==========================================

segment_names = {
    0: "Recent Customers",
    1: "At-Risk Customers",
    2: "High-Value Loyal Customers",
    3: "Regular Customers"
}

customer_df["Segment"] = (
    customer_df["Cluster"].map(segment_names)
)

segments = ["All"] + sorted(
    customer_df["Segment"].dropna().unique().tolist()
)

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segments
)


# ==========================================
# DATE FILTER
# ==========================================

st.sidebar.subheader("📅 Date Range")

min_date = sales_df["InvoiceDate"].min().date()
max_date = sales_df["InvoiceDate"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ==========================================
# CREATE FILTERED SALES DATA
# ==========================================

filtered_sales_df = sales_df.copy()


# Apply Country filter

if selected_country != "All":

    filtered_sales_df = filtered_sales_df[
        filtered_sales_df["Country"] == selected_country
    ]


# Apply Date filter

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_sales_df = filtered_sales_df[
        (filtered_sales_df["InvoiceDate"].dt.date >= start_date)
        &
        (filtered_sales_df["InvoiceDate"].dt.date <= end_date)
    ]


# ==========================================
# CREATE FILTERED CUSTOMER DATA
# ==========================================

if selected_segment != "All":

    filtered_customer_df = customer_df[
        customer_df["Segment"] == selected_segment
    ]

else:

    filtered_customer_df = customer_df.copy()

# ==========================================
# 6. DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    st.header("📊 Business Overview")

    # ==========================================
    # CALCULATE KPIs
    # ==========================================

    total_revenue = filtered_sales_df["TotalAmount"].sum()
    total_customers = filtered_sales_df["CustomerID"].nunique()
    total_orders = filtered_sales_df["InvoiceNo"].nunique()
    total_products = filtered_sales_df["StockCode"].nunique()


    # ==========================================
    # KPI CARDS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">💰 Total Revenue</div>
                <div class="metric-value">£{total_revenue:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">👥 Customers</div>
                <div class="metric-value">{total_customers:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🧾 Orders</div>
                <div class="metric-value">{total_orders:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">📦 Products</div>
                <div class="metric-value">{total_products:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------

    st.subheader("📈 Monthly Revenue")

    sales_df["Month"] = (
        sales_df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_revenue = (
    filtered_sales_df
    .groupby(
        filtered_sales_df["InvoiceDate"].dt.to_period("M")
    )["TotalAmount"]
    .sum()
    .reset_index()
)

    monthly_revenue["InvoiceDate"] = (
    monthly_revenue["InvoiceDate"]
    .astype(str)
)


    fig_monthly = px.line(
        monthly_revenue,
        x="InvoiceDate",
        y="TotalAmount",
        markers=True,
        title="Monthly Revenue Trend"
    )


    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified"
    )


    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


    # --------------------------------------
    # COUNTRY REVENUE
    # --------------------------------------

    st.subheader("🌍 Revenue by Country")


    country_revenue = (
    filtered_sales_df
    .groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


    fig_country = px.bar(
        country_revenue,
        x="Country",
        y="TotalAmount",
        title="Top 10 Countries by Revenue"
    )


    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


# ==========================================
# 7. CUSTOMER ANALYSIS
# ==========================================

elif page == "Customer Analysis":

    # Filter customers by selected segment
    if selected_segment != "All":
        filtered_customer_df = customer_df[
            customer_df["Segment"] == selected_segment
        ]
    else:
        filtered_customer_df = customer_df.copy()
    

    st.header("👥 Customer Analysis")


    # --------------------------------------
    # CUSTOMER METRICS
    # --------------------------------------

    avg_recency = filtered_customer_df["Recency"].mean()
    avg_frequency = filtered_customer_df["Frequency"].mean()
    avg_monetary = filtered_customer_df["Monetary"].mean()


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Recency",
            f"{avg_recency:.1f} days"
        )


    with col2:

        st.metric(
            "Average Orders",
            f"{avg_frequency:.1f}"
        )


    with col3:

        st.metric(
            "Average Customer Value",
            f"£{avg_monetary:,.0f}"
        )


    st.divider()


    # --------------------------------------
    # CUSTOMER TABLE
    # --------------------------------------

    st.subheader("Customer RFM Data")

    st.dataframe(
    filtered_customer_df[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary"
        ]
    ].head(100),
    use_container_width=True
)

# ==========================================
# PRODUCT ANALYSIS
# ==========================================

elif page == "Product Analysis":

    st.header("📦 Product Analysis")

    # Calculate product revenue using the selected country filter
    product_revenue = (
        filtered_sales_df
        .groupby("Description")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    # Product Revenue Chart
    fig_products = px.bar(
        product_revenue,
        x="TotalAmount",
        y="Description",
        orientation="h",
        title="Top 15 Products by Revenue",
        labels={
            "TotalAmount": "Revenue",
            "Description": "Product"
        }
    )

    fig_products.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # Product Revenue Table
    st.subheader("Top Products")

    st.dataframe(
        product_revenue,
        use_container_width=True
    )


# ==========================================
# 9. CUSTOMER SEGMENTATION
# ==========================================

# ==========================================
# SEGMENTATION
# ==========================================

elif page == "Segmentation":

    st.header("🎯 Customer Segmentation")

    st.write(
        "Customers are grouped using RFM analysis "
        "(Recency, Frequency, and Monetary Value)."
    )

    # ------------------------------------------
    # Segment Summary
    # ------------------------------------------

    segment_summary = (
        filtered_customer_df
        .groupby("Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .round(2)
        .reset_index()
    )

    # ------------------------------------------
    # Segment Count Chart
    # ------------------------------------------

    segment_counts = (
        filtered_customer_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = ["Segment", "Customers"]

    fig_segments = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        title="Customers by Segment",
        labels={
            "Segment": "Customer Segment",
            "Customers": "Number of Customers"
        }
    )

    st.plotly_chart(
        fig_segments,
        use_container_width=True
    )

    # ------------------------------------------
    # Segment Profile Table
    # ------------------------------------------

    st.subheader("📊 Segment Profile")

    st.dataframe(
        segment_summary,
        use_container_width=True
    )

    # ------------------------------------------
    # PCA Visualization
    # ------------------------------------------

    st.subheader("🔍 Customer Segments Visualization")

    if "PC1" in customer_df.columns and "PC2" in customer_df.columns:

        # Use the currently selected segment
        pca_df = filtered_customer_df.copy()

        fig_pca = px.scatter(
            pca_df,
            x="PC1",
            y="PC2",
            color="Segment",
            hover_data=[
                "CustomerID",
                "Recency",
                "Frequency",
                "Monetary"
            ],
            title="Customer Segments using PCA"
        )

        st.plotly_chart(
            fig_pca,
            use_container_width=True
        )

    else:

        st.warning(
            "PCA data is not available. "
            "Please run 06_pca_visualization.py first."
        )


# ==========================================
# BUSINESS INSIGHTS
# ==========================================

elif page == "Business Insights":

    st.header("💡 Business Insights")

    st.write(
        "Key findings from the e-commerce sales, RFM analysis, "
        "and customer segmentation."
    )


    # ==========================================
    # REVENUE INSIGHTS
    # ==========================================

    st.subheader("💰 Revenue Insights")

    st.markdown("""
    - The dataset generated approximately **£8.89 million in total revenue**.
    - Revenue increased strongly during **September, October, and November 2011**.
    - November 2011 recorded the highest monthly revenue in the dataset.
    - The **United Kingdom** contributed the majority of total revenue.
    """)


    # ==========================================
    # CUSTOMER INSIGHTS
    # ==========================================

    st.subheader("👥 Customer Insights")

    st.markdown("""
    - The dataset contains **4,338 unique customers**.
    - Customer purchasing behavior varies significantly in terms of recency,
      frequency, and monetary value.
    - RFM analysis helps identify customers who purchase frequently,
      customers who recently purchased, and customers who may require
      re-engagement.
    """)


    # ==========================================
    # CUSTOMER SEGMENTATION
    # ==========================================

    st.subheader("🎯 Customer Segmentation")

    st.markdown("""
    The K-Means clustering analysis identified four customer segments:

    **🟢 Recent Customers**
    
    Customers with relatively recent purchases but lower purchasing
    frequency and monetary value.

    **🔴 At-Risk Customers**
    
    Customers with high recency values, indicating that they have not
    purchased recently.

    **🟣 High-Value Loyal Customers**
    
    Customers with high purchasing frequency and substantially higher
    monetary contribution.

    **🔵 Regular Customers**
    
    Customers showing moderate purchasing activity and revenue contribution.
    """)


    # ==========================================
    # BUSINESS RECOMMENDATIONS
    # ==========================================

    st.subheader("📌 Business Recommendations")

    st.markdown("""
    **1. Retain high-value customers**
    
    Provide personalized offers, loyalty rewards, and targeted
    recommendations to customers with high purchase frequency and revenue.

    **2. Re-engage at-risk customers**
    
    Use targeted email campaigns, discounts, and personalized product
    recommendations to encourage customers who have not purchased recently.

    **3. Encourage recent customers to purchase again**
    
    Follow-up campaigns can help convert recent one-time buyers into
    repeat customers.

    **4. Increase regular customer value**
    
    Cross-selling and product recommendations can encourage regular
    customers to increase their order frequency and spending.

    **5. Monitor revenue trends**
    
    Monthly revenue analysis can help identify seasonal patterns and
    periods of increased customer demand.
    """)


    # ==========================================
    # PROJECT SUMMARY
    # ==========================================

    st.subheader("📊 Project Summary")

    st.info(
        "This project combines data cleaning, exploratory data analysis, "
        "RFM customer analysis, K-Means clustering, PCA visualization, "
        "and an interactive Streamlit dashboard to understand e-commerce "
        "customer behavior."
    )

# ==========================================
# 11. FOOTER
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "E-Commerce Customer Segmentation & Purchase Behavior Analysis"
)