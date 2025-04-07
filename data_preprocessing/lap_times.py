import pandas as pd

lap_times = pd.read_csv('lap_times.csv')
qualifying = pd.read_csv('qualifying.csv')

merged_df = pd.merge(lap_times, qualifying[['raceId', 'driverId', 'constructorId']], 
                     on=['raceId', 'driverId'], how='left')

merged_df['lapId'] = range(1, len(merged_df) + 1)
final_df = merged_df[['lapId', 'raceId', 'driverId', 'constructorId', 'lap', 'position', 'time']]
final_df.columns = ['lapId', 'raceId', 'driverId', 'constructorId', 'lapNumber', 'position', 'lapTime']

final_df.to_csv('newLapTimes.csv', index=False)
