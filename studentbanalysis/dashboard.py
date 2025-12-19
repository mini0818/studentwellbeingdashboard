import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Wellbeing & Productivity",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.markdown("<h1 style='text-align:center;'>🌱 Student Digital Wellbeing Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'></p>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("student_digital_behavior.csv")

# Productivity Score Formula
df["productivity_score"] = (
    (df["study_hours"] * 2)
    - (df["social_media_hours"] + df["entertainment_hours"])
    + (df["sleep_hours"] * 0.5)
)

# Burnout Detection
def detect_burnout(row):
    risk = 0
    if row["sleep_hours"] < 6:
        risk += 1
    if row["study_hours"] > 8:
        risk += 1
    if row["breaks_count"] < 2:
        risk += 1
    return "High Risk" if risk >= 2 else "Low Risk"

df["burnout_risk"] = df.apply(detect_burnout, axis=1)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🎛️ Filters")
day_filter = st.sidebar.selectbox("Day Type", ["All", "Weekday", "Weekend"])

if day_filter != "All":
    df = df[df["day_type"] == day_filter]

# -----------------------------
# KPI Section (With Units)
# -----------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "😊 Avg Productivity Score",
    f"{round(df['productivity_score'].mean(), 2)} pts"
)

k2.metric(
    "🔥 Students at Burnout Risk",
    f"{df[df['burnout_risk'] == 'High Risk'].shape[0]} students"
)

k3.metric(
    "👨‍🎓 Total Students",
    f"{df.shape[0]} students"
)

st.divider()

# -----------------------------
# Chart 1: Time Distribution
# -----------------------------
st.subheader("⏰ Average Daily Time Distribution (hrs/day)")

time_df = pd.DataFrame({
    "Activity": ["Study", "Social Media", "Entertainment"],
    "Average Hours (hrs/day)": [
        df["study_hours"].mean(),
        df["social_media_hours"].mean(),
        df["entertainment_hours"].mean()
    ]
})

fig1 = px.bar(
    time_df,
    x="Activity",
    y="Average Hours (hrs/day)",
    color="Activity",
    text_auto=".2f",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig1.update_layout(
    yaxis_title="Hours per Day (hrs/day)",
    xaxis_title="Activity Type"
)

st.plotly_chart(fig1, use_container_width=True)
st.caption("📌 Shows how students spend an average day in hours")

st.divider()

# -----------------------------
# Chart 2: Burnout Risk
# -----------------------------
st.subheader("🔥 Burnout Risk Distribution (Student Count)")

fig2 = px.pie(
    df,
    names="burnout_risk",
    hole=0.4,
    color="burnout_risk",
    color_discrete_map={
        "High Risk": "#ff6b6b",
        "Low Risk": "#51cf66"
    }
)
fig2.update_traces(
    hovertemplate="Burnout Status: %{label}<br>Students: %{value}"
)

st.plotly_chart(fig2, use_container_width=True)
st.caption("📌 Percentage and count of students under burnout risk")

st.divider()

# -----------------------------
# Chart 3: Productivity Distribution
# -----------------------------
st.subheader("📈 Productivity Score Distribution (Score Index)")

fig3 = px.histogram(
    df,
    x="productivity_score",
    nbins=10,
    labels={"productivity_score": "Productivity Score (Index)"},
    color_discrete_sequence=["#339af0"]
)
fig3.update_layout(
    xaxis_title="Productivity Score (unitless index)",
    yaxis_title="Number of Students"
)

st.plotly_chart(fig3, use_container_width=True)
st.caption("📌 Distribution of productivity scores across students")

st.divider()

# -----------------------------
# Chart 4: Sleep vs Academic Performance
# -----------------------------
st.subheader("😴 Sleep (hrs/day) vs Academic Score (Marks)")

fig4 = px.scatter(
    df,
    x="sleep_hours",
    y="academic_score",
    size="study_hours",
    color="burnout_risk",
    hover_data={
        "sleep_hours": ":.1f",
        "academic_score": True,
        "study_hours": True,
        "breaks_count": True
    },
    labels={
        "sleep_hours": "Sleep (hrs/day)",
        "academic_score": "Academic Score (out of 100)",
        "study_hours": "Study Hours (hrs/day)",
        "breaks_count": "Breaks per Day"
    },
    color_discrete_map={
        "High Risk": "#ff922b",
        "Low Risk": "#4dabf7"
    }
)

st.plotly_chart(fig4, use_container_width=True)
st.caption("📌 Bubble size represents study hours (hrs/day)")

st.divider()

# -----------------------------
# Recommendations (Clear Units)
# -----------------------------
st.subheader("💡 Actionable Insights")

if df["social_media_hours"].mean() > 3:
    st.warning("📵 Average social media usage exceeds **3 hrs/day** — reducing it may improve focus.")

if df["sleep_hours"].mean() < 7:
    st.warning("😴 Average sleep is below **7 hrs/day**, which increases burnout risk.")

st.success("☕ Maintaining balanced study hours with breaks improves long-term productivity.")
