import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Excel AI Chat", layout="wide")

st.title("📊 Excel AI Multi-Sheet Summary Chatbot")

api_key = st.text_input("Enter OpenAI API Key (optional for AI answers)", type="password")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    excel_data = pd.ExcelFile(uploaded_file)
    sheet_names = excel_data.sheet_names

    st.success(f"Sheets detected: {sheet_names}")

    summaries = {}

    for sheet in sheet_names:
        df = pd.read_excel(excel_data, sheet_name=sheet)

        summaries[sheet] = {
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Column Names": list(df.columns),
            "Missing Values": df.isnull().sum().to_dict(),
            "Statistics": df.describe(include='all').fillna("").to_dict()
        }

    st.subheader("📋 Auto Generated Summary")
    st.json(summaries)

    question = st.text_input("Ask a question about your Excel data")

    if question and api_key:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional data analyst."},
                {"role": "user", "content": f"Data: {summaries}\n\nQuestion: {question}"}
            ]
        )

        st.write("### 🤖 AI Answer")
        st.write(response.choices[0].message.content)
