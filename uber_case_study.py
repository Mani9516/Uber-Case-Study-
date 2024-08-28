import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('Uber Request Data.csv', parse_dates=[4, 5], dayfirst=True, na_values="NA")

# Manually convert 'Request timestamp' and 'Drop timestamp' to datetime
df['Request timestamp'] = pd.to_datetime(df['Request timestamp'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
df['Drop timestamp'] = pd.to_datetime(df['Drop timestamp'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

# Extract hour from the Request timestamp
df["RequestHour"] = df["Request timestamp"].dt.hour

# Separate 5 different time slots
df["TimeSlot"] = df["RequestHour"].apply(
    lambda x: "Dawn" if x <= 4 else ("Early Morning" if x <= 9 else
    ("Noon" if x <= 16 else ("Late Evening" if x <= 21 else "Night"))))

# Distinguish Supply-Demand Gap
df["Cab Availability"] = df["Status"].apply(lambda x: "Available" if x == "Trip Completed" else "Not Available")

# Function to plot Frequency of Requests by Hour
def plot_frequency_of_requests_by_hour():
    plt.figure(figsize=(20, 10))
    df.groupby(['RequestHour', 'Status']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Frequency of Requests by Hour')
    plt.xlabel('Request Hour')
    plt.ylabel('Frequency')
    plt.legend(title='Status')
    st.pyplot(plt.gcf())

# Function to plot Problematic Types of Requests
def plot_problematic_types_of_requests():
    plt.figure(figsize=(6, 6))
    df.groupby(['Pickup point']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Types of Requests")
    plt.ylabel("")
    st.pyplot(plt.gcf())

# Function to plot Problematic Time Slots
def plot_problematic_time_slots():
    plt.figure(figsize=(6, 6))
    df[df["Cab Availability"] == "Not Available"].groupby(['TimeSlot']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Time Slots")
    plt.ylabel("")
    st.pyplot(plt.gcf())

# Function to plot Demand-Supply Gap from Airport to City
def plot_demand_supply_gap_airport_city():
    plt.figure(figsize=(20, 10))
    df[df['Pickup point'] == "Airport"].groupby(['RequestHour', 'Status']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Demand-Supply Gap from Airport to City')
    plt.xlabel('Request Hour')
    plt.ylabel('Frequency')
    plt.legend(title='Status')
    st.pyplot(plt.gcf())

# Function to plot Time Slots Where Highest Gap Exists
def plot_time_slots_highest_gap():
    plt.figure(figsize=(20, 10))
    df.groupby(['TimeSlot', 'Cab Availability']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Time Slots Where Highest Gap Exists')
    plt.xlabel('Time Slot')
    plt.ylabel('Frequency')
    plt.legend(title='Cab Availability')
    st.pyplot(plt.gcf())

# Function to plot Problematic Types of Requests During Late Evening
def plot_requests_during_late_evening():
    plt.figure(figsize=(6, 6))
    df[df["TimeSlot"] == "Late Evening"].groupby(['Pickup point']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Types of Requests During Late Evening")
    plt.ylabel("")
    st.pyplot(plt.gcf())

# Streamlit Interface
st.title("Uber Request Data Analysis")
st.write("Visualize the analysis of Uber request data.")

# Select the type of analysis to perform
analysis_type = st.sidebar.selectbox(
    "Choose the analysis you want to see:",
    [
        "Frequency of Requests by Hour",
        "Problematic Types of Requests",
        "Problematic Time Slots",
        "Demand-Supply Gap from Airport to City",
        "Time Slots Where Highest Gap Exists",
        "Problematic Types of Requests During Late Evening"
    ]
)

# Display the selected analysis
if analysis_type == "Frequency of Requests by Hour":
    plot_frequency_of_requests_by_hour()
elif analysis_type == "Problematic Types of Requests":
    plot_problematic_types_of_requests()
elif analysis_type == "Problematic Time Slots":
    plot_problematic_time_slots()
elif analysis_type == "Demand-Supply Gap from Airport to City":
    plot_demand_supply_gap_airport_city()
elif analysis_type == "Time Slots Where Highest Gap Exists":
    plot_time_slots_highest_gap()
elif analysis_type == "Problematic Types of Requests During Late Evening":
    plot_requests_during_late_evening()
