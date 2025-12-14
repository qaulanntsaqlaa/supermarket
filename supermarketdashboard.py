import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supermarket Dashboard", layout="wide", page_icon="🛒")

# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>

    [data-testid="stAppViewContainer"] {
        background: #fff1f6;
    }

    .header {
        background: #ff6f9c;
        padding: 22px;
        border-radius: 16px;
        color: white;
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 25px;
        font-family: 'Georgia', serif;
        box-shadow: 0px 5px 14px rgba(0,0,0,0.1);
    }

    [data-testid="stSidebar"] {
        background: #ffe0eb;
        color: #6a2c3e;
        padding-top: 40px;
    }

    .member-card {
        background: white;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        color: #6a2c3e;
        text-align: center;
        font-weight: 600;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }

    .kpi {
        padding: 18px;
        border-radius: 14px;
        background: #ffffff;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
        border: 3px solid #ff6f9c;
    }

    .kpi-title {
        font-size: 15px;
        font-weight: 600;
        color: #6a2c3e;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 900;
        color: #6a2c3e;
    }

    .box {
        background: white;
        padding: 16px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
        border: 2px solid #ff6f9c;
    }

    /* Judul chart hitam pekat */
    .chart-title {
        font-size: 20px;
        font-weight: 700;
        color: black !important;
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("### 👥 Group 3 — Math Business")

    with st.expander("Show / Hide Members"):
        st.markdown('<div class="member-card">Qaulan Tsaqilaa</div>', unsafe_allow_html=True)
        st.markdown('<div class="member-card">Nanta Claudia</div>', unsafe_allow_html=True)
        st.markdown('<div class="member-card">Wulan Dwi Apriyanti</div>', unsafe_allow_html=True)
        st.markdown('<div class="member-card">Yustina Welli A Bohoji</div>', unsafe_allow_html=True)

    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])


# ============================================================
# LOAD DATA
# ============================================================

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_cols = ["Total", "Quantity", "cogs", "Rating"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # HEADER
    st.markdown('<div class="header">SUPERMARKET SALES DASHBOARD</div>', unsafe_allow_html=True)

    # ============================================================
    # KPI SECTION
    # ============================================================

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"<div class='kpi'><div class='kpi-title'>Total Sales</div>"
            f"<div class='kpi-value'>${df['Total'].sum():,.2f}</div></div>",
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            f"<div class='kpi'><div class='kpi-title'>Products Sold</div>"
            f"<div class='kpi-value'>{df['Quantity'].sum():,}</div></div>",
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            f"<div class='kpi'><div class='kpi-title'>Total COGS</div>"
            f"<div class='kpi-value'>${df['cogs'].sum():,.2f}</div></div>",
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            f"<div class='kpi'><div class='kpi-title'>Average Rating</div>"
            f"<div class='kpi-value'>{df['Rating'].mean():.2f}</div></div>",
            unsafe_allow_html=True
        )


    # ============================================================
    # LAYOUT 1 — MONTHLY SALES & PRODUCT SALES
    # ============================================================

    left, right = st.columns([1.2, 1.8])

    with left:
        st.markdown("<div class='box'><div class='chart-title'>📈 Monthly Sales</div>", unsafe_allow_html=True)
        df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
        monthly = df.groupby("Month")["Total"].sum().reset_index()
        fig1 = px.line(monthly, x="Month", y="Total", markers=True,
                       color_discrete_sequence=["#4cb944"])
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='box'><div class='chart-title'>🏆 Product Sales</div>", unsafe_allow_html=True)
        prod = df.groupby("Product line")["Total"].sum().reset_index()
        fig4 = px.bar(prod, x="Product line", y="Total",
                      color="Product line",
                      color_discrete_sequence=["#ff6f9c", "#7ed957", "#f14f7b", "#4cb944"])
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # LAYOUT 2 — RATING & PAYMENT
    # ============================================================

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='box'><div class='chart-title'>⭐ Rating by City</div>", unsafe_allow_html=True)
        city_rating = df.groupby("City")["Rating"].mean().reset_index()
        fig3 = px.bar(city_rating, x="Rating", y="City",
                      orientation="h",
                      color="City",
                      color_discrete_sequence=["#ff6f9c", "#7ed957", "#f14f7b"])
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='box'><div class='chart-title'>💳 Payment Methods</div>", unsafe_allow_html=True)
        fig2 = px.pie(df, names="Payment",
                      color_discrete_sequence=["#ff6f9c", "#f14f7b", "#7ed957"])
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # LAYOUT 3 — DATASET PREVIEW
    # ============================================================

    st.markdown("<div class='box'><div class='chart-title'>📄 Dataset Preview</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Please upload your Excel file to show the dashboard.")
