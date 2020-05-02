import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

    
mapbox_access_token = "pk.eyJ1Ijoib2N0YXJ5biIsImEiOiJjazlvOXRjNHgwNml6M2xwMnpzaDZiYnVmIn0.zVZNaRlrbDGmKijUsuqXag"

# example measurement stations
lats = [41.434760, 38.436662]
lons = [-105.925030, -88.962141]
text = ['red', 'blue']

#viewer = jupyterlab_dash.AppViewer()


########### Initiate the app
app = dash.Dash(__name__)
server = app.server


#app = JupyterDash('SimpleExample')

app.layout = html.Div([
    # map centered to USA
    html.Div([
        dcc.Graph(
            id = "mapbox",
            figure={
                "data": [
                    dict(
                        type = "scattermapbox",
                        lat = lats,
                        lon = lons,
                        mode = "markers",
                        marker = {'size': '14'},
                        text = text
                    )
                ],
                "layout": dict(
                    autosize = True,
                    hovermode = "closest",
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    mapbox = dict(
                        accesstoken = mapbox_access_token,
                        bearing = 0,
                        center = dict(lat = 38.30, lon = -90.68),
                        style = "outdoors",
                        pitch = 0,
                        zoom = 3.5,
                        layers = []
                    )   
                )
            },
            style = {"height": "100%"}
        )
    ], style = {"border-style": "solid", "height": "50vh"}),
    # text container
    html.Div([
            html.P(id='station_id',
                   style={'fontSize': '12px'})]),
    # graph container
    html.Div([
            dcc.Graph(id='basic_graph')])

])

@app.callback(
        Output('basic_graph', 'figure'),
        [Input('mapbox', 'clickData')])
def plot_basin(selection):
    if selection is None:
        return {}
    else:
        x_data = np.linspace(0,500,500)
        y_data = np.random.rand(500)
        
        # depending on the station text use different color for line
        if selection['points'][0]['text'] == 'red':
            color='#ff0000'
        else:
            color='#0000ff'
        data = [go.Scatter(
                    x=x_data,
                    y=y_data,
                    line={'color': color},
                    opacity=0.8,
                    name="Graph"
                )]
        layout = go.Layout(
                    xaxis={'type': 'linear', 'title': "Timestep"},
                    yaxis={'type': 'linear', 'title': "Value"},
                    margin={'l': 60, 'b': 40, 'r': 10, 't': 10},
                    hovermode="closest"
                    )
        
        return {'data': data, 'layout': layout}

    
#viewer.show(app)
if __name__ == '__main__':
    app.run_server()
