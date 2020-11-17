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
        marks = {str (year) : {'label' : str (year), 'style' : {'color' : 'blue', 'fontSize' : 9, 'writing-mode' : 'vertical-lr', 'text-orientation' : 'sideways-right'}} for year in data ['Year'].unique ()}
    ),
    html.Div (id = 'output-container-slider'),
    ], style = {'display' : 'inline-block', 'width' : '800px'}),      
        html.Div ([
        dcc.Graph (id = 'graph_1'),
    ], style = {'display' : 'inline-block', 'width' : '60%'}),
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
        
    map.update_layout (
      title_text = column + ' deaths in '+ str (value) + ' (average: '+ str (average) + ' deaths)',
      geo = dict (
          showframe = False,
          showcoastlines = False,
          projection_type = 'equirectangular'
      ), coloraxis_showscale = False,
      annotations = [dict (
        x = 0.05,
        y = 0.05,
        xref = 'paper',
        yref = 'paper',
        text = 'Source:<a href="https://www.emdat.be/">\
            EM-DAT</a>',
        showarrow = False
    )]
)

    top_15 = filtered_df.sort_values (column, ascending = False)

    bar = px.bar (top_15.head (15), x = 'Country', y = column, color = column, color_continuous_scale = 'Reds')

    bar.update_xaxes (title_text = '')
    bar.update_yaxes (title_text = '')
    bar.update_layout (title = 'Top 15 Countries')
    return map, bar

@app.callback(
    Output('output-container-slider', 'figure'),
    [Input ('column', 'value'), Input ('year-slider', 'value')]
)
@app.callback(
    [Output ('graph_1', 'figure'), Output ('graph_2', 'figure')],
    [Input ('column', 'value'), Input ('year-slider', 'value')]
)
def update (column, value):
    return create_graphs (column, value)

if __name__ == '__main__':
  app.run_server()
