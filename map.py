import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static  # Changed for better stability
import os
import random

def app():
    st.header("Map Visualization")

    # 1. Check if dataset exists
    if not os.path.exists("dataset.csv"):
        st.warning("Please upload 'dataset.csv' to the directory first.")
        return

    # 2. Load Data
    df = pd.read_csv("dataset.csv")

    # 3. Initialize Map (Centered on India)
    m = folium.Map(location=[20.59, 78.96], zoom_start=5)

    # 4. Plot Points
    if "Latitude" in df.columns and "Longitude" in df.columns:
        # Optimization: itertuples is much faster than standard indexing
        for row in df.itertuples():
            folium.CircleMarker(
                location=[row.Latitude, row.Longitude],
                radius=7,
                color="red",
                fill=True,
                fill_opacity=0.7,
                popup=f"Lat: {row.Latitude}, Lon: {row.Longitude}"
            ).add_to(m)
    else:
        st.info("Coordinates not found in CSV. Generating static random points for visualization.")
        
        # Set seed so points don't "jump" on every rerun
        random.seed(42)
        
        for i in range(len(df)):
            lat = 20 + random.uniform(-10, 10)
            lon = 78 + random.uniform(-10, 10)

            folium.CircleMarker(
                location=[lat, lon],
                radius=7,
                color="blue",
                fill=True,
                fill_opacity=0.6
            ).add_to(m)

    # 5. Render Map
    # folium_static is generally more stable than st_folium if you don't need 
    # to send data back from the map to Streamlit.
    folium_static(m, width=725, height=500)

if __name__ == "__main__":
    app()