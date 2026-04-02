import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Excel Summary Chatbot", layout="wide")

st.title("📊 Excel Summary Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Raw Data")
    st.dataframe(df)

    # -------------------------------
    # Sidebar Filters
    # -------------------------------
    st.sidebar.header("🔧 Filters")

    # ✅ Categorical filters (fixed warning)
    for col in df.select_dtypes(include=['object', 'string']).columns:
        unique_vals = df[col].dropna().unique().tolist()

        selected_vals = st.sidebar.multiselect(
            f"Select {col}",
            unique_vals,
            default=unique_vals
        )

        df = df[df[col].isin(selected_vals)]

    # ✅ Numeric filters (fixed slider crash)
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        min_val = float(df[col].min())
        max_val = float(df[col].max())

        # Handle constant columns
        if min_val == max_val:
            st.sidebar.write(f"ℹ️ {col}: constant value ({min_val})")
            continue

        selected_range = st.sidebar.slider(
            f"Range for {col}",
            min_val,
            max_val,
            (min_val, max_val)
        )

        df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

    # -------------------------------
    # KPI Section
    # -------------------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_cols) >= 1:
        col1.metric("Total Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Sum (First Numeric)", round(df[numeric_cols[0]].sum(), 2))

    # -------------------------------
    # Summary Stats
    # -------------------------------
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # -------------------------------
    # Charts
    # -------------------------------
    st.subheader("📊 Visualizations")

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select column for chart", numeric_cols)

        st.bar_chart(df[selected_col])
        st.line_chart(df[selected_col])

    # -------------------------------
    # Final Filtered Data
    # -------------------------------
    st.subheader("✅ Filtered Data")
    st.dataframe(df)

else:
    st.info("👆 Please upload an Excel file to begin.")