# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Read the airline data into pandas dataframe
cd = os.getcwd()
spacex_df = pd.read_csv(cd + "\\IBM - Capstone Project\\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'All', 'value': 'All'}
    ]

for launch_site in spacex_df['Launch Site'].unique():
    dropdown_options.append({'label': launch_site, 'value': launch_site})


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                                options= dropdown_options,
                                                value = 'All',
                                                placeholder = 'All',
                                                style={'width': '80%',
                                                        'padding': '3px',
                                                        'font-size': '20px',
                                                        'textAlign': 'center',
                                                        })
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart'),
                                         style = {'display': 'flex'}),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(
                                    dcc.RangeSlider(min=0, max=10000, step=1000,
                                                    id='payload-slider',
                                                     marks={0: '0',
                                                            100: '100'},
                                                    value=[min_payload, max_payload])
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id= 'success-pie-chart', component_property= 'figure'),
    Input(component_id= 'site-dropdown', component_property= 'value')
)

def return_pie(launch_site):
    if launch_site == 'All':
        df_pie = spacex_df
        df_group = df_pie.groupby(by='Launch Site').mean(['class']).reset_index()
        fig = px.pie(df_group, names= 'Launch Site', values='class')
    else:
        df_pie = spacex_df[spacex_df['Launch Site'] == launch_site]
        df_group = df_pie['class'].value_counts().reset_index()
        fig = px.pie(df_group, names= 'class', values='count')

    return(fig)


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id= 'site-dropdown', component_property= 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')
])

def return_scatter(launch_site, payload_range):
    if launch_site == 'All':
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
    df = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(df, x = 'Payload Mass (kg)', y='class',color="Booster Version Category")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


