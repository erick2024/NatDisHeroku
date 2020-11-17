import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/BWLwgP.css']

url = 'https://raw.githubusercontent.com/erick2024/NaturalDisastersMapgraph/main/Natural_disasters_data.csv'

data = pd.read_csv (url)

dropdown_labels = data.groupby (['Country', 'Year']).sum (numeric_only = True)

app = dash.Dash (__name__, external_stylesheets = external_stylesheets)
server = app.server

app.layout = html.Div ([
        html.H6 ("Deaths Due to Natural Disasters From 1900-2020"),
        html.Div ([
        html.H6 ("Data Set"),
        dcc.Dropdown(
            id = 'column', clearable = False,
            value = 'Total Deaths',
            options = [
                {'label' : c, 'value' : c}
                for c in dropdown_labels.columns
            ]),
        ], style = {'display' : 'inline-block', 'width' : '200px'}),  
        html.Div ([
        html.H6 ("Year"),
        dcc.Slider (
        id = 'year-slider',
        min = data ['Year'].min(),
        max = data ['Year'].max(),
        value = data ['Year'].max(),
        marks = {str (year) : {'label' :str (year), 'style' : {'color' : 'blue', 'fontSize' : 9, 'writing-mode' : 'vertical-lr', 'text-orientation' : 'sideways-right'}} for year in data ['Year'].unique()}
    ),
    html.Div (id = 'output-container-slider'),
    ], style = {'display' : 'inline-block', 'width' : '800px'}),      
        html.Div ([
        dcc.Graph (id = 'graph_1'),
    ], style = {'display' : 'inline-block', 'width' : '200px'}),
     html.Div ([
        dcc.Graph (id = 'graph_2'),
    ], style = {'display' : 'inline-block', 'width' : '40%'})
], style = {'display' : 'inline-block', 'width' : '1000px'})    

def create_graphs (column, value):
    filtered_df = data [data.Year == value]
    average = '{:,}'.format (int (data [column].sum ()/data.shape [0]))
   
    map = go.Figure (data = go.Choropleth (
      locations = filtered_df ['country_code'],
      z = filtered_df [column],
      text = filtered_df ['Country'],
      colorscale = 'Reds',
      autocolorscale = False,
      reversescale = False,
      marker_line_color = 'darkgray',
      marker_line_width = 0.5
))
    
if __name__ == '__main__' :
  app.run_server ()
