import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openai
openai.api_key = "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"


# Set page title
st.title("Employee Analysis Dashboard")

# Display key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Employees", "1500")
with col2:
    st.metric("Attrition Employees", "237")
with col3:
    st.metric("Retention Employees", "1263")

#############################################
# 1. Age Group Bar Chart
#############################################
# Load and process Age Group data
df_age = pd.read_csv("Age Group.csv", sep="\t", encoding="utf-16", header=None)
df_age.columns = ["Category", "Metric", "< 25", "25-34", "35-44", "45-55", "> 55"]

df_age = df_age[df_age["Metric"] == "Employee Count"].drop(columns=["Metric"])

df_age = df_age.set_index("Category").transpose().reset_index()
df_age.rename(columns={"index": "Age Group"}, inplace=True)

df_age["Attrition"] = df_age["Attrition"].astype(float).astype(int)
df_age["Retention"] = df_age["Retention"].astype(float).astype(int)

fig_age = px.bar(
    df_age,
    x="Age Group",
    y=["Retention", "Attrition"],
    title="Attrition vs Retention Across Age Groups",
    labels={"value": "Employee Count", "variable": "Category"},
    color_discrete_map={"Retention": "black", "Attrition": "tan"},
    barmode="stack")

st.plotly_chart(fig_age, use_container_width=True)

#############################################
# 2. Education Level Bar Chart
#############################################
data_edu = {
    "Education Level": [
        "Bachelor's Degree", "Bachelor's Degree",
        "Master's Degree", "Master's Degree",
        "Associates Degree", "Associates Degree",
        "High School", "High School",
        "Doctoral Degree", "Doctoral Degree"
    ],
    "Category": [
        "Attrition", "Retention",
        "Attrition", "Retention",
        "Attrition", "Retention",
        "Attrition", "Retention",
        "Attrition", "Retention"
    ],
    "Employee Count": [99, 473, 58, 340, 44, 238, 31, 139, 5, 43]
}
df_edu = pd.DataFrame(data_edu)
df_edu["Category"] = df_edu["Category"].str.strip()

df_pivot = df_edu.pivot(index="Education Level", columns="Category", values="Employee Count").reset_index()

fig_edu = go.Figure()
fig_edu.add_trace(go.Bar(
    x=df_pivot["Education Level"],
    y=df_pivot["Retention"],
    name="Retention",
    marker=dict(color="black")
))
fig_edu.add_trace(go.Bar(
    x=df_pivot["Education Level"],
    y=df_pivot["Attrition"],
    name="Attrition",
    marker=dict(color="tan")
))
fig_edu.update_layout(
    title="Education Level vs Attrition & Retention",
    barmode="group",
    xaxis_title="Education Level",
    yaxis_title="Employee Count",
    template="simple_white")

st.plotly_chart(fig_edu, use_container_width=True)

#############################################
# 3. Gender Donut Charts
#############################################
df_gender = pd.read_csv('Gender.csv', sep="\t", encoding="utf-16")
df_gender.columns = ["Gender", "Category", "% Attrition", "Attrition Count", "Employee Count"]

df_gender = df_gender.dropna(subset=["Employee Count"])
df_gender["Employee Count"] = df_gender["Employee Count"].astype(str).str.strip()
df_gender["Employee Count"] = df_gender["Employee Count"].astype(float).astype(int)

df_female = df_gender[df_gender["Gender"] == "Female"]
df_male = df_gender[df_gender["Gender"] == "Male"]

fig_female = go.Figure(go.Pie(
    labels=df_female["Category"],
    values=df_female["Employee Count"],
    hole=0.7,
    marker=dict(colors=["tan", "black"]),
    textinfo="none"
))
fig_female.update_layout(title_text="Female")

fig_male = go.Figure(go.Pie(
    labels=df_male["Category"],
    values=df_male["Employee Count"],
    hole=0.7,
    marker=dict(colors=["tan", "black"]),
    textinfo="none"
))
fig_male.update_layout(title_text="Male")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_female, use_container_width=True)
with col2:
    st.plotly_chart(fig_male, use_container_width=True)

#############################################
# 4. Employee Data Table (Job Title)
#############################################
data_job = [
    {"Job Title": "Data Visualization Technician", "Attrition": 62, "Retention": 197},
    {"Job Title": "Sales Executive", "Attrition": 57, "Retention": 269},
    {"Job Title": "Research Scientist", "Attrition": 47, "Retention": 245},
    {"Job Title": "Sales Representative", "Attrition": 33, "Retention": 50},
    {"Job Title": "Human Resources", "Attrition": 12, "Retention": 40},
]
df_job = pd.DataFrame(data_job)

fig_job = go.Figure(data=[go.Table(
    header=dict(
        values=["Job Title", "Attrition", "Retention"],
        align="left",
        font=dict(color="black", size=14),
        fill_color="#eee"
    ),
    cells=dict(
        values=[df_job["Job Title"], df_job["Attrition"], df_job["Retention"]],
        align="left",
        font=dict(color="black", size=12),
        fill_color=["white", "#f2f2f2"]
    )
)])
fig_job.update_layout(title="Employee Data")

st.plotly_chart(fig_job, use_container_width=True)

#############################################
# 5. User Query Input
#############################################
query = st.text_area("Ask a question about the data:", "", height=100)
if st.button("Submit") and query:
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": query}]
)

    st.write(response["choices"][0]["message"]["content"])
