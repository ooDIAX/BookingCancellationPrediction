import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data Analysis")

if "df" in st.session_state:
    df = st.session_state.df

    st.write("Here is your uploaded CSV:")
    st.dataframe(df)

    if 'adr' in df.columns:
        st.subheader("ADR Column Distribution")

        fig, ax = plt.subplots()
        ax.hist(df['adr'], bins=30, color='blue', alpha=0.7, edgecolor='black')
        ax.set_xlabel("ADR")
        ax.set_ylabel("Frequency")
        ax.set_title("ADR Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'adr' column not found in the uploaded CSV.")

    if 'booking_changes' in df.columns:
        st.subheader("booking_changes Column Distribution")

        fig, ax = plt.subplots()
        ax.hist(df['booking_changes'], bins=30, color='blue', alpha=0.7, edgecolor='black')
        ax.set_xlabel("booking_changes")
        ax.set_ylabel("Frequency")
        ax.set_title("booking_changes Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'booking_changes' column not found in the uploaded CSV.")

    if 'lead_time' in df.columns:
        st.subheader("lead_time Column Distribution")

        fig, ax = plt.subplots()
        ax.hist(df['lead_time'], bins=30, color='blue', alpha=0.7, edgecolor='black')
        ax.set_xlabel("lead_time")
        ax.set_ylabel("Frequency")
        ax.set_title("lead_time Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'lead_time' column not found in the uploaded CSV.")

    if 'deposit_type' in df.columns:
        st.subheader("Deposit Type Distribution")

        deposit_counts = df['deposit_type'].value_counts()

        fig, ax = plt.subplots()
        ax.bar(deposit_counts.index, deposit_counts.values, color=['blue', 'orange'], alpha=0.7, edgecolor='black')

        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Refundable", "Non-Refundable"])
        ax.set_ylabel("Frequency")
        ax.set_title("Deposit Type Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'deposit_type' column not found in the uploaded CSV.")

    if 'previous_cancellations' in df.columns:
        st.subheader("Users who cancelled before")
        cancel_counts = (df["previous_cancellations"] >= 1).astype(int).value_counts()

        fig, ax = plt.subplots()
        ax.bar(cancel_counts.index, cancel_counts.values, color=['blue', 'orange'], alpha=0.7, edgecolor='black')

        ax.set_xticks([0, 1])
        ax.set_xticklabels(["No", "Yes"])
        ax.set_xlabel("Previous Cancellations")
        ax.set_ylabel("Frequency")
        ax.set_title("Previous Cancellations Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'deposit_type' column not found in the uploaded CSV.")


    if 'is_repeated_guest' in df.columns:
        st.subheader("Repeated guests")
        cancel_counts = (df["is_repeated_guest"] >= 1).astype(int).value_counts()

        fig, ax = plt.subplots()
        ax.bar(cancel_counts.index, cancel_counts.values, color=['blue', 'orange'], alpha=0.7, edgecolor='black')

        ax.set_xticks([0, 1])
        ax.set_xticklabels(["No", "Yes"])
        ax.set_xlabel("Repeated gest")
        ax.set_ylabel("is_repeated_guest")
        ax.set_title("is_repeated_guest Distribution")

        st.pyplot(fig)
    else:
        st.error("❌ 'deposit_type' column not found in the uploaded CSV.")

    
    st.subheader("Average ADR by Month")

    avg_adr = df.groupby("arrival_date_month")["adr"].mean()

    fig, ax = plt.subplots()
    ax.plot(avg_adr.index, avg_adr.values, marker="o", linestyle="-", color="green")

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Average ADR")
    ax.set_title("Average ADR by Month")

    st.pyplot(fig)


else:
    st.error("❌ No CSV data found. Please upload a file first.")
