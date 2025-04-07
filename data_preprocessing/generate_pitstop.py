import pandas as pd

pit_stops = pd.read_csv("pit_stops.csv")
lap_times = pd.read_csv("lap_times.csv")

merged_df = pd.merge(
    pit_stops,
    lap_times[['lapId', 'raceId', 'driverId', 'lapNumber']],
    on=['raceId', 'driverId', 'lapNumber'],
    how='left'
)

merged_df.insert(0, 'pitstopid', range(1, len(merged_df) + 1))
output_df = merged_df[['pitstopid', 'lapId', 'time', 'duration']]
output_df.to_csv("new_pitstops.csv", index=False)
