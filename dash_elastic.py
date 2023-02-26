import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
import re
from flask import Flask, render_template, request
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State



df_finale = pd.read_csv('dataframe_finale.csv',delimiter=';')
# conversion des variables et formatage
df_finale['Last Week'] = df_finale['Last Week'].replace("-",0)
df_finale['Last Week']= df_finale['Last Week'].astype('int64')
df_finale['Date'] = pd.to_datetime(df_finale['Date'])

data = df_finale.to_dict('records')

# séparation des strings dans plusieurs catégories
for i,song in enumerate(data):
    song['Genre'] = re.split(', | & ', song['Genre'])
    song['Producers'] = re.split(', | & ', song['Producers'])
    try:
        song['Writers'] = re.split(', | & ', song['Writers'])
    except TypeError:
        data[i]["Writers"] = "None"
        song['Writers'] = re.split(', | & ', song['Writers'])
    try:
        song['Distributor'] = re.split(', | & ', song['Distributor'])
    except TypeError:
        data[i]["Distributor"] = "None"
        song['Distributor'] = re.split(', | & ', song['Distributor'])


# démarrage ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])

# indexation des données dans elastic search
def generate_data(data):
    for docu in data:
        yield {
            "_index": "billboard2",
            "_type": "song",
            "_source": {k:v if v else None for k,v in docu.items()},
        }
        
if es.indices.exists('billboard2')==True:
    es.indices.delete(index='billboard2')
    bulk(es, generate_data(data))
else :
    bulk(es, generate_data(data))



def graph_rank(query,field):
    QUERY = {
    "aggs": {
        "2": {
        "date_histogram": {
            "field": "Date",
            "calendar_interval": "1w",
            "time_zone": "Europe/Paris",
            "min_doc_count": 1
        },
        "aggs": {
            "1": {
            "avg": {
                "field": "Rank"
            }
            }
        }
        }
    },
    "size": 0,
    "_source": {
        "excludes": []
    },
    "stored_fields": [
        "*"
    ],
    "script_fields": {},
    "docvalue_fields": [
        {
        "field": "Date",
        "format": "date_time"
        }
    ],
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "bool": {
                "should": [
                {
                    "match_phrase": {
                    field : query
                    }
                }
                ],
                "minimum_should_match": 1
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    }
    result = es.search(index="billboard2", body=QUERY)

    x_values, y_values = [],[]
    for i in range(len(result["aggregations"]["2"]["buckets"])):
        aggregations_x = result["aggregations"]["2"]["buckets"][i]['key_as_string']
        aggregations_y = result["aggregations"]["2"]["buckets"][i]['1']['value']
        x_values.append(aggregations_x)
        y_values.append(aggregations_y)

    fig = px.line(x=x_values,y=y_values,title=f"Evolution du Average Rank de {query} de au cours des semaines")
    fig.update_layout(
        xaxis_title="Dates by Weeks",
        yaxis_title="Average Rank"
    )
    fig.update_yaxes(autorange="reversed")

    return fig

def graph_count(query,field):
    QUERY = {
        "aggs": {
            "2": {
            "date_histogram": {
                "field": "Date",
                "calendar_interval": "1w",
                "time_zone": "Europe/Paris",
                "min_doc_count": 1
            }
            }
        },
        "size": 0,
        "_source": {
            "excludes": []
        },
        "stored_fields": [
            "*"
        ],
        "script_fields": {},
        "docvalue_fields": [
            {
            "field": "Date",
            "format": "date_time"
            }
        ],
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "bool": {
                    "should": [
                    {
                        "match_phrase": {
                        field: query
                        }
                    }
                    ],
                    "minimum_should_match": 1
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        }
    
    result = es.search(index="billboard2", body=QUERY)
    x_values, y_values = [],[]
    for i in range(len(result["aggregations"]["2"]["buckets"])):
        aggregations_x = result["aggregations"]["2"]["buckets"][i]['key_as_string']
        aggregations_y = result["aggregations"]["2"]["buckets"][i]['doc_count']
        x_values.append(aggregations_x)
        y_values.append(aggregations_y)


    fig2 = px.line(x=x_values,y=y_values,title=f"Evolution du nombre de chanson de {query} au cours des semaines")
    fig2.update_layout(
        xaxis_title="Dates by Weeks",
        yaxis_title="Count"
    )

    return fig2

def graph_classement(size,field):
    QUERY = {
    "aggs": {
        "2": {
        "terms": {
            "field": field,
            "order": {
            "_count": "desc"
            },
            "size": size
        }
        }
    },
    "size": 0,
    "_source": {
        "excludes": []
    },
    "stored_fields": [
        "*"
    ],
    "script_fields": {},
    "docvalue_fields": [
        {
        "field": "Date",
        "format": "date_time"
        }
    ],
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "match_all": {}
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    }
    result = es.search(index="billboard", body=QUERY)
    x_values, y_values = [],[]

    for i in range(len(result["aggregations"]["2"]["buckets"])):
        aggregations_y = result["aggregations"]["2"]["buckets"][i]['key']
        aggregations_x = result["aggregations"]["2"]["buckets"][i]['doc_count']
        x_values.append(aggregations_x)
        y_values.append(aggregations_y)

    fig = px.bar(x=x_values,y=y_values, orientation='h', title=f"Top {size} des {field} sur toute la période")

    fig.update_layout(
        xaxis_title="Count",
        yaxis_title="Genre"
    )
    fig.update_yaxes(autorange="reversed")

    return fig

################################### DASH APP ###########################################

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(children='Dashboard Genius-Billboard', style={'text-align':'center','font-family':'Arial'}),

    html.H2('Graphique de rang :',style={'font-family':'Arial'}),

    html.Label('Barre de recherche : ',style={'font-family':'Arial'}),

    dcc.Input(id='search-input', type='text', placeholder='Enter a search query',value='Shut Down'),
    # html.Button('Search', id='search-button', n_clicks=0),

    dcc.RadioItems(
        options=[
            {'label': 'Title', 'value': 'Title'},
            {'label': 'Artist', 'value': 'Artist'},
            {'label': 'Genre', 'value': 'Genre'},
            {'label': 'Distributor', 'value': 'Distributor'},
            {'label': 'Producer', 'value': 'Producer'},
        ],
        id='search-field',
        value='Title',
    ),
    # html.Label('Graphe de rank : ',style={'font-family':'Arial'}),

    dcc.Graph(id='rank-graph'),

    html.H2('Graphique de count :',style={'font-family':'Arial'}),

    html.Label('Barre de recherche : ',style={'font-family':'Arial'}),

    dcc.Input(id='search-input2', type='text', placeholder='Enter a search query',value='Christmas'),
    # html.Button('Search', id='search-button2', n_clicks=0),

    dcc.RadioItems(
        options=[
            {'label': 'Title', 'value': 'Title'},
            {'label': 'Artist', 'value': 'Artist'},
            {'label': 'Genre', 'value': 'Genre'},
            {'label': 'Distributor', 'value': 'Distributor'},
            {'label': 'Producer', 'value': 'Producer'},
        ],
        id='search-field2',
        value='Genre',
        
    ),

    # html.Label('Graphe de count : ',style={'font-family':'Arial'}),
    dcc.Graph(id='count-graph'),


    html.H2('Graphique de classement :',style={'font-family':'Arial'}),

    dcc.Slider(10,60, 
        step =5,
        id='size-slider',
        value=10,
    ),

    dcc.RadioItems(
        options=[
            {'label': 'Artist.keyword', 'value': 'Artist.keyword'},
            {'label': 'Genre.keyword', 'value': 'Genre.keyword'},
        ],
        id='search-field3',
        value='Genre.keyword',
    ),

    # html.Label('Graphe de classement : ',style={'font-family':'Arial'}),
    dcc.Graph(id='classement-graph')
])

