import requests
import pandas as pd 
from pandas import json_normalize
import plotly.express as px
from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt

# Defines the url, parameters and headers for the default API Request. 

url = "https://api.openaq.org/v2/measurements"

headers = {"accept": "application/json", 
           "content-type": "json",
           "X-API-Key": "REDACTED"}

default_params = {
    'date_from':'17-02-2024',
    'date_to':'18-02-2024',
    'limit':'10000',
    'offset':'0',
    'sort':'desc',
    'parameter':'pm25',
    'country':'GB',
}

# Defines the function that creates a pandas dataframe from the API response. 

def make_API_call(params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        df = json_normalize(data['results']) # Extract only the data inside the results dictionary and make into a pandas dataframe
        df = df.rename(columns={'value': 'PM2.5 (μg/m3)', 'coordinates.latitude':'Latitude', 'coordinates.longitude': 'Longitude', 'location':'Location'}) # renames some important columns
        df = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['PM2.5 (μg/m3)'].mean() # Calculates an average for PM2.5 concentrations for each location
        df = df.round({'PM2.5 (μg/m3)':1}) # Rounds the PM2.5 column to one decimal
        return df
    else: 
        print(f"Error: {response.status_code}, {response.text}")


# Creates a dataframe with make_API_call function 

df = make_API_call(default_params) 
# print(df)

# Identifies 10 most polluted locations

df_sorted = df.sort_values(by=['PM2.5 (μg/m3)'],ascending=False) # Sorts from highest to lowest PM2.5 concentration
top_locations = df_sorted[['Location', 'PM2.5 (μg/m3)']].head(10) # Picks the top 10 locations based on highest PM2.5 concentration
top_locations = top_locations.reset_index(drop=True) # Resets the indexes, deleting the original ones and add new index starting from 0
top_locations.index = top_locations.index + 1 # Add one to each index, so that we have ranking 1 to 10
top_locations = top_locations.reset_index() # Resets index, converting the previous index into a new colum
top_locations= top_locations.rename(columns={'index':'Rank'}) # Renames the 'index' column to 'Rank'
# print(top_locations)
# print(df.head())

# Creates a function defining the properties of the figure to show. Uses plotly express library (px)

def create_figure(dataframe):
    fig = px.scatter_mapbox(dataframe, #dataframe to use for the scatter map
                            lon=dataframe['Longitude'], # Longitude of the locations to plot
                            lat=dataframe['Latitude'], # Latitude of the location to plot
                            zoom=5, # Zoom of the map
                            color=dataframe['PM2.5 (μg/m3)'], # Column to use to define the colour of the symbol
                            size=dataframe['PM2.5 (μg/m3)'], # Column to use to define the size of the symbol
                            width=1000, # Width of the figure
                            height=800, # Height of the figure
                            color_continuous_scale=px.colors.sequential.Agsunset_r, # Chooses the colour palette for the colour bar
                            hover_data={'Location': True, 'PM2.5 (μg/m3)': True, 'Longitude':True, 'Latitude':True}, # Sets what data to show when we hover over a point
                            )
    fig.update_layout(mapbox_style="carto-positron") # Sets a simple map style
    # fig.update_layout(mapbox_style="open-street-map") # To try a different map style. Decided for simpler map for a better contrast with the scatter
    return fig

# Creates the default figure 

initial_fig = create_figure(df)

# Creates a list of all the locations available in the dataframe

location_list = df['Location']
# print(location_list)

# Loops through the location list to create the options for the dropdown list

dropdown_options = []
for element in location_list:
    dropdown_options.append({'value':element, 'label':element})
# print(dropdown_options)

# Creates the Dash app

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='Air Quality in the United Kingdom', style={'margin-left':'1rem'}), # Adds title to the Dashboard 
    dcc.Dropdown(id='my-dropdown', options=dropdown_options, placeholder='Select a location'), # Adds dropdown list to select location
    html.Div(id='output-container'), # Adds text notifying selection
    html.Div([dcc.Graph(id='my-graph',figure=initial_fig, style={'display':'inline-block'}), # Adds the initial figure to the dashboard
              html.Div(dash_table.DataTable(top_locations.to_dict('records'), [{'name':i, 'id': i} for i in top_locations.columns], # Creates ranking table with its styling components. Dash_table needs the dataframe converted to dictionary
                                            style_table={'display':'in-line-block'}, 
                                            style_cell={'font-family':'serif'}), 
                       style={'margin-top':'5rem', 'margin-left':'5rem', 'margin-right':'5rem'})],
              style={'display':'flex', 'flex-direction':'row'})
])

# Gives a title to the website containing the dashboard
app.title = 'Air Quality in the United Kingdom'

# Creates a callback function to update output container and graph based on the dropdown selection.
@app.callback(
    [Output('output-container', 'children'),
    Output('my-graph', 'figure')],
    [Input('my-dropdown', 'value')]
)

#  Creates the function that updates the output based on the input (dropdown selection). update_content() is the name defined by the library

def update_content(selected_option):
    params = {
    'date_from':'17-02-2024',
    'date_to':'18-02-2024',
    'limit':'498',
    'offset':'0',
    'sort':'desc',
    'parameter':'pm25',
    'country':'GB',
    'location': selected_option # Adds the selected location to the params to make a call just for that location
    }
    new_df = make_API_call(params) # Updates the dataframe just for that location
    new_fig = create_figure(new_df) # Creates the figure that only displays that location
    return f'You have selected {selected_option}', new_fig # The first part updates 'output-container' and the second updates 'my-graph'.

# Runs the app and displays it

if __name__ == '__main__':
    app.run(debug=True)




