import pandas as pd
import plotly.express as px
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime as dt

# Read the data source and convert date to year and month
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')
df['Month'] = pd.to_datetime(df['Date']).dt.month #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Create list for dropdown, radioItem, and legend usage
region_list = ['New South Wales', 'Northern Territory', 'Queensland', 'South Australia',
             'Tasmania', 'Victoria', 'Western Australia']

year_list = list(range(2005, 2021))

month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Convert region and month data
for old_reg, new_reg in zip(df['Region'].unique(), region_list):
    df['Region'].replace(old_reg, new_reg, inplace=True)

for old_mon, new_mon in zip(df['Month'].unique(), month_list):
    df['Month'].replace(old_mon, new_mon, inplace=True)

# Dashboard structure design
app = Dash(__name__)
app.layout = html.Div([html.H1('Australia Wildfire Dashboard', style={'textAlign': 'center', 'fonSize': 40, 'fontWeight': 'bold'}),

                       html.Div('Select Region: ', style={'textAlign': 'left', 'fontSize': 25, 'height': 45, 'fontWeight': 'bold'}),
                       html.Div(dcc.RadioItems(id='region-selection',
                                               options=region_list,
                                               value='New South Wales',
                                               inline=True,
                                               style={'textAlign': 'left', 'fontSize': 20, 'height': 35})),

                       html.Div('Select Year: ', style={'textAlign': 'left', 'fontSize': 25, 'height': 45, 'fontWeight': 'bold'}),
                       html.Div(dcc.Dropdown(id='year-selection',
                                             options=year_list,
                                             value=2010,
                                             style={'textAlign': 'left', 'fontSize': 20, 'height': 35, 'width': '75%'}) ),
                       html.Br(),
                       html.Div([dcc.Graph(id='pie-chart'),
                                 dcc.Graph(id='bar-chart', style={'width': '50%'})],
                                style={'display': 'flex'})
                       ]
                      )

# Callback decorator design and decorator function
@app.callback([Output(component_id='pie-chart', component_property='figure'),
               Output(component_id='bar-chart', component_property='figure')],
              [Input(component_id='region-selection', component_property='value'),
               Input(component_id='year-selection', component_property='value')])
def get_graph(entered_region, entered_year):
    df_year_region = df[(df['Year'] == entered_year) & (df['Region'] == entered_region)]
    df_pie = df_year_region.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    df_bar = df_year_region.groupby('Month')['Count'].mean().reset_index()

    pie_chart = px.pie(df_pie, names='Month', values='Estimated_fire_area',
                       title=f'{entered_region} : Monthly Average Estimated Fire Area in year {entered_year}')
    pie_chart.update_layout(legend=dict(x=1, y=1,
                                        xanchor='center',
                                        yanchor='top',
                                        bgcolor='white',
                                        ))

    bar_chart = px.bar(df_bar, x='Month', y='Count',
                       title=f'{entered_region} : Average Count of Pixels for Presumed Vegetation Fires in year {entered_year}')
    return pie_chart, bar_chart

if __name__ == '__main__':
    app.run(debug=True)