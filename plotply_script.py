import pandas as pd
import dash
from dash import dash_table, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os


from tkinter import *

  


#app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")

conn = sqlite3.connect('db.db')
cursor = conn.cursor()
cursor.execute('SELECT ID,FECHA,GASTO,IMPORTE,CATEGORIA, TIPO FROM gastos')

df = pd.read_sql('SELECT ID,FECHA,GASTO,IMPORTE,CATEGORIA, TIPO FROM gastos', conn)



app = dash.Dash(__name__)

app.layout = html.Div([

            html.Div([
                html.Pre(children="Gastos",
                style={"text-align": "center", "font-size":"100%", "color":"black"})
                ]),


            html.Div([
                html.Label(['X-axis categories to compare:'], style={'font-weight':'bold'}),
                dcc.RadioItems(
                    id='xaxis_raditem',
                    options=[
                            {'label': 'Importe', 'value': 'IMPORTE'},
                            {'label': 'Categoría', 'value': 'CATEGORIA'},
                    ],
                    value='IMPORTE',
                    style={'width': '50%'},      
                ),                             
            ]),
                        html.Div([
                html.Label(['y-axis categories to compare:'], style={'font-weight':'bold'}),
                dcc.RadioItems(
                    id='yaxis_raditem',
                    options=[
                            {'label': 'Importe', 'value': 'IMPORTE'},
                            {'label': 'Categoría', 'value': 'CATEGORIA'},
                    ],
                    value='IMPORTE',
                    style={'width': '50%'},      
                ),                             
            ]),
            dcc.Graph(id='the_graph')
    ])



@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
    Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):
    dff = df

    #print(dff[[x_axis],[y_axis]][:1])

    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': por '+x_axis
    )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9, 'x':0.5,})

    return(barchart)






if __name__ == '__main__':
    
    cursor.close()
    app.run_server(debug=True)
