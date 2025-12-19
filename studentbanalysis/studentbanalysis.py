# Import required libraries
import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("student_digital_behavior.csv")

# Display first 5 rows to verify data
print(df.head())

# -----------------------------
# Productivity Score Calculation
# -----------------------------

# Formula:
# (study_hours × 2) - (social_media_hours + entertainment_hours) + (sleep_hours × 0.5)

df["productivity_score"] = (
    (df["study_hours"] * 2)
    - (df["social_media_hours"] + df["entertainment_hours"])
    + (df["sleep_hours"] * 0.5)
)

# -----------------------------
# Burnout Risk Detection
# -----------------------------

def detect_burnout(row):
    risk_conditions = 0
    
    if row["sleep_hours"] < 6:
        risk_conditions += 1
    if row["study_hours"] > 8:
        risk_conditions += 1
    if row["breaks_count"] < 2:
        risk_conditions += 1
        
    if risk_conditions >= 2:
        return "High Risk"
    else:
        return "Low Risk"

# Apply burnout detection function
df["burnout_risk"] = df.apply(detect_burnout, axis=1)

# -----------------------------
# Productivity Level Classification
# -----------------------------

def productivity_level(score):
    if score >= 15:
        return "High"
    elif score >= 8:
        return "Medium"
    else:
        return "Low"

df["productivity_level"] = df["productivity_score"].apply(productivity_level)

# -----------------------------
# Basic Insights
# -----------------------------

average_productivity = df["productivity_score"].mean()
high_burnout_count = df[df["burnout_risk"] == "High Risk"].shape[0]

print("\nAverage Productivity Score:", round(average_productivity, 2))
print("Students with High Burnout Risk:", high_burnout_count)

# -----------------------------
# Save Processed Data
# -----------------------------

df.to_csv("processed_student_behavior.csv", index=False)

print("\nProcessed dataset saved successfully!")
