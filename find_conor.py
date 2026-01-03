import pandas as pd

master = pd.read_csv('dataset/Ultimate ufc/ufc-master.csv')

# Find Conor vs Dustin
conor_dustin = master[(master['RedFighter'] == 'Conor McGregor') & 
                      (master['BlueFighter'] == 'Dustin Poirier')]
print(f'Found {len(conor_dustin)} Conor vs Dustin fights')
for _, row in conor_dustin.iterrows():
    date_val = row['Date']
    winner = row['Winner']
    print(f'  Date: {date_val}, Winner: {winner}')
