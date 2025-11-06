import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Step 1: Define tasks
tasks = ['Foundation', 'Framing', 'Plumbing', 'Electrical', 'Roofing', 'Finishing']

# Step 2: Simulate start dates
start_time = datetime.now()
start_dates = [start_time + timedelta(days=i*7) for i in range(len(tasks))]

# Step 3: Simulate end dates (random duration 5-15 days)
np.random.seed(42)
end_dates = [start + timedelta(days=np.random.randint(5, 15)) for start in start_dates]

# Step 4: Simulate labor hours, material cost, equipment cost
labor_hours = np.random.randint(50, 200, len(tasks))
material_cost = np.random.randint(1000, 10000, len(tasks))
equipment_cost = np.random.randint(500, 5000, len(tasks))

# Step 5: Assign teams
teams = ['Team A', 'Team B', 'Team C', 'Team A', 'Team B', 'Team C']

# Step 6: Combine into DataFrame
df = pd.DataFrame({
    'task_name': tasks,
    'start_date': start_dates,
    'end_date': end_dates,
    'labor_hours': labor_hours,
    'material_cost': material_cost,
    'equipment_cost': equipment_cost,
    'assigned_team': teams
})

# Step 7: Create folder and save CSV
os.makedirs('data', exist_ok=True)
df.to_csv('data/resource_data.csv', index=False)

# Step 8: Load and prepare data for analysis
df = pd.read_csv('data/resource_data.csv')
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Add total cost and duration
df['total_cost'] = df['labor_hours']*50 + df['material_cost'] + df['equipment_cost']
df['duration_days'] = (df['end_date'] - df['start_date']).dt.days

# Step 9: Summary statistics for numeric columns
summary = df[['labor_hours', 'material_cost', 'equipment_cost', 'total_cost', 'duration_days']].describe()
print(summary)

# Step 10: Optional: identify tasks consuming most resources
top_cost_tasks = df.sort_values(by='total_cost', ascending=False)
print(top_cost_tasks[['task_name', 'total_cost']])
# Group by team
team_summary = df.groupby('assigned_team').agg({
    'labor_hours': 'sum',
    'total_cost': 'sum'
}).reset_index()

print(team_summary)

# Optional: find team with least labor usage
team_summary_sorted = team_summary.sort_values('labor_hours')
print(team_summary_sorted)
import matplotlib.pyplot as plt

# Bar chart: total cost per task
plt.figure(figsize=(8,5))
plt.bar(df['task_name'], df['total_cost'], color='skyblue')
plt.ylabel('Total Cost ($)')
plt.title('Total Cost per Task')
plt.show()

# Gantt-style timeline
plt.figure(figsize=(8,5))
plt.barh(df['task_name'], df['duration_days'], left=df['start_date'].map(pd.Timestamp.toordinal), color='orange')
plt.xlabel('Date (ordinal)')
plt.title('Project Timeline (Gantt-style)')
plt.show()
# Save full resource data with calculations
df.to_csv('data/resource_analysis.csv', index=False)

# Save team summary
team_summary.to_csv('data/team_summary.csv', index=False)
