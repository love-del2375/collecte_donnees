from flask import Flask, render_template, request
from models import db, Patient
import statistics
import plotly.express as px
import plotly.io as pio
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


def classification_imc(imc):
    if imc < 18.5:
        return "Maigreur"
    elif 18.5 <= imc < 25:
        return "Normal"
    elif 25 <= imc < 30:
        return "Surpoids"
    else:
        return "Obésité"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    graph_imc = None
    graph_tension = None
    graph_corr = None

    if request.method == "POST":
        age = int(request.form["age"])
        poids = float(request.form["poids"])
        taille = float(request.form["taille"]) / 100  # cm → m
        tension = int(request.form["tension"])

        imc = round(poids / (taille ** 2), 2)
        categorie = classification_imc(imc)

        patient = Patient(age=age, poids=poids, taille=taille,
                          tension=tension, imc=imc, categorie=categorie)
        db.session.add(patient)
        db.session.commit()

    patients = Patient.query.all()

    if patients:
        imcs = [p.imc for p in patients]
        tensions = [p.tension for p in patients]
        ages = [p.age for p in patients]

        result = {
            "moyenne_imc": round(statistics.mean(imcs), 2),
            "moyenne_tension": round(statistics.mean(tensions), 2),
            "nb_participants": len(patients)
        }

        fig_imc = px.histogram(imcs, nbins=10,
                               title="Distribution des IMC",
                               labels={"value": "IMC"})
        graph_imc = pio.to_html(fig_imc, full_html=False)

        fig_tension = px.histogram(tensions, nbins=10,
                                   title="Distribution des tensions artérielles",
                                   labels={"value": "Tension (mmHg)"})
        graph_tension = pio.to_html(fig_tension, full_html=False)

        if len(patients) > 2:
            fig_corr = px.scatter(x=ages, y=imcs, trendline="ols",
                                  labels={"x": "Âge", "y": "IMC"},
                                  title="Corrélation Âge ↔ IMC (régression linéaire)")
            graph_corr = pio.to_html(fig_corr, full_html=False)

    return render_template("index.html",
                           result=result,
                           patients=patients,
                           graph_imc=graph_imc,
                           graph_tension=graph_tension,
                           graph_corr=graph_corr)


@app.route("/rapport")
def rapport():
    patients = Patient.query.all()
    imcs = [p.imc for p in patients]
    tensions = [p.tension for p in patients]

    stats = {
        "moyenne_imc": round(statistics.mean(imcs), 2) if imcs else 0,
        "moyenne_tension": round(statistics.mean(tensions), 2) if tensions else 0,
        "nb_participants": len(patients)
    }

    return render_template("rapport.html", patients=patients, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))