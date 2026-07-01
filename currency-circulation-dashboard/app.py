# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION

st.set_page_config(
    page_title="TZS Currency circulation Dashboard",
    page_icon="💰",
    layout="wide"
)

# CUSTOM STYLING

st.markdown("""
<style>

.stApp{
    background-color:#f4f7fc;
}

/* Remove extra spacing at top */
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}


h1{
    color:#0F172A;
    font-weight:700;
}

h2,h3{
    color:#1E3A8A;
}

[data-testid="stSidebar"]{
    background:#ffffff;
    border-right:1px solid #E5E7EB;
}
.kpi-card{

        background: linear-gradient(
            135deg,
            #38BDF8,
            #0EA5E9);

    color:white;

    border-radius:18px;

    padding:22px;

    text-align:center;

    box-shadow:
        0 10px 25px rgba(0,0,0,.15);

    transition:all .35s ease;

    cursor:pointer;

}


.kpi-card:hover{

    transform:
        translateY(-8px)
        scale(1.03);

    box-shadow:
        0 18px 35px rgba(0,0,0,.25);

}


.kpi-icon{

    font-size:38px;

    margin-bottom:10px;

}


.kpi-title{

    font-size:15px;

    font-weight:500;

    opacity:.9;

}


.kpi-value{

    font-size:34px;

    font-weight:bold;

    margin-top:12px;

}


[data-testid="stPlotlyChart"]{

    background:white;

    border-radius:15px;

    padding:12px;

    box-shadow:
        0 5px 18px rgba(0,0,0,.08);

}



.stSuccess{

    border-radius:12px;

}



.stInfo{

    border-radius:12px;

}


.stButton>button{

    border-radius:10px;

    background:#2563EB;

    color:white;

    border:none;

    transition:.3s;

}

.stButton>button:hover{

    background:#1E40AF;

}



[data-testid="stFileUploader"]{

    border-radius:12px;

    border:none;

    background:white;

    padding:10px;

}

</style>
""", unsafe_allow_html=True)

# TITLE

st.title("💰 Tanzanian Currency Circulation Analysis Dashboard")

st.write(
    "Upload a CSV or Excel dataset to analyze Tanzanian Shilling notes and coins circulation."
)

# FILE UPLOAD

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

# PROCESS DATA

if uploaded_file:

    try:

        # LOAD FILE

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Dataset loaded successfully!")

        # PREVIEW
        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        # DATASET INFO

        st.subheader("Dataset Information")

        c1, c2, c3 = st.columns(3)

        c1.metric("Rows", len(df))
        c2.metric("Columns", len(df.columns))
        c3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        # FILTERS

        st.sidebar.header("Dashboard Filters")

        selected_regions = st.sidebar.multiselect(
            "Select region",
            options=df["region"].unique(),
            default=df["region"].unique()
        )

        selected_months = st.sidebar.multiselect(
            "Select month",
            options=df["month"].unique(),
            default=df["month"].unique()
        )

        selected_denominations = st.sidebar.multiselect(
            "Select denomination",
            options=df["denomination"].unique(),
            default=df["denomination"].unique()
        )

        # FILTER DATA

        filtered = df[
            (df["region"].isin(selected_regions))
            &
            (df["month"].isin(selected_months))
            &
            (df["denomination"].isin(selected_denominations))
        ]

        # KPI CALCULATIONS

        total_issued = filtered["notes_issued"].sum()

        total_returned = filtered["notes_returned"].sum()

        net_circulation = filtered["net_circulation"].sum()

        return_rate = (
            total_returned / total_issued * 100
            if total_issued > 0 else 0
        )

        top_region = (
            filtered.groupby("region")["net_circulation"]
            .sum()
            .idxmax()
        )

        top_denomination = (
            filtered.groupby("denomination")["net_circulation"]
            .sum()
            .idxmax()
        )

        # KPI DISPLAY

        st.subheader("📊 KPI's")

        k1, k2, k3, k4, k5 = st.columns(5)

        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">💵</div>
                <div class="kpi-title">Total Notes Issued</div>
                <div class="kpi-value">{total_issued:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">💸</div>
                <div class="kpi-title">Notes Returned</div>
                <div class="kpi-value">{total_returned:,.0f}</div>
             </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-title">Net Circulation</div>
                <div class="kpi-value">{net_circulation:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📈</div>
                <div class="kpi-title">Return Rate</div>
                <div class="kpi-value">{return_rate:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with k5:
             st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📍</div>
                <div class="kpi-title">Top Region</div>
                <div class="kpi-value">{top_region}</div>
            </div>
            """, unsafe_allow_html=True)

        # CHARTS

        chart1, chart2 = st.columns(2)

        # BAR CHART

        region_summary = (
            filtered.groupby("region")["net_circulation"]
            .sum()
            .reset_index()
        )

        bar_fig = px.bar(
            region_summary,
            x="region",
            y="net_circulation",
            text_auto=True,
            title="net circulation by region"
        )

        chart1.plotly_chart(
            bar_fig,
            use_container_width=True
        )

        # PIE CHART

        denom_summary = (
            filtered.groupby("denomination")["net_circulation"]
            .sum()
            .reset_index()
        )

        pie_fig = px.pie(
            denom_summary,
            names="denomination",
            values="net_circulation",
            title="Distribution by denomination"
        )

        chart2.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        # TREND ANALYSIS

        st.subheader("monthly circulation Trend")

        trend = (
            filtered.groupby("month")["net_circulation"]
            .sum()
            .reset_index()
        )

        trend_fig = px.line(
            trend,
            x="month",
            y="net_circulation",
            markers=True,
            title="monthly net circulation Trend"
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

        # INSIGHTS

        st.subheader("Insights")

        st.info(
            f"""
            Highest circulation region: {top_region}

            Most circulated denomination: {top_denomination}

            Total circulation: {net_circulation:,.0f}

            Return rate: {return_rate:.2f}%
            """
        )

        # DETAILED DATA
        st.subheader("Detailed Dataset")

        st.dataframe(
            filtered,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Error processing dataset: {e}")

else:

    st.info(
        "👆 Upload your CSV or Excel dataset to begin analysis."
    )