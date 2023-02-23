from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    data = pd.read_csv("dataframe_finale.csv", sep=";")
    return render_template("index.html", data=data.to_html())

if __name__ == "__main__":
    app.run()

#Lancer la page (pour l'instant) avec la commande "flask --app testA run"