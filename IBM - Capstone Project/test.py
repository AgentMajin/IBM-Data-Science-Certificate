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

def return_pie(launch_site):
    df_pie = spacex_df[spacex_df['Launch Site'] == launch_site]
    df_group = df_pie['class'].value_counts().reset_index()
    print(df_group)
    # fig = px.pie(df_group, names= 'class', values='count')
    
    # fig.show()

if __name__ == '__main__':
    return_pie('CCAFS LC-40')