import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
# Make sure 'hotel_bookings.csv' is in the same folder as this script
try:
    df = pd.read_csv('hotel_bookings.csv')
    print("✅ Dataset loaded successfully!\n")
except FileNotFoundError:
    print("❌ Error: 'hotel_bookings.csv' not found. Please make sure the file is in the correct directory.")
    exit()

# Set the style for the plots
sns.set_style("whitegrid")

# ==============================================================================
# SOLUTIONS TO INITIAL QUESTIONS
# ==============================================================================

## Q1: Calculate booking counts by hotel type.
print("## Q1: Booking Counts by Hotel Type\n")
hotel_counts = df['hotel'].value_counts()
print(hotel_counts)
print("\n-------------------------------------------------\n")

## Q2: Group by arrival month to identify high demand periods.
print("## Q2: High Demand Periods by Month\n")
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
df['arrival_date_month_sorted'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)
monthly_demand = df['arrival_date_month_sorted'].value_counts().sort_index()
print("Booking counts per month (sorted chronologically):\n")
print(monthly_demand)
highest_demand_month = monthly_demand.idxmax()
print(f"\n💡 The month with the highest demand is {highest_demand_month} with {monthly_demand.max()} bookings.\n")
print("\n-------------------------------------------------\n")


## Q3: Fill missing stays values with the median.
print("## Q3: Fill Missing Stays Values with Median\n")
df['total_stays'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
median_stays = df['total_stays'].median()
print(f"The median for 'total_stays' is: {median_stays}")
df['total_stays'] = df['total_stays'].fillna(median_stays)
print("\n✅ Checked for missing values in 'total_stays' and they have been handled (if any existed).\n")
print("\n-------------------------------------------------\n")


## Q4: Analyze the impact of children on cancellations.
print("## Q4: Impact of Children on Cancellations\n")
cancellation_analysis = df.groupby(df['children'] > 0)['is_canceled'].value_counts(normalize=True).unstack() * 100
cancellation_analysis.index = ['No Children', 'With Children']
cancellation_analysis.columns = ['Not Canceled (%)', 'Canceled (%)']
print("Cancellation rates based on the presence of children:\n")
print(cancellation_analysis)
print(f"\n💡 Bookings with children have a cancellation rate of {cancellation_analysis.loc['With Children', 'Canceled (%)']:.2f}%, slightly higher than those without.\n")
print("\n-------------------------------------------------\n")


## Q5: Initial Plots
print("## Q5: Generating Initial Visualizations\n")

# Bar plot for cancellations vs. month
plt.figure(figsize=(12, 6))
sns.countplot(x='arrival_date_month_sorted', hue='is_canceled', data=df)
plt.title('Cancellations by Month')
plt.xlabel('Month')
plt.ylabel('Number of Bookings')
plt.xticks(rotation=45)
plt.legend(title='Canceled', labels=['No', 'Yes'])
plt.tight_layout()
plt.show()

# Line plot for total stays vs. number of adults
plt.figure(figsize=(12, 6))
df_filtered_adults = df[(df['adults'] > 0) & (df['adults'] <= 10)] # Filter for more meaningful plot
sns.lineplot(x='adults', y='total_stays', data=df_filtered_adults, errorbar=None, marker='o')
plt.title('Average Total Stays vs. Number of Adults')
plt.xlabel('Number of Adults')
plt.ylabel('Average Total Stay (nights)')
plt.grid(True)
plt.tight_layout()
plt.show()
print("✅ Initial plots have been generated.\n")
print("\n-------------------------------------------------\n")


# ==============================================================================
# EXTRA GRAPHS
# ==============================================================================

print("## Generating Extra Graphs\n")

## Graph 1: Distribution of Bookings by Market Segment (Pie Chart)
plt.figure(figsize=(10, 8))
segment_counts = df['market_segment'].value_counts()
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140,
        wedgeprops={'edgecolor': 'black'})
plt.title('Distribution of Bookings by Market Segment', fontsize=16)
plt.axis('equal')
plt.show()


## Graph 2: Cancellation Rate by Market Segment (Bar Chart)
plt.figure(figsize=(12, 7))
cancellation_rates = df.groupby('market_segment')['is_canceled'].mean().sort_values(ascending=False) * 100
sns.barplot(x=cancellation_rates.index, y=cancellation_rates.values, hue=cancellation_rates.index, palette='viridis', legend=False)
plt.title('Cancellation Rate by Market Segment', fontsize=16)
plt.xlabel('Market Segment', fontsize=12)
plt.ylabel('Cancellation Rate (%)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


## Graph 3: Average Daily Rate (ADR) per Month by Hotel Type (Line Plot)
plt.figure(figsize=(14, 7))
# Filter out extreme ADR values for a cleaner plot
df_filtered_adr = df[df['adr'] < 5000]
sns.lineplot(x='arrival_date_month_sorted', y='adr', hue='hotel', data=df_filtered_adr, errorbar=None, marker='o')
plt.title('Average Daily Rate (ADR) by Month and Hotel Type', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Daily Rate (ADR)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Hotel Type')
plt.tight_layout()
plt.show()
print("✅ Extra graphs have been generated.\n")