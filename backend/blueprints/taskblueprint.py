import os
from flask import Flask, flash, request, redirect, render_template
from flask import Blueprint
from flask import jsonify
from werkzeug.utils import secure_filename

from flask_cors import CORS, cross_origin # para que no genere errores de CORS al hacer peticiones

#from backend.models.task_model import TaskModel
#model = TaskModel()

model = None

task_blueprint = Blueprint('task_blueprint', __name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Creando un usuario
@task_blueprint.route('/create_usuario', methods=['POST'])
@cross_origin()
def create_usuario():
    content = model.create_usuario(request.json['usuarionombre'], request.json['usuarioapellidos'], 
        request.json['usuariodni'], request.json['usuariodireccion'], request.json['usuarioedad'], 
        request.json['usuariofechanacimiento'], request.json['usuariodniemision'], request.json['usuariogenero'],
        request.json['usuarioalias'], request.json['usuariocontraseña'], request.json['usuarioemail'])
    return jsonify(content)

#Creando un candidato
@task_blueprint.route('/create_candidate', methods=['POST'])
@cross_origin()
def create_candidate():
    content = model.create_candidate(request.json['id_usuario'], request.json['candidatepartido'], 
        request.json['candidateocupacion'], request.json['candidatesentencias'])    
    return jsonify(content)

#Creando un votante
@task_blueprint.route('/create_votante', methods=['POST'])
@cross_origin()
def create_votante():
    content = model.create_votante(request.json['nombrevotante'], request.json['apellidovotante'], request.json['dnivotante'], request.json['numerosala'], request.json['numeromesa'], request.json['numeroorden'], request.json['localdevotacion'])    
    return jsonify(content)

#Creando un voto
@task_blueprint.route('/create_voto', methods=['POST'])
@cross_origin()
def create_voto():
    content = model.create_voto(request.json['usuariovoto'], request.json['partidovoto'], 
        request.json['candidatovoto'], request.json['dnivoto'], request.json['fechavoto'],
        request.json['lugarvoto'])
    # id_votanteB = request.form["id_votante"]
    # dni_votoB = request.form["dni_voto"]
    # imagen_votoB = request.form["imagen_voto"]
    # model.update_voto(dni_votoB, imagen_votoB)
    return jsonify(content)

#Creando un mapa
@task_blueprint.route('/create_mapa', methods=['POST'])
@cross_origin()
def create_mapa():
    content = model.create_mapa(request.json['mapa_departamento'], request.json['mapa_provincia'], 
        request.json['mapa_distrito'], request.json['mapa_coordenadas'])
    # id_votanteB = request.form["id_votante"]
    # dni_votoB = request.form["dni_voto"]
    # imagen_votoB = request.form["imagen_voto"]
    # model.update_voto(dni_votoB, imagen_votoB)
    return jsonify(content)

#Mostrando los usuarios con sus respectivos datos
@task_blueprint.route('/usuarios', methods=['GET'])
@cross_origin()
def usuarios():
    return jsonify(model.usuarios())

#Mostrando los candidatos con sus respectivos datos
@task_blueprint.route('/candidatos', methods=['GET'])
@cross_origin()
def candidatos():
    return jsonify(model.candidatos())

#Mostrando los votantes con sus respectivos datos
@task_blueprint.route('/votantes', methods=['GET'])
@cross_origin()
def votantes():
    return jsonify(model.votantes())

#Mostrando los votos con sus respectivos datos
@task_blueprint.route('/votos', methods=['GET'])
@cross_origin()
def voto():
    return jsonify(model.voto())