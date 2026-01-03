import pandas as pd

master = pd.read_csv('dataset/Ultimate ufc/ufc-master.csv')

# Check fights with those two fighters
fights = master[((master['RedFighter'].str.contains('Conor', na=False)) | 
                (master['BlueFighter'].str.contains('Conor', na=False))) &
               ((master['RedFighter'].str.contains('Dustin', na=False)) | 
                (master['BlueFighter'].str.contains('Dustin', na=False)))]

print(f'Total Conor vs Dustin fights: {len(fights)}')
for idx, row in fights.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    date = row['Date']
    winner = row['Winner']
    print(f'{date}: {red} vs {blue} - Winner: {winner}')