@app.callback(
    # Output('rank-graph', 'figure'),
    # Input('search-button', 'n-clicks'),
    # Input('search-field', 'value'),
    # State('search-input', 'value'),
    Output('rank-graph', 'figure'),
    # Input('search-button', 'n-clicks'),
    Input('search-input', 'value'),
    Input('search-field', 'value'),
)
# def update_rank_graph(n_clicks,field, query):
#     # if n_clicks is not None and n_clicks > 0:
#     if n_clicks:
#         fig = graph_rank(query, field)
#         return fig
#     else:
#         return dash.no_update
def update_rank_graph(query, field):
    fig = graph_rank(query, field)
    return fig


@app.callback(
    # Output('count-graph', 'figure'),
    # Input('search-button2', 'n-clicks'),
    # Input('search-field2', 'value'),
    # State('search-input2', 'value'),
    Output('count-graph', 'figure'),
    # Input('search-button2', 'n-clicks'),
    Input('search-input2', 'value'),
    Input('search-field2', 'value'),
    
)

# def update_count_graph(n_clicks,field, query):
#     # if n_clicks is not None and n_clicks > 0:
#     if n_clicks:    
#         fig = graph_count(query, field)
#         return fig
#     else:
#         return dash.no_update
def update_count_graph(query, field):
    fig = graph_count(query, field)
    return fig
    
@app.callback(
    Output('classement-graph', 'figure'),
    Input('size-slider', 'value'),
    Input('search-field3', 'value')
)
def update_classement_graph(size, field):
    fig = graph_classement(size, field)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False,port=8051) # RUN APP