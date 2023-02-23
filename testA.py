from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = pd.read_csv("dataframe_finale.csv", sep=";")
    if request.method == "POST":
        query = request.form["genre"]
        results = data.query('Genre.str.contains(@query, na=False)', engine='python')
        return render_template("index.html",  table=results.to_html(classes="table", index=False, table_id="table"))
    return render_template("index.html", table=data.to_html(classes="table", index=False, table_id="table"))

if __name__ == "__main__":
    app.run()

#Lancer la page (pour l'instant) avec la commande "flask --app testA run"