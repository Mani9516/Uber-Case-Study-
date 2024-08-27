import gradio as gr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('/content/Uber Request Data.csv', parse_dates=[4, 5], dayfirst=True, na_values="NA")

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


def plot_frequency_of_requests_by_hour():
    plt.figure(figsize=(20, 10))
    df.groupby(['RequestHour', 'Status']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Frequency of Requests by Hour')
    plt.xlabel('Request Hour')
    plt.ylabel('Frequency')
    plt.legend(title='Status')
    plt.close()
    return plt.gcf()


def plot_problematic_types_of_requests():
    plt.figure(figsize=(6, 6))
    df.groupby(['Pickup point']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Types of Requests")
    plt.ylabel("")
    plt.close()
    return plt.gcf()


def plot_problematic_time_slots():
    plt.figure(figsize=(6, 6))
    df[df["Cab Availability"] == "Not Available"].groupby(['TimeSlot']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Time Slots")
    plt.ylabel("")
    plt.close()
    return plt.gcf()


def plot_demand_supply_gap_airport_city():
    plt.figure(figsize=(20, 10))
    df[df['Pickup point'] == "Airport"].groupby(['RequestHour', 'Status']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Demand-Supply Gap from Airport to City')
    plt.xlabel('Request Hour')
    plt.ylabel('Frequency')
    plt.legend(title='Status')
    plt.close()
    return plt.gcf()


def plot_time_slots_highest_gap():
    plt.figure(figsize=(20, 10))
    df.groupby(['TimeSlot', 'Cab Availability']).size().unstack().plot(kind='bar', stacked=True)
    plt.title('Time Slots Where Highest Gap Exists')
    plt.xlabel('Time Slot')
    plt.ylabel('Frequency')
    plt.legend(title='Cab Availability')
    plt.close()
    return plt.gcf()


def plot_requests_during_late_evening():
    plt.figure(figsize=(6, 6))
    df[df["TimeSlot"] == "Late Evening"].groupby(['Pickup point']).size().plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Problematic Types of Requests During Late Evening")
    plt.ylabel("")
    plt.close()
    return plt.gcf()


# Gradio Interface
interface = gr.Interface(
    title="Uber Request Data Analysis",
    description="Visualize the analysis of Uber request data.",
    inputs=[],
    outputs=gr.Plot(),
    live=False,
    examples=[],
    fn=[
        plot_frequency_of_requests_by_hour,
        plot_problematic_types_of_requests,
        plot_problematic_time_slots,
        plot_demand_supply_gap_airport_city,
        plot_time_slots_highest_gap,
        plot_requests_during_late_evening
    ]
)

interface.launch()
