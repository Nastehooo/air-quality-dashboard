# Description

This project consists of a UK Air Quality Dashboard created using Python libraries Plotly, Dash, matplotlib and pandas, for the course "Python and Apps", run by Code First Girls. The project was created by team members Nasteho Abdi and Claudia Castro Faccetti.

# Key Features

## Air Quality Dashboard 

The UK Air Quality Dashboard enables the user to see a scatter plot in a map of the United Kingdom, showing PM2.5 (fine dust) concentrations in different locations in the UK with air quality monitoring stations. The data was extracted from the open air quality API, OpenAQ (https://openaq.org/). The user is able to select a specific monitoring station from a dropdown list on the top part of the website. When selecting a location, the map is updated to show only the location selected. On the right side, a ranking of the top 10 locations with higher PM2.5 concentrations in the UK is shown. 

The time period of the scatter plot and ranking is fixed within the code. Further work on the dashboard will enable the user to select the time period they wish to visualise. 

## Historical Data for a Specific Location

If the user is interested in seeing data changes in time, they can select a location from the dropdown list in the dashboard, and write its name as input on the historical data app. A line plot of the changes in time for a given time period is the output of running this app. 

The time period of the line plot is fixed within the code. Further code will enable the user to input the time period they wish to visualise.

# How to Use the Project

## Air Quality Dashboard

Upon running the Python code in the file "dashboard-map.py", a dashboard will open on the browser, with the address http://127.0.0.1:8050/. Note that the API key has been redacted. Insert your own OpenAQ API key tp the code to access the data. 

## Historical Data for a Specific Location

Upon running the Python code in the file "historical-data-locations.py", an input request, asking for the name of the location to examine will appear. Type a location name from the dashboard dropdown list. Note that the API key has been redacted. Insert your own OpenAQ API key tp the code to access the data. 

# Author Contributions

Claudia Castro Faccetti created the dashboard, available in the file "dashboard-map.py".

Nasteho Abdi created the historical data app, available in the file "historical-data-locations.py".
