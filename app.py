import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Summary Dashboard", layout="wide")

st.title("📊 Excel Summary Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel
        df = pd.read_excel(uploaded_file)

        # Remove unwanted index columns like "Unnamed: 0"
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        st.subheader("🔍 Raw Data")
        st.dataframe(df)

        # Check if dataframe is empty
        if df.empty:
            st.error("❌ Uploaded file has no data. Please upload a valid Excel file.")
        else:
            st.subheader("📌 Key Metrics")
            col1, col2, col3 = st.columns(3)

            col1.metric("Total Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])

            # First numeric column sum
            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:
                col3.metric("Sum (First Numeric)", float(df[numeric_cols[0]].sum()))
            else:
                col3.metric("Sum (First Numeric)", "N/A")

            # Summary stats
            st.subheader("📈 Summary Statistics")
            st.write(df.describe())

            # Visualization
            st.subheader("📊 Visualizations")

            if len(numeric_cols) > 0:
                selected_col = st.selectbox(
                    "Select column for chart",
                    numeric_cols
                )

                if selected_col:
                    st.bar_chart(df[selected_col])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

else:
    st.info("📂 Please upload an Excel file to begin.")