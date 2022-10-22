from dash import Dash
import logging

import archi.parsexml as parsexml
import archi.creategraphs as creategraphs
import archi.configarchi as conf
import archi.exploitgraph as exploitgraph
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, html, dcc, Input, Output


if __name__ == '__main__':

    logger = logging.getLogger('archi-external-use')
    logger.setLevel(logging.WARNING)
    fh = logging.FileHandler(filename='test-archi-external-use.log')
    fh.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start. Application is initializing')

    fileToRead = 'tinker.xml'
    
    content = parsexml.readModel(fileToRead)
    viewIdentifier = 'id-14c9a667d06949e49b10686750cf5cac'
    viewAsGraph = creategraphs.createGraphView(viewIdentifier, content)
    lists: conf.Lists
    lists = exploitgraph.prepareBusinessCapabilitiesTreemap(viewAsGraph)

    df = pd.DataFrame() 
    df['parent'] = lists.parents 
    df['ids'] = lists.ids 
    #df['value']= size 
    df['level'] = lists.levels
    df['hovertext'] = lists.textsinfo
    df['label'] = lists.textsinfo


    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            0,
            3,
            step=None,
            value=3,
            marks = {0 : 'TopLevel', 1: 'Level1', 2: 'Level2', 3: 'Level3'},
            id='sliderVal'
        )
    ])


    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('sliderVal', 'value'))
    def update_figure(sliderVal):

        fig = go.Figure()
        fig.add_trace(go.Treemap(
            ids = df[df['level']<=sliderVal]['ids'],
            labels = df[df['level']<=sliderVal]['label'],
            #values = df[df['level']<=sliderVal]['value'],
            parents = df[df['level']<=sliderVal]['parent'],
            hovertext=df[df['level']<=sliderVal]['hovertext']
        ))
        fig.update_traces(root_color="#f1f1f1")
        fig.update_layout(width = 900, height = 900)


        return fig
    
    app.run_server(debug=True)
