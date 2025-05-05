from utils import load_csv
import pandas as pd
from datetime import date


# Loading the CSVs
call_logs_df = load_csv("call_logs.csv")
roster_df = load_csv("agent_roster.csv")
dispo_df = load_csv("disposition_summary.csv")

#here we are printing initial rows
print("\n Call Logs:")
print(call_logs_df.head())

print("\n Agent Roster:")
print(roster_df.head())

print("\n Disposition Summary:")
print(dispo_df.head())

# now after printing we are checking for missing values
print("\n Checking for missing data...")
print(call_logs_df.isnull().sum())  
print(roster_df.isnull().sum())     
print(dispo_df.isnull().sum())      

# now we are checking the data types
print("\n Checking data types...")
print(call_logs_df.dtypes)  
print(roster_df.dtypes)     
print(dispo_df.dtypes)    

# Fill missing login_time
dispo_df['login_time'].fillna('Unknown', inplace=True)

# Showing the updated dispo
print("\n Updated Disposition Summary:")
print(dispo_df.head())

# Merging all DataFrames 
merged_df = pd.merge(call_logs_df, dispo_df, on=["agent_id", "org_id", "call_date"], how="left")
merged_df = pd.merge(merged_df, roster_df, on=["agent_id", "org_id"], how="left")

# Convert duration to minutes (if there is anything in seconds)
merged_df['duration'] = merged_df['duration'] / 60  

# Previewing the merged data
print("\n Merged Data:")
print(merged_df.head())

# Grouping and calculating the metrics
metrics_df = merged_df.groupby(['agent_id', 'call_date']).agg(
    total_calls=('call_id', 'count'),
    completed_calls=('status', lambda x: (x == 'completed').sum()),
    avg_duration=('duration', lambda x: round(x.mean(), 2))
).reset_index()

# Adding connect rate
metrics_df['connect_rate'] = round(metrics_df['completed_calls'] / metrics_df['total_calls'] * 100, 2)

# Showing calculated metrics
print("\n Calculated Metrics:")
print(metrics_df.head())

# Saving to CSV
metrics_df.to_csv('agent_metrics.csv', index=False)
print("\n Saved the final results to 'agent_metrics.csv'")

# Summary which can be viewed
best_agent = metrics_df.loc[metrics_df['completed_calls'].idxmax()]
active_agents = metrics_df['agent_id'].nunique()
avg_call_time = metrics_df['avg_duration'].mean()
today = date.today().strftime("%Y-%m-%d")

# Final Slack-style summary for better understanding
print("\n Daily Agent Performance Summary")
print(f" Date: {today}")
print(f" Best Agent: {best_agent['agent_id']} with {best_agent['completed_calls']} completed calls")
print(f" Active Agents: {active_agents}")
print(f" Avg Call Duration: {avg_call_time:.2f} minutes")
print(f" Highest Connect Rate: {metrics_df['connect_rate'].max()}%")
