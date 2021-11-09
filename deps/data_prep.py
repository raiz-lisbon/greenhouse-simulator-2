import pandas as pd

def get_seconds_data(date_from, date_to):
    # Read data from CSV file
    weather_df = pd.read_csv("./weather_data/Lisboa_2020.csv", index_col=0)

    # Convert timestamp column from string to pandas timestamp
    weather_df["timestamp"] = pd.to_datetime(weather_df['timestamp'], format='%Y-%m-%d %H:%M:%S')

    # Keep rows only within the provided range
    date_to = f"{date_to}T00:00:00.000000" # To avoid cutting off the last hour of the day
    weather_of_day_df = weather_df[(weather_df['timestamp'] >= date_from) & (weather_df['timestamp'] <= date_to)].copy(deep=True)

    # Set TemistampIndex as interpolation requires it
    weather_of_day_df.set_index('timestamp', inplace=True)

    # Resample from hourly data then interpolate it
    weather_of_day_df = weather_of_day_df.resample('s').interpolate(method='polynomial', order=2)

    return weather_of_day_df