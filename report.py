import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(df):

    file_name = "disaster_report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "NGO Disaster Report")

    c.setFont("Helvetica", 12)

    high = len(df[df["Priority"] == "HIGH"])
    medium = len(df[df["Priority"] == "MEDIUM"])
    low = len(df[df["Priority"] == "LOW"])

    c.drawString(50, 700, f"Total Locations Analysed: {len(df)}")
    c.drawString(50, 680, f"HIGH Priority Areas: {high}")
    c.drawString(50, 660, f"MEDIUM Priority Areas: {medium}")
    c.drawString(50, 640, f"LOW Priority Areas: {low}")

    y = 600
    c.drawString(50, y, "Top Crisis Locations:")
    y -= 20

    if "People_in_need" in df.columns:

        top = df.sort_values("People_in_need", ascending=False).head(10)

        for _, row in top.iterrows():

            place = row.get("PlaceName", "Unknown")
            people = row.get("People_in_need", "N/A")

            c.drawString(60, y, f"{place} - People in need: {people}")
            y -= 20

    c.save()

    return file_name


def app():

    st.title("📄 Disaster Analysis Report")

    if not os.path.exists("dataset.csv"):
        st.warning("Please upload dataset first")
        return

    df = pd.read_csv("dataset.csv")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Auto create priority if not trained
    if "Priority" not in df.columns:

        st.info("Priority not found. Generating predictions automatically...")

        def calc(row):

            people = row.get("People_in_need", 0)
            volunteers = row.get("Volunteers", 0)

            score = people - volunteers

            if score > 700:
                return "HIGH"
            elif score > 300:
                return "MEDIUM"
            else:
                return "LOW"

        df["Priority"] = df.apply(calc, axis=1)

    st.subheader("Priority Distribution")
    st.bar_chart(df["Priority"].value_counts())

    if "People_in_need" in df.columns:

        st.subheader("People in Need Distribution")
        st.line_chart(df["People_in_need"])

    st.subheader("Top Crisis Locations")

    if "People_in_need" in df.columns:

        top = df.sort_values("People_in_need", ascending=False).head(10)
        st.dataframe(top, use_container_width=True)

    if "Recommendation" in df.columns:

        st.subheader("NGO Recommendations")
        st.dataframe(df[["Priority", "Recommendation"]].head(10), use_container_width=True)

    st.subheader("Generate Disaster Report")

    if st.button("Generate PDF Report"):

        pdf_file = generate_pdf(df)

        with open(pdf_file, "rb") as f:

            st.download_button(
                "Download Report",
                f,
                file_name="Disaster_Report.pdf"
            )