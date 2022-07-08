from enum import unique
from flask import Flask, request, jsonify, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import psycopg2

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['WTF_CSRF_ENABLED']= False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Cedula(db.Model):
    __tablename__ = 'Cedula'
    ID_cedula = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    ID_elector_cedula = db.Column(db.String(15), db.ForeignKey('Elector.ID_elector'), nullable=False, unique=True)
    ID_partido_politico_cedula = db.Column(db.String(10), db.ForeignKey('Partido_politico.ID_siglas_partido_politico'), nullable=False)
    ID_candidato_cedula = db.Column(db.Integer, db.ForeignKey('Candidato.ID_candidato'), nullable=False)
    ID_ubigeo_cedula = db.Column(db.String(6), db.ForeignKey('Ubigeo.ID_ubigeo'), nullable=False)
    Fecha_cedula_voto = db.Column(db.DateTime, nullable=False)
    ID_eleccion = db.Column(db.Integer, db.ForeignKey('Elecciones.ID_eleccion'), nullable=False)
 
    def __init__(self, ID_cedula,ID_elector_cedula, ID_partido_politico_cedula, ID_candidato_cedula, ID_ubigeo_cedula, Fecha_cedula_voto, ID_eleccion):
        self.ID_cedula = ID_cedula
        self.ID_elector_cedula = ID_elector_cedula
        self.ID_partido_politico_cedula = ID_partido_politico_cedula
        self.ID_candidato_cedula = ID_candidato_cedula
        self.ID_ubigeo_cedula = ID_ubigeo_cedula
        self.Fecha_cedula_voto = Fecha_cedula_voto
        self.ID_eleccion = ID_eleccion

db.create_all()

class Cedula_schema(ma.Schema):
    class Meta:
        fields = ('ID_cedula', 'ID_elector_cedula', 'ID_partido_politico_cedula', 'ID_candidato_cedula', 'ID_ubigeo_cedula', 'Fecha_cedula_voto', 'ID_eleccion')
cedula_schema = Cedula_schema()
cedulas_schema = Cedula_schema(many=True)

@app.route('/cedula', methods=['POST'])
@cross_origin()
def add_cedula():
    ID_cedula = request.json['ID_cedula']
    ID_elector_cedula = request.json['ID_elector_cedula']
    ID_partido_politico_cedula = request.json['ID_partido_politico_cedula']
    ID_candidato_cedula = request.json['ID_candidato_cedula']
    ID_ubigeo_cedula = request.json['ID_ubigeo_cedula']
    Fecha_cedula_voto = request.json['Fecha_cedula_voto']
    ID_eleccion = request.json['ID_eleccion']

    nuevo_cedula = Cedula(ID_cedula, ID_elector_cedula, ID_partido_politico_cedula, ID_candidato_cedula, ID_ubigeo_cedula, Fecha_cedula_voto, ID_eleccion)

    db.session.add(nuevo_cedula)
    db.session.commit()
        
    return cedula_schema.jsonify(nuevo_cedula)

@app.route('/cedula', methods=['GET'])
@cross_origin()
def get_cedulas():
    cedulas = Cedula.query.all()
    return cedulas_schema.jsonify(cedulas)

@app.route('/cedula/<ID_cedula>', methods=['GET'])
@cross_origin()
def get_cedula(ID_cedula):
    cedula = Cedula.query.get(ID_cedula)
    return cedula_schema.jsonify(cedula)
