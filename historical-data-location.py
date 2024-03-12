import requests
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Defines the url, parameters, and headers for the default API Request.
location_selected = input('What location do you want to see? ')
url = "https://api.openaq.org/v2/measurements"
headers = {
    "accept": "application/json",
    "content-type": "json",
    "X-API-Key": "REDACTED",
}
default_params = {
    'date_from': '26-11-2023 00:00',
    'date_to': '27-11-2023 00:00',
    'limit': '499',
    'offset': '0',
    'sort': 'desc',
    'parameter': 'pm25',
    'country': 'GB',
    'location': location_selected,
}
# Historical data
def make_API_call_no_average(params):
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    df = json_normalize(data['results'])
    df = df.rename(
        columns={
            'value': 'PM2.5 (μg/m3)',
            'coordinates.latitude': 'Latitude',
            'coordinates.longitude': 'Longitude',
            'location': 'Location',
        }
    )
    df = df.round({'PM2.5 (μg/m3)': 1})
    return df
df_no_average = make_API_call_no_average(default_params)
location_data = df_no_average[df_no_average['Location'] == location_selected]
# Convert 'date.local' column to datetime
location_data['date.local'] = pd.to_datetime(location_data['date.local'])
# Plot using scatter plot with lines
fig, ax = plt.subplots()
ax.scatter(location_data['date.local'], location_data['PM2.5 (μg/m3)'], marker='o', color='blue', label='Scatter Plot')
ax.plot(location_data['date.local'], location_data['PM2.5 (μg/m3)'], linestyle='-', color='red', label='Lines')
ax.set_xlabel('Date and Time')
ax.set_ylabel('PM2.5 (μg/m3)')
ax.set_title(f'PM2.5 Levels in {location_selected}')
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))  # Set ticks for each hour
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))  # Format for date and time
plt.xticks(rotation=20, ha='right')  # Rotate x-axis labels for better visibility
plt.legend()
plt.show()