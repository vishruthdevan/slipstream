import pandas as pd


constructor_standings = pd.read_csv('constructor_standings.csv')
races = pd.read_csv('race.csv')

merged_df = pd.merge(constructor_standings, races[['raceId', 'year', 'round']], on='raceId', how='left')
final_df = merged_df.loc[merged_df.groupby(['constructorId', 'year'])['round'].idxmax()]
result_df = final_df[['constructorId', 'year', 'points', 'position']].rename(columns={'position': 'rank'})
result_df.to_csv('constructor_standings_by_year.csv', index=False)
