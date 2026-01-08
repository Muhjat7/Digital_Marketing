import streamlit as st
import pandas as pd

st.set_page_config(page_title="Digital Marketing Dashboard", layout="wide")
st.title("📊 Dashboard Analisis Digital Marketing")

# =========================
# Upload CSV
# =========================
uploaded_file = st.file_uploader(
    "Upload file CSV Digital Marketing",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Silakan upload file CSV untuk mulai analisis.")
    st.stop()

# =========================
# Load Data
# =========================
df = pd.read_csv(uploaded_file)

# =========================
# Validasi Kolom Wajib
# =========================
required_cols = {
    "date", "campaign_name", "impressions",
    "clicks", "cost", "conversions", "revenue"
}

if not required_cols.issubset(df.columns):
    st.error("❌ Format CSV tidak sesuai. Periksa nama kolom.")
    st.stop()

# =========================
# Hitung Metrik
# =========================
df["CTR"] = df["clicks"] / df["impressions"]
df["CPC"] = df["cost"] / df["clicks"]
df["CR"] = df["conversions"] / df["clicks"]
df["ROI"] = (df["revenue"] - df["cost"]) / df["cost"]

# =========================
# Agregasi per Campaign
# =========================
agg = df.groupby("campaign_name").agg({
    "impressions": "sum",
    "clicks": "sum",
    "cost": "sum",
    "conversions": "sum",
    "revenue": "sum"
}).reset_index()

agg["CTR"] = agg["clicks"] / agg["impressions"]
agg["CPC"] = agg["cost"] / agg["clicks"]
agg["CR"] = agg["conversions"] / agg["clicks"]
agg["ROI"] = (agg["revenue"] - agg["cost"]) / agg["cost"]

# =========================
# KPI Agregat
# =========================
st.subheader("📌 KPI Agregat Keseluruhan")

total_impressions = df["impressions"].sum()
total_clicks = df["clicks"].sum()
total_cost = df["cost"].sum()
total_conversions = df["conversions"].sum()
total_revenue = df["revenue"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Impressions", f"{total_impressions:,}")
col2.metric("Total Clicks", f"{total_clicks:,}")
col3.metric("CTR", f"{total_clicks/total_impressions:.2%}")
col4.metric("Conversion Rate", f"{total_conversions/total_clicks:.2%}")
col5.metric("ROI", f"{(total_revenue-total_cost)/total_cost:.2%}")

# =========================
# Tabel Agregat
# =========================
st.subheader("📈 Performa per Campaign")

st.dataframe(
    agg.style.format({
        "CTR": "{:.2%}",
        "CR": "{:.2%}",
        "ROI": "{:.2%}",
        "CPC": "Rp{:,.0f}",
        "cost": "Rp{:,.0f}",
        "revenue": "Rp{:,.0f}"
    })
)

# =========================
# Visualisasi
# =========================
# =========================
# Visualisasi Kinerja (CTR & ROI)
# =========================
st.subheader("📊 Visualisasi Kinerja")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**CTR per Campaign**")
    ctr_chart = agg.set_index("campaign_name")[["CTR"]]
    st.bar_chart(ctr_chart)

with col2:
    st.markdown("**ROI per Campaign**")
    roi_chart = agg.set_index("campaign_name")[["ROI"]]
    st.bar_chart(roi_chart)