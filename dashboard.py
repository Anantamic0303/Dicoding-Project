import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

st.header('Dicoding Final Project :sparkles:')

st.subheader('Project Overview: Bike Sharing Datasets')
with st.expander("**What is bike sharing system?**"):
    st.write("""
   Bike sharing systems are a new generation of traditional bike rentals where the entire process—from membership to rental and return—has become automatic. Through these systems, users can easily rent a bike from a specific location and return it to another. Currently, there are over 500 bike-sharing programs around the world, comprising more than 500,000 bicycles. These systems have gained significant interest due to their crucial roles in traffic management, environmental impact, and public health.
    """)

st.subheader('Problem question 1: How do user patterns differ by time of day for weekdays and weekends for both registered and casual user?')

all_df = pd.read_csv("all_data.csv")

# Define the day_df DataFrame
day_df = all_df  # Adjust as necessary to get your day_df

# Calculate the means for weekdays and weekends
mean_weekdays = day_df[day_df['weekday'] < 5].groupby('hr').agg({'casual': 'mean', 'registered': 'mean'})
mean_weekends = day_df[day_df['weekday'] >= 5].groupby('hr').agg({'casual': 'mean', 'registered': 'mean'})

# Calculate means for casual and registered users by weekday
weekday_means = day_df.groupby('weekday').agg({
    'casual': 'mean',
    'registered': 'mean'
})

# Create a bar chart to compare casual and registered users
plt.figure(figsize=(10, 6))
weekday_means.plot(kind='bar', color=['grey', '#00674F'], width=0.7)

# Add labels and title
plt.title('Mean Bike-Sharing Usage: Casual vs Registered Users', fontsize=10)
plt.xlabel('Day', fontsize=12)
plt.ylabel('Mean Count', fontsize=12)
plt.xticks(ticks=range(7), labels=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], rotation=0)

# Adjust legend position and size
plt.legend(labels=['Casual Users', 'Registered Users'], fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))

# Annotate the bar chart with mean values for casual and registered users
for i in range(len(weekday_means)):
    plt.text(i - 0.15, weekday_means['casual'][i] + 5, f"{weekday_means['casual'][i]:.0f}", 
             color='black', ha='center', fontsize=9)  # Smaller font size for casual bars
    plt.text(i + 0.15, weekday_means['registered'][i] + 5, f"{weekday_means['registered'][i]:.0f}", 
             color='black', ha='center', fontsize=9)  # Smaller font size for registered bars

# Show the plot in Streamlit
st.pyplot(plt)
plt.tight_layout()
plt.show()

# Create an expander for additional information
with st.expander("**Additional Information**"):
    st.write("""
    From the chart, we can see that casual users mostly use bike-sharing services during the weekend. Meanwhile, registered users show relatively stable usage throughout the week, except for a little drop on Sunday.
    """)

# Create a line chart for weekdays
plt.figure(figsize=(12, 6))

# Plot weekdays
sns.lineplot(data=mean_weekdays, x=mean_weekdays.index, y='casual', label='Casual Users (Weekdays)', color='gray', marker='o')
sns.lineplot(data=mean_weekdays, x=mean_weekdays.index, y='registered', label='Registered Users (Weekdays)', color='#00674F', marker='o')

# Add labels and title for weekdays
plt.title('Mean Bike Sharing Usage by Hour (Weekdays)', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Mean Count', fontsize=12)
plt.xticks(ticks=range(24), labels=range(24))
plt.grid(False)

# Adjust legend position and size
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, frameon=False)

# Show the plot for weekdays in Streamlit
plt.tight_layout()
st.pyplot(plt)

# Create a line chart for weekends
plt.figure(figsize=(12, 6))

# Plot weekends
sns.lineplot(data=mean_weekends, x=mean_weekends.index, y='casual', label='Casual Users (Weekends)', color='gray', marker='o')
sns.lineplot(data=mean_weekends, x=mean_weekends.index, y='registered', label='Registered Users (Weekends)', color='#00674F', marker='o')

# Add labels and title for weekends
plt.title('Mean Bike Sharing Usage by Hour (Weekends)', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Mean Count', fontsize=12)
plt.xticks(ticks=range(24), labels=range(24))
plt.grid(False)

# Adjust legend
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

# Show the plot for weekends
plt.tight_layout()
st.pyplot(plt)

# Create an expander for additional information
with st.expander("**Additional Information**"):
    st.write("""
    It can be seen that for the first question, casual users are more likely to use bike-sharing on weekends or holidays, while registered users tend to have stable usage but show a slight decline on weekends. In terms of time, during weekdays, casual users are more active during the day, whereas registered users are active in the morning and evening. This can serve as a basis for strategic actions by the company, such as implementing dynamic pricing, so that higher prices can be charged during peak hours to maintain bike availability.
    """)





#Problem question 2
st.subheader('Problem Question 2: How does seasonality affect bike sharing usage?')
seasonal_counts = day_df.groupby('season')['cnt'].sum()

# Create a bar chart for seasonal counts across all data
plt.figure(figsize=(10, 6))
bars_overall = plt.bar(seasonal_counts.index, seasonal_counts.values, color='#00674F', alpha=0.8, width=0.6)

# Adding data labels
for bar in bars_overall:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=10)

# Set the title and labels for overall data
plt.title('Total Bike Sharing Count by Season (2011-2012)', fontsize=18, weight='bold')
plt.xlabel('Season', fontsize=14)
plt.ylabel('Total Count', fontsize=14)
plt.xticks(ticks=seasonal_counts.index, labels=['Spring', 'Summer', 'Fall', 'Winter'], fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Use Streamlit to display the plot
st.pyplot(plt)

# Clear the figure to prevent overlap with future plots
plt.clf()

# Create an expander for additional information
with st.expander("**Additional Information**"):
    st.write("""
    Seasonality plays a crucial role in bike sharing usage. The data indicates that users are more inclined to utilize bike-sharing services during the warmer months (summer and fall), while spring experiences lower engagement and winter sees a moderate level of usage
    """)
