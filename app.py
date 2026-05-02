import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🔐 AI JIT Access Decision Engine")

user = st.text_input("User Name")
role = st.selectbox("Role", ["user", "admin"])
last_login = st.number_input("Last Login (days ago)", 0, 365)
privilege = st.selectbox("Privilege Level", ["low", "high"])
request = st.text_input("Requested Access")

def calculate_risk(role, privilege, last_login):
    score = 0
    if privilege == "high":
        score += 40
    if role == "admin":
        score += 30
    if last_login > 90:
        score += 30
    return score

if st.button("Evaluate Access"):
    risk_score = calculate_risk(role, privilege, last_login)

    prompt = f"""
    Decide whether to APPROVE or DENY access.

    User: {user}
    Role: {role}
    Last Login: {last_login}
    Privilege: {privilege}
    Request: {request}
    Risk Score: {risk_score}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.write(response.choices[0].message.content)
    st.write("Risk Score:", risk_score)