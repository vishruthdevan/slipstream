import pandas as pd  

def parse_time_str(time_str):  
    if pd.isnull(time_str) or time_str.strip() == "":  
        return None  

    time_str = time_str.strip()  
    if time_str.startswith('+'):  
        time_str = time_str[1:]  
        if ':' in time_str:  
            minutes, seconds = time_str.split(':')  
            total_seconds = int(minutes) * 60 + float(seconds)  
        else:  
            total_seconds = float(time_str)  
        return total_seconds  
    else:  
        if ':' in time_str:  
            minutes, seconds = time_str.split(':')  
            total_seconds = int(minutes) * 60 + float(seconds)  
        else:  
            total_seconds = float(time_str)  
        return total_seconds  

def format_seconds_to_time(total_seconds):  
    if total_seconds is None:  
        return ""  
    minutes = int(total_seconds // 60)  
    seconds = total_seconds % 60  
    return f"{minutes}:{seconds:06.3f}"  

def compute_raw_duration(group):  
    winner = group[group['positionOrder'] == 1]
    if not winner.empty and not pd.isnull(winner.iloc[0]['duration']):  
        winner_time_str = winner.iloc[0]['duration']  
        winner_seconds = parse_time_str(winner_time_str)  
    else:  
        winner_seconds = None  

    def compute_row_time(row):  
        time_str = row['duration']  
        if pd.isnull(time_str) or time_str.strip() == "":  
            return ""  
        if time_str.startswith('+'):  
            delay_seconds = parse_time_str(time_str)  
            if winner_seconds is not None:  
                raw_time_seconds = winner_seconds + delay_seconds  
                return format_seconds_to_time(raw_time_seconds)  
            else:  
                return ""  
        else:  
            raw_time_seconds = parse_time_str(time_str)  
            return format_seconds_to_time(raw_time_seconds)  
    
    group['duration'] = group.apply(compute_row_time, axis=1)  
    return group  


df = pd.read_csv('data/sprint_results.csv')  
df = df.groupby('raceId', group_keys=False).apply(compute_raw_duration)  
final_df = df[['raceId', 'driverId', 'constructorId', 'duration', 'grid', 'positionOrder', 'points']].copy()  

final_df.columns = ['raceid', 'driverid', 'constructorid', 'duration', 'grid', 'positionOrder', 'points']  

final_df.to_csv('data/sprint_results_PSQL.csv', index=False)  

