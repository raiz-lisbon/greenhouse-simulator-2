import pandas as pd
from datetime import timezone
from pathlib import Path

def get_weather_data(date_from, date_to, resample_period="min"):
    """
    Valid resample values: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    """
    # Read data from CSV file
    weather_df = pd.read_csv(Path(__file__).parent.parent / "weather_data/Lisboa_2020.csv", index_col=0)

    # Convert timestamp column from string to pandas timestamp
    weather_df["timestamp"] = pd.to_datetime(weather_df['timestamp'], format='%Y-%m-%d %H:%M:%S')

    # Keep rows only within the provided range
    date_to = f"{date_to}T00:00:00.000000" # To avoid cutting off the last hour of the day
    weather_of_day_df = weather_df[(weather_df['timestamp'] >= date_from) & (weather_df['timestamp'] <= date_to)].copy(deep=True)

    # Set TimestampIndex as interpolation requires it
    weather_of_day_df.set_index('timestamp', inplace=True)

    # Resample from hourly data then interpolate it
    weather_of_day_df = weather_of_day_df.resample(resample_period).interpolate(method='polynomial', order=2)

    # Add timezone information
    weather_of_day_df = weather_of_day_df.tz_localize(timezone.utc)

    return weather_of_day_df