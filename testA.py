from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = pd.read_csv("dataframe_finale.csv", sep=";")
    if request.method == "POST":
        query = request.form["query"]
        # Récupérer les colonnes sélectionnées
        columns = []
        if request.form.get("title"):
            columns.append("Title")
        if request.form.get("artist"):
            columns.append("Artist")
        if request.form.get("distributor"):
            columns.append("Distributor")
        if request.form.get("producers"):
            columns.append("Producers")
        if request.form.get("genre"):
            columns.append("Genre")

        # Filtrer les résultats en fonction des colonnes sélectionnées

        if len(columns) > 0:
            results = pd.DataFrame(columns=data.columns)
            for col in columns:
                results = results.append(data[data[col].str.contains(query, na=False)])
        else:
            results = data[data.apply(lambda row: row.str.contains(query, na=False)).any(axis=1)]
        # Retourner le résultat filtré sous forme de tableau HTML
        return render_template("index.html", table=results.to_html(classes="table", index=False, table_id="table"))
    # Retourner le tableau complet par défaut
    return render_template("index.html", table=data.to_html(classes="table", index=False, table_id="table"))

if __name__ == "__main__":
    app.run()



#Lancer la page (pour l'instant) avec la commande "flask --app testA run"