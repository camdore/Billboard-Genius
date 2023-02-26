import time 
import datetime
from datetime import date
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
import re
from flask import Flask, render_template, request
import plotly.express as px


start_time = time.time()

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

def graphsong_rank(query,field):
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


    fig = px.line(x=x_values,y=y_values, title=f"Evolution du Average Rank de {query} de au cours des semaines")
    fig.update_layout(
        xaxis_title="Dates by Weeks",
        yaxis_title="Average Rank"
    )
    fig.update_yaxes(autorange="reversed")
    fig_json = fig.to_json()

    return fig_json

##################################################### FLASK APP ##########################################################
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        field = request.form.get('field')
        results = search(query, field)
        infos = searchinfos(query,field)
        plot1 = graphsong_rank(query,field)
        return render_template('index.html', results=results, infos=infos, plot = plot1)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


# Lancer la page (pour l'instant) avec la commande "flask --app TestB run"

end_time = time.time()
execution_time = end_time - start_time

print("Temps d'exécution : ", execution_time, " secondes")