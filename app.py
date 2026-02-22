import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Excel Visual AI Dashboard", layout="wide")

st.title("📊 Excel Visual Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    excel_data = pd.ExcelFile(uploaded_file)
    sheet = st.sidebar.selectbox("Select Sheet", excel_data.sheet_names)

    df = pd.read_excel(excel_data, sheet_name=sheet)

    st.sidebar.header("🔎 Filters")

    # Column selection
    columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select Columns", columns, default=columns)

    df = df[selected_columns]

    # Categorical Filters
    for col in df.select_dtypes(include=['object']).columns:
        unique_vals = df[col].dropna().unique()
        selected_vals = st.sidebar.multiselect(f"Filter {col}", unique_vals, default=unique_vals)
        df = df[df[col].isin(selected_vals)]

    # Numeric Filters
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        selected_range = st.sidebar.slider(f"Range for {col}", min_val, max_val, (min_val, max_val))
        df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

    # KPI Section
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))
    col2.metric("Total Columns", len(df.columns))

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 0:
        col3.metric("Average of First Numeric Column", round(df[numeric_cols[0]].mean(), 2))

    # Charts Section
    st.subheader("📊 Visual Summary")

    if len(numeric_cols) > 0:
        num_col = st.selectbox("Select Numeric Column for Chart", numeric_cols)
        cat_cols = df.select_dtypes(include=['object']).columns

        if len(cat_cols) > 0:
            cat_col = st.selectbox("Select Category Column", cat_cols)

            fig_bar = px.bar(df, x=cat_col, y=num_col, title="Bar Chart")
            st.plotly_chart(fig_bar, use_container_width=True)

            fig_pie = px.pie(df, names=cat_col, values=num_col, title="Pie Chart")
            st.plotly_chart(fig_pie, use_container_width=True)

        fig_hist = px.histogram(df, x=num_col, title="Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)

        fig_line = px.line(df, y=num_col, title="Line Trend")
        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📋 Filtered Data Preview")
    st.dataframe(df)
