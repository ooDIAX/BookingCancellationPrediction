import streamlit as st
import pandas as pd
from joblib import load
import matplotlib.pyplot as plt
import seaborn as sns

model_path = "app/models/random_forest_model.joblib" 
rf_model = load(model_path)

st.title("CSV Results")

if "df" in st.session_state:
    df = st.session_state.df
    st.write("Here is your uploaded CSV:")
    st.dataframe(df)

    required_features = [
        'lead_time', 'arrival_date_month', 'arrival_date_week_number',
        'arrival_date_day_of_month', 'stays_in_weekend_nights', 
        'stays_in_week_nights', 'adults', 'children', 'babies', 
        'meal', 'market_segment', 'distribution_channel', 
        'is_repeated_guest', 'previous_cancellations', 
        'previous_bookings_not_canceled', 'reserved_room_type', 
        'assigned_room_type', 'booking_changes', 'deposit_type', 
        'days_in_waiting_list', 'customer_type', 'adr', 
        'required_car_parking_spaces', 'total_of_special_requests'
    ]

    if all(feature in df.columns for feature in required_features):
        X_test = df[required_features]

        y_pred = rf_model.predict(X_test)
        predicted_1_ratio = y_pred.sum() / len(y_pred)

        df["y_pred"] = y_pred
        
        #avg diff
        st.subheader("Average Difference Between Rows")

        mean_1 = df[y_pred == 1].mean()
        mean_0 = df[y_pred == 0].mean()

        diff = mean_1 - mean_0

        if 'lead_time' in diff.index:
            diff = diff.drop('lead_time')

        fig, ax = plt.subplots(figsize=(10, 5))
        diff.plot(kind="bar", color="blue", alpha=0.7, edgecolor="black", ax=ax)

        ax.set_xlabel("Columns")
        ax.set_ylabel("Average Difference")
        ax.set_title("Average Difference")
        ax.axhline(0, color="black", linewidth=1)
        ax.set_xticklabels(diff.index, rotation=45, ha="right")

        st.pyplot(fig)

        #canceled before
        st.subheader("Only users who have cancelled before")
        filtered_df = df[df["previous_cancellations"] > 0]
        counts = filtered_df["y_pred"].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values, color=['blue', 'orange'], alpha=0.7, edgecolor='black')
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["pred_no_cancel", "pred_cancel"])
        ax.set_title("Distribution of previous_cancellations = 1 by y_pred")

        st.pyplot(fig)


        #repeated guest
        st.subheader("Cancel predictions for repeated guests")
        filtered_df = df[df["is_repeated_guest"] > 0]
        counts = filtered_df["y_pred"].value_counts().sort_index()
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values, color=['blue', 'orange'], alpha=0.7, edgecolor='black')
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["pred_no_cancel", "pred_cancel"])
        ax.set_title("Cancel prediction for repeated guests")

        st.pyplot(fig)

        #heatmap
        st.subheader("Feature Correlation Heatmap")

        correlation_matrix = df.corr()

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)

        ax.set_title("Feature Correlation Heatmap")

        st.pyplot(fig)

        #changes made
        st.subheader("Cancellation Rate by Changes Made")
        df["booking_changes_grouped"] = df["booking_changes"].apply(lambda x: x if x <= 5 else 6)

        cancel_rate = df.groupby("booking_changes_grouped")["y_pred"].apply(lambda x: (x > 0).mean())
        cancel_rate.index = cancel_rate.index.astype(str)
        cancel_rate.rename(index={"6": "6+"}, inplace=True)

        fig, ax = plt.subplots()
        ax.bar(cancel_rate.index, cancel_rate.values, color="blue", alpha=0.7, edgecolor="black")

        ax.set_xlabel("Number of Changes")
        ax.set_ylabel("Cancellation Rate")
        ax.set_title("Cancellation Rate by Changes Made")

        st.pyplot(fig)


        st.subheader("Overall Prediction Percentage")
        st.write(f"Predicted cancel rate: {predicted_1_ratio:.2%}")
        st.write(f"Can safely overbook: {predicted_1_ratio/6:.2%}")



    else:
        st.error("❌ The uploaded CSV must contain the required features for predictions.")

else:
    st.error("❌ No CSV data found. Please upload a file first.")
