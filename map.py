import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import os


def app():

    st.title("🗺 NGO Crisis Location Map")

    if not os.path.exists("dataset.csv"):
        st.warning("Please upload dataset first")
        return

    df = pd.read_csv("dataset.csv")

    # -------- Detect location column automatically --------
    location_keywords = ["place", "location", "city", "district", "area"]

    location_col = None

    for col in df.columns:

        col_lower = col.lower()

        for key in location_keywords:
            if key in col_lower:
                location_col = col
                break

        if location_col:
            break

    if location_col is None:
        st.error("No location column found in dataset")
        return

    # -------- Check coordinates --------
    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        st.error("Dataset must contain Latitude and Longitude columns")
        return

    # -------- Create Map --------
    m = folium.Map(location=[22.97, 78.65], zoom_start=5)

    marker_cluster = MarkerCluster().add_to(m)

    # -------- Marker Color --------
    def get_color(priority):

        if priority == "HIGH":
            return "red"
        elif priority == "MEDIUM":
            return "orange"
        else:
            return "green"

    # -------- Add Markers --------
    for _, row in df.iterrows():

        place = row.get(location_col, "Unknown")
        people = row.get("People_in_need", "N/A")
        volunteers = row.get("Volunteers", "N/A")
        priority = row.get("Priority", "LOW")

        tooltip_text = f"""
        Place: {place}
        People in Need: {people}
        Volunteers: {volunteers}
        Priority: {priority}
        """

        popup_text = f"""
        <b>Place:</b> {place}<br>
        <b>People in Need:</b> {people}<br>
        <b>Volunteers:</b> {volunteers}<br>
        <b>Priority:</b> {priority}
        """

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=7,
            color=get_color(priority),
            fill=True,
            fill_color=get_color(priority),
            fill_opacity=0.8,
            tooltip=tooltip_text,
            popup=popup_text
        ).add_to(marker_cluster)

    st.subheader("Disaster Locations")

    folium_static(m)