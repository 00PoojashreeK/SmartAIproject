import streamlit as st
import pandas as pd
import os


def calculate_priority(row):

    score = 0

    if "People_in_need" in row:
        score += row["People_in_need"]

    if "Volunteers" in row:
        score -= row["Volunteers"]

    if "Food_need" in row:
        if str(row["Food_need"]).lower() == "high":
            score += 100
        elif str(row["Food_need"]).lower() == "medium":
            score += 50

    if "Medical_need" in row:
        if str(row["Medical_need"]).lower() == "high":
            score += 100
        elif str(row["Medical_need"]).lower() == "medium":
            score += 50

    if "NGO_available" in row:
        if row["NGO_available"] == 0:
            score += 200

    if score > 700:
        return "HIGH"
    elif score > 300:
        return "MEDIUM"
    else:
        return "LOW"


def recommendation(priority):

    if priority == "HIGH":
        return "Deploy NGOs immediately with food & medical support"

    elif priority == "MEDIUM":
        return "Send volunteers and monitor situation"

    else:
        return "Area stable. Monitor only"


def app():

    st.title("🧠 AI Disaster Resource Prediction")

    if not os.path.exists("dataset.csv"):
        st.warning("Please upload dataset first in Upload page")
        return

    df = pd.read_csv("dataset.csv")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # -------- Required columns --------
    required_cols = ["People_in_need", "Volunteers"]

    for col in required_cols:
        if col not in df.columns:
            st.error(f"Dataset must contain column: {col}")
            return

    # -------- Train AI Model --------
    if st.button("Train AI Model"):

        df["Priority"] = df.apply(calculate_priority, axis=1)
        df["Recommendation"] = df["Priority"].apply(recommendation)

        df.to_csv("dataset.csv", index=False)

        st.success("Model trained successfully and predictions saved!")

    # -------- Show predictions --------
    if "Priority" in df.columns:

        st.subheader("AI Predictions")
        st.dataframe(df, use_container_width=True)

        st.subheader("Priority Distribution")
        st.bar_chart(df["Priority"].value_counts())

    # -------- LOCATION SEARCH --------
    st.subheader("🔎 Search Location")

    place = st.text_input("Enter location name")

    if place:

        location_keywords = ["place", "location", "city", "district", "area"]

        location_col = None

        # detect location column automatically
        for col in df.columns:
            if any(key in col.lower() for key in location_keywords):
                location_col = col
                break

        # fallback to PlaceName
        if location_col is None and "PlaceName" in df.columns:
            location_col = "PlaceName"

        if location_col:

            result = df[
                df[location_col]
                .astype(str)
                .str.lower()
                .str.contains(place.lower())
            ]

            if len(result) > 0:

                st.success(f"Location found in column: {location_col}")
                st.dataframe(result, use_container_width=True)

            else:

                st.warning("Location not found")

        else:

            st.error("No location column detected in dataset")