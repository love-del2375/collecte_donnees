from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    poids = db.Column(db.Float, nullable=False)
    taille = db.Column(db.Float, nullable=False)
    tension = db.Column(db.Integer, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    categorie = db.Column(db.String(20), nullable=False)