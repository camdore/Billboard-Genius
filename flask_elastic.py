from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re 
import pandas as pd
import plotly.express as px

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
            "_index": "billboard",
            "_type": "song",
            "_source": {k:v if v else None for k,v in docu.items()},
        }
        
if es.indices.exists('billboard')==True:
    es.indices.delete(index='billboard')
    bulk(es, generate_data(data))
else :
    bulk(es, generate_data(data))

################################### APP FLASK ###############################################
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        field = request.form.get('field')
        results = search(query, field)
        infos = searchinfos(query,field)
        return render_template('index2.html', results=results, infos=infos)
    else:
        return render_template('index2.html')

def search(query, field):
    QUERY ={
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
    result = es.search(index="billboard", body=QUERY,size=4200)

    results = []
    [results.append(elt['_source']) for elt in result["hits"]["hits"]]

    return results

def searchinfos(query, field):
    QUERY ={
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
    result = es.search(index="billboard", body=QUERY,size=4200)

    results = []
    [results.append(elt['_source']) for elt in result["hits"]["hits"]]

    N_DOCS = result['hits']['total']['value']
    infos = f"{N_DOCS} document{'s' if N_DOCS> 1 else '' } correspondent à la requête qui a pris {result['took']} ms"

    return infos

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
    result = es.search(index="billboard", body=QUERY)

    x_values, y_values = [],[]
    for i in range(len(result["aggregations"]["2"]["buckets"])):
        aggregations_x = result["aggregations"]["2"]["buckets"][i]['key_as_string']
        aggregations_y = result["aggregations"]["2"]["buckets"][i]['1']['value']
        x_values.append(aggregations_x)
        y_values.append(aggregations_y)


    fig = px.line(x=x_values,y=y_values, title=f"Evolution du rang de {query} de au cours des semaines")
    # title="Evolution du rang de chanson au cours des semaines")
    fig.update_layout(
        xaxis_title="Dates by Weeks",
        yaxis_title="Average Rank"
    )
    fig.update_yaxes(autorange="reversed")
    fig_json = fig.to_json()

    return fig_json

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
    
    result = es.search(index="billboard", body=QUERY)
    x_values, y_values = [],[]
    for i in range(len(result["aggregations"]["2"]["buckets"])):
        aggregations_x = result["aggregations"]["2"]["buckets"][i]['key_as_string']
        aggregations_y = result["aggregations"]["2"]["buckets"][i]['doc_count']
        x_values.append(aggregations_x)
        y_values.append(aggregations_y)


    fig = px.line(x=x_values,y=y_values,title=f"Evolution du nombre de chanson de {query} au cours des semaines")
    fig.update_layout(
        xaxis_title="Dates by Weeks",
        yaxis_title="Count"
    )

    fig_json2 = fig.to_json()

    return fig_json2


# # Convert plotly data to JSON format for rendering in template
#     plot_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

#     # Render template with plotly bar chart
#     return render_template('search.html', plot=plot_json)

if __name__ == '__main__':
    app.run(debug=True)


# Lancer la page (pour l'instant) avec la commande "flask --app flask_elastic run"