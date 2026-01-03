import pandas as pd
from datetime import datetime

# Load both datasets
master = pd.read_csv('dataset/Ultimate ufc/ufc-master.csv')
upcoming = pd.read_csv('dataset/Ultimate ufc/upcoming.csv')

# Convert dates
master['Date'] = pd.to_datetime(master['Date'])
upcoming['Date'] = pd.to_datetime(upcoming['Date'])

# Check date ranges
print('Master dataset date range:')
print(f'  From: {master["Date"].min().date()}')
print(f'  To: {master["Date"].max().date()}')
print(f'  Total fights: {len(master)}')

print('\nUpcoming dataset date range:')
print(f'  From: {upcoming["Date"].min().date()}')
print(f'  To: {upcoming["Date"].max().date()}')
print(f'  Total fights: {len(upcoming)}')

# Check if any upcoming fights are in master dataset
print('\nChecking for Dec 14, 2024 fights in master dataset:')
dec_14_2024 = master[master['Date'].dt.date == pd.to_datetime('2024-12-14').date()]
print(f'Found: {len(dec_14_2024)} fights on 2024-12-14')

if len(dec_14_2024) > 0:
    print('\nFights on 2024-12-14:')
    for _, row in dec_14_2024.iterrows():
        print(f'  {row["RedFighter"]} vs {row["BlueFighter"]} - Winner: {row["Winner"]}')

# Check other nearby dates
print('\nChecking for Colby Covington fights in master:')
colby = master[master['RedFighter'].str.contains('Colby', case=False, na=False) | 
               master['BlueFighter'].str.contains('Colby', case=False, na=False)]
print(f'Found: {len(colby)} fights with Colby')
if len(colby) > 0:
    for _, row in colby.head(3).iterrows():
        print(f'  {row["RedFighter"]} vs {row["BlueFighter"]} ({row["Date"].date()}) - {row["Winner"]}')
