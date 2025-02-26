import streamlit as st
import pandas as pd
import io
from joblib import load


st.title("CSV Upload")

sample_csv_path = "app/data/sample_data.csv"

sample_df = pd.read_csv(sample_csv_path)
sample_csv = io.BytesIO()
sample_df.to_csv(sample_csv, index=False)
sample_csv.seek(0)

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

required_columns = {
    'lead_time', 'arrival_date_month', 'arrival_date_week_number', 
    'arrival_date_day_of_month', 'stays_in_weekend_nights', 
    'stays_in_week_nights', 'adults', 'children', 'babies', 
    'meal', 'market_segment', 'distribution_channel', 
    'is_repeated_guest', 'previous_cancellations', 
    'previous_bookings_not_canceled', 'reserved_room_type', 
    'assigned_room_type', 'booking_changes', 'deposit_type', 
    'days_in_waiting_list', 'customer_type', 'adr', 
    'required_car_parking_spaces', 'total_of_special_requests'
}

if "validated" not in st.session_state:
    st.session_state.validated = False

if st.button("Submit"):
    if uploaded_file is None:
        st.error("❌ Please upload a CSV file before submitting.")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            
            if not required_columns.issubset(df.columns):
                st.error("❌ Invalid CSV: Missing required columns.")
            elif df.isnull().values.any():
                st.error("❌ Invalid CSV: Contains empty values.")
            else:
                st.session_state.df = df
                st.session_state.validated = True
                st.switch_page("pages/result.py")

        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")

st.subheader("Download Sample CSV")
st.download_button(
    label="Download Sample CSV",
    data=sample_csv,
    file_name="sample.csv",
    mime="text/csv"
)
