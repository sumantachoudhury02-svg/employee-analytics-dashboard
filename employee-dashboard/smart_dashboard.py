import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Smart Employee Dashboard", layout="wide")

st.title("Smart Employee Analytics Dashboard")

# Load Excel
df = pd.read_excel("5.4-Sales Data.xlsx")

# Sidebar Filter
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

position = st.sidebar.multiselect(
    "Position",
    df["Position"].unique(),
    default=df["Position"].unique()
)

df_filtered = df[
    (df["Gender"].isin(gender)) &
    (df["Position"].isin(position))
]

# KPI
total_emp = df_filtered["EmpID"].count()
avg_salary = round(df_filtered["Salary"].mean(),2)
max_salary = df_filtered["Salary"].max()

col1,col2,col3 = st.columns(3)

col1.metric("Total Employees", total_emp)
col2.metric("Average Salary", avg_salary)
col3.metric("Highest Salary", max_salary)

# Charts
col1,col2 = st.columns(2)

with col1:
    fig1 = px.pie(df_filtered,
                  names="Gender",
                  title="Gender Distribution")

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    salary_position = df_filtered.groupby("Position")["Salary"].mean().reset_index()

    fig2 = px.bar(
        salary_position,
        x="Position",
        y="Salary",
        title="Average Salary by Position"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Top Employees
st.subheader("Top 10 Highest Salary Employees")

top_emp = df_filtered.sort_values(by="Salary", ascending=False).head(10)

st.dataframe(top_emp)

# Automatic Insights
st.subheader("Key Insights")

highest_position = salary_position.sort_values(by="Salary", ascending=False).iloc[0]["Position"]

st.write(f"📊 Highest paying position: **{highest_position}**")
st.write(f"💰 Average company salary: **{avg_salary}**")
st.write(f"👥 Total employees analysed: **{total_emp}**")