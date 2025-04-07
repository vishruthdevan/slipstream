import pandas as pd

results_df = pd.read_csv('results.csv')
race_df = pd.read_csv('race.csv')

merged_df = pd.merge(results_df, race_df[['raceId', 'year']], on='raceId', how='left')
agg_df = merged_df.groupby(['driverId', 'constructorId', 'year'], as_index=False)['points'].sum()


agg_df = agg_df.sort_values(by=['year', 'points'], ascending=[True, False])
agg_df['rank'] = agg_df.groupby('year')['points'].rank(method='dense', ascending=False).astype(int)

agg_df.rename(columns={'driverId': 'driverid', 
                       'constructorId': 'constructorid'}, inplace=True)

final_df = agg_df[['driverid', 'constructorid', 'year', 'points', 'rank']]

final_df.to_csv('driver_season_rankings.csv', index=False)

print("New CSV created: driver_season_rankings.csv")
