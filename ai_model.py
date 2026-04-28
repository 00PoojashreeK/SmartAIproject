import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def app():
    st.header("NGO Intelligence: Priority & Gap Analysis")

    if not os.path.exists("dataset.csv"):
        st.warning("Please upload 'dataset.csv' first.")
        return

    # Load Data
    df = pd.read_csv("dataset.csv")
    original_columns = df.columns.tolist()
    
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Detect categories
    potential_targets = []
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype == 'string' or df[col].nunique() < 15:
            potential_targets.append(col)
    
    if not potential_targets:
        potential_targets = original_columns

    if st.button("Generate Detailed Priority Reports"):
        with st.spinner("Analyzing data patterns..."):
            
            analysis_df = df.copy()
            priority_matrix = pd.DataFrame(index=df.index)
            
            # --- PHASE 1: INDIVIDUAL COLUMN PRIORITIES ---
            st.subheader("1. Individual Column Priorities")
            
            for col in potential_targets:
                # Features are columns other than the current target
                X = df.drop(columns=[col])
                y = df[col].astype(str).fillna("None")
                
                # Preprocess Features
                X_encoded = pd.DataFrame()
                for x_col in X.columns:
                    if pd.api.types.is_numeric_dtype(X[x_col]):
                        X_encoded[x_col] = X[x_col].fillna(X[x_col].median())
                    else:
                        X_encoded[x_col] = LabelEncoder().fit_transform(X[x_col].astype(str).fillna('Missing'))
                
                # Preprocess Target
                le = LabelEncoder()
                y_encoded = le.fit_transform(y)
                
                # Train & Predict
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_encoded, y_encoded)
                preds = model.predict(X_encoded)
                pred_labels = le.inverse_transform(preds)
                
                # Store Prediction in analysis_df
                analysis_df[f"AI_Suggested_{col}"] = pred_labels
                
                # Compare Actual vs Predicted
                actual_val = analysis_df[col].astype(str).str.strip().str.lower()
                predicted_val = analysis_df[f"AI_Suggested_{col}"].astype(str).str.strip().str.lower()
                
                # Identify Gaps
                is_gap = (actual_val != predicted_val)
                priority_matrix[col] = is_gap.astype(int)

                # Individual Column Expander
                with st.expander(f"Priority Report: {col}"):
                    ind_report = pd.DataFrame({
                        "Current Value": df[col],
                        "AI Suggested": pred_labels,
                        "Status": is_gap.map({True: "🚨 High Priority", False: "✅ Optimal"})
                    })
                    st.dataframe(ind_report)

            # --- PHASE 2: OVERALL DATASET PRIORITY ---
            st.divider()
            st.subheader("2. Overall Dataset Priority (Global Analysis)")

            # Calculate the score
            analysis_df["Global_Gap_Score"] = priority_matrix.mean(axis=1)
            
            # Generate Gap Reasons
            reasons = []
            for idx, row in priority_matrix.iterrows():
                missing = [c for c in potential_targets if row[c] == 1]
                reasons.append(f"Lacking: {', '.join(missing)}" if missing else "No gaps detected")
            
            analysis_df["Gap_Reason"] = reasons

            def get_global_priority(score):
                if score > 0.5: return "Rank 1: CRITICAL"
                if score > 0.2: return "Rank 2: HIGH"
                if score > 0:   return "Rank 3: MODERATE"
                return "Rank 4: OPTIMAL"

            analysis_df["Overall_Priority"] = analysis_df["Global_Gap_Score"].apply(get_global_priority)

            # Display Stats
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Rows", len(df))
            m2.metric("Critical Gaps", len(analysis_df[analysis_df["Global_Gap_Score"] > 0.5]))
            m3.metric("Systemic Gap %", f"{analysis_df['Global_Gap_Score'].mean():.1%}")

            # Master Table Fix: Sort BEFORE filtering columns
            st.write("### Master Priority Table")
            
            # Sort the full dataframe first
            analysis_df = analysis_df.sort_values(by="Global_Gap_Score", ascending=False)
            
            # Select only the columns we want to see
            final_display_cols = original_columns + ["Overall_Priority", "Gap_Reason"]
            st.dataframe(analysis_df[final_display_cols])

            # Visualization
            st.subheader("Gap Breakdown by Category")
            gap_counts = priority_matrix.sum().sort_values(ascending=False)
            st.bar_chart(gap_counts)

if __name__ == "__main__":
    app()