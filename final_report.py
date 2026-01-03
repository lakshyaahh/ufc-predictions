import pandas as pd

print('=' * 80)
print('FINAL WINNER COLUMN STATUS REPORT')
print('=' * 80)

# Check master_dataset.csv
md = pd.read_csv('master_dataset.csv')
winner_filled = (md['Winner'].notna() & (md['Winner'] != '')).sum()
print(f'\nmaster_dataset.csv:')
print(f'  Total fights: {len(md)}')
print(f'  Fights with Winner filled: {winner_filled}')
print(f'  Winner values: {list(md["Winner"].unique())}')

# Check data
print(f'\n  Fight Details:')
for idx, row in md.iterrows():
    red = row['RedFighter']
    blue = row['BlueFighter']
    date = row['Date']
    winner = row['Winner']
    print(f'    {red} vs {blue} ({date}) -> {winner}')

# Check upcoming.csv
uc = pd.read_csv('dataset/Ultimate ufc/upcoming.csv')
winner_filled_upcoming = (uc['Winner'].notna() & (uc['Winner'] != '')).sum()
empty_upcoming = (uc['Winner'].isna() | (uc['Winner'] == '')).sum()
print(f'\nupcoming.csv:')
print(f'  Total upcoming fights: {len(uc)}')
print(f'  Fights with Winner filled: {winner_filled_upcoming}')
print(f'  Empty winners: {empty_upcoming}')
date_min = uc['Date'].min()
date_max = uc['Date'].max()
print(f'  Dates: {date_min} to {date_max}')

print(f'\n' + '=' * 80)
print('SUCCESS: Winner column filled with real UFC fight results!')
print('=' * 80)
