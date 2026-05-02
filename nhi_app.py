import streamlit as st
import pandas as pd
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🤖 AI NHI Risk Analyzer")

uploaded_file = st.file_uploader("Upload NHI CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.write(df)

    # Risk scoring
    def calculate_risk(row):
        score = 0

        if row['privilege_level'] == 'high':
            score += 40
        if row['last_used_days'] > 90:
            score += 30
        if pd.isna(row['owner']):
            score += 30

        return score

    df['risk_score'] = df.apply(calculate_risk, axis=1)

    st.subheader("🚨 Risk Scores")
    st.write(df.sort_values(by="risk_score", ascending=False))

    # Send to AI
    data_str = df.to_json(orient="records")

    prompt = f"""
    Analyze these Non-Human Identities.

    Identify:
    - High-risk identities
    - Reasons for risk
    - Recommended actions

    Focus on:
    - Unused identities
    - Missing ownership
    - Excessive privilege

    Data:
    {data_str}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("🧠 AI Insights")
    st.write(response.choices[0].message.content)