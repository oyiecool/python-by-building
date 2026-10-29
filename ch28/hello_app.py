# hello_app.py
import streamlit as st

st.title("Loan calculator")
principal = st.number_input("Loan amount", min_value=0, value=1_500_000, step=50_000)
rate = st.slider("Annual interest rate (%)", 1.0, 15.0, 7.0, 0.25)
years = st.selectbox("Term (years)", [5, 10, 15, 20, 25, 30], index=3)

r, n = rate / 12 / 100, years * 12
monthly = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
st.metric("Monthly payment", f"{monthly:,.2f}")
st.write(f"Total interest over {years} years: **{monthly * n - principal:,.0f}**")
