from enum import unique
from flask import Flask, request, jsonify, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['WTF_CSRF_ENABLED']= False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# conn = psycopg2.connect(database="flaskmysql", user="root", password="", host="localhost", port="5432")
# cursor = conn.cursor()

# -----------------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    response = make_response(redirect('/hello'))
    return response

@app.route('/hello', methods=['GET', 'POST'])
def hello ():
    return'Bienvenido a mi API'

# ------------------------------------------------------------------------------------------------------------------------------------

#tabla departamento
class Departamento(db.Model):
    __tablename__ = 'Departamento'
    ID_departamento = db.Column(db.String(2), autoincrement=False, unique=True, nullable=False)
    Nombre_departamento = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)

    def __init__(self, ID_departamento, Nombre_departamento):
        self.ID_departamento = ID_departamento
        self.Nombre_departamento = Nombre_departamento

db.create_all()

class DepartamentoSchema(ma.Schema):
    class Meta:
        fields = ('ID_departamento', 'Nombre_departamento')

Departamento_schema = DepartamentoSchema()
Departamentos_schema = DepartamentoSchema(many=True)

@app.route('/departamento', methods=['POST'])
def add_departamento():
    ID_departamento = request.json['ID_departamento']
    Nombre_departamento = request.json['Nombre_departamento']

    new_departamento = Departamento(ID_departamento, Nombre_departamento)

    db.session.add(new_departamento)
    db.session.commit()
    return Departamento_schema.jsonify(new_departamento)

@app.route('/departamento', methods=['GET'])
def get_departamento():
    all_departamentos = Departamento.query.all()
    result = Departamentos_schema.dump(all_departamentos)
    return jsonify(result)

@app.route('/departamento/<Nombre_departamento>', methods=['GET'])
def get_departamento_by_name(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)
    return Departamento_schema.jsonify(departamento)

@app.route('/departamento/<Nombre_departamento>', methods=['PUT'])
def update_departamento(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)

    Nombre_departamento = request.json['Nombre_departamento']

    departamento.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return Departamento_schema.jsonify(departamento)

@app.route('/departamento/<Nombre_departamento>', methods=['DELETE'])
def delete_departamento(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)
    db.session.delete(departamento)
    db.session.commit()

    return 'Departamento eliminado'

# ------------------------------------------------------------------------------------------------------------------------------------
    
#tabla provincia

class Provincia(db.Model):
    __tablename__ = 'Provincia'
    ID_provincia = db.Column(db.String(4), unique=False, autoincrement=False, nullable=False)
    Nombre_provincia = db.Column(db.String(100), primary_key=True, unique=False, nullable=False)
    Nombre_departamento = db.Column(db.String(100), db.ForeignKey('Departamento.Nombre_departamento'), nullable=False)
    
    def __init__(self, ID_provincia, Nombre_provincia, Nombre_departamento):
        self.ID_provincia = ID_provincia
        self.Nombre_provincia = Nombre_provincia
        self.Nombre_departamento = Nombre_departamento
       

db.create_all()

class ProvinciaSchema(ma.Schema):
    class Meta:
        fields = ('ID_provincia', 'Nombre_provincia', 'Nombre_departamento')

provinciaSchema = ProvinciaSchema()
provinciasSchema = ProvinciaSchema(many=True)

@app.route('/provincia', methods=['POST'])
def add_provincia():
    ID_provincia = request.json['ID_provincia']
    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    new_provincia = Provincia(ID_provincia, Nombre_provincia, Nombre_departamento)

    db.session.add(new_provincia)
    db.session.commit()
    return provinciaSchema.jsonify(new_provincia)

@app.route('/provincia', methods=['GET'])
def get_provincia():
    all_provincias = Provincia.query.all()
    result = provinciasSchema.dump(all_provincias)
    return jsonify(result)

@app.route('/provincia/<Nombre_provincia>', methods=['GET'])
def get_provincia_by_name(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<ID_provincia>', methods=['GET'])
def get_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<Nombre_provincia>', methods=['PUT'])
def update_provincia(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)

    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    provincia.Nombre_provincia = Nombre_provincia
    provincia.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<ID_provincia>', methods=['PUT'])
def update_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()

    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    provincia.Nombre_provincia = Nombre_provincia
    provincia.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return provinciaSchema.jsonify(provincia)


@app.route('/provincia/<Nombre_provincia>', methods=['DELETE'])
def delete_provincia(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)
    db.session.delete(provincia)
    db.session.commit()

    return 'Provincia eliminada'

@app.route('/provincia/<ID_provincia>', methods=['DELETE'])
def delete_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()
    db.session.delete(provincia)
    db.session.commit()

    return 'Provincia eliminada'



# ------------------------------------------------------------------------------------------------------------------------------------

#tabla UBIGEO
class Ubigeo(db.Model):
    __tablename__ = 'Ubigeo'
    ID_ubigeo = db.Column(db.String(6), primary_key=True, unique=False, nullable=False)
    Nombre_departamento = db.Column(db.String(100), db.ForeignKey('Departamento.Nombre_departamento'), nullable=False, unique=False)
    Nombre_provincia = db.Column(db.String(100), db.ForeignKey('Provincia.Nombre_provincia'), nullable=False, unique=False)
    Nombre_distrito = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, ID_ubigeo, Nombre_departamento, Nombre_provincia, Nombre_distrito):
        self.ID_ubigeo = ID_ubigeo
        self.Nombre_departamento = Nombre_departamento
        self.Nombre_provincia = Nombre_provincia
        self.Nombre_distrito = Nombre_distrito
db.create_all()

class UbigeoSchema(ma.Schema):
    class Meta:
        fields = ('ID_ubigeo', 'Nombre_departamento', 'Nombre_provincia', 'Nombre_distrito')
ubigeoSchema = UbigeoSchema()
ubigeosSchema = UbigeoSchema(many=True)

@app.route('/ubigeo', methods=['POST'])
def add_ubigeo():
    ID_ubigeo = request.json['ID_ubigeo']
    Nombre_departamento = request.json['Nombre_departamento']
    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_distrito = request.json['Nombre_distrito']

    new_ubigeo = Ubigeo(ID_ubigeo, Nombre_departamento, Nombre_provincia, Nombre_distrito)

    db.session.add(new_ubigeo)
    db.session.commit()
    return ubigeoSchema.jsonify(new_ubigeo)

@app.route('/ubigeo', methods=['GET'])
def get_ubigeo():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeosSchema.dump(all_ubigeos)
    return jsonify(result)

@app.route('/ubigeo/<ID_ubigeo>', methods=['GET'])
def get_ubigeo_by_id(ID_ubigeo):
    ubigeo = Ubigeo.query.get(ID_ubigeo)
    return ubigeoSchema.jsonify(ubigeo)

@app.route('/ubigeo/<ID_ubigeo>', methods=['PUT'])
def update_ubigeo(ID_ubigeo):
    ubigeo = Ubigeo.query.get(ID_ubigeo)

    ID_ubigeo = request.json['ID_ubigeo']
    Nombre_departamento = request.json['Nombre_departamento']
    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_distrito = request.json['Nombre_distrito']

    ubigeo.ID_ubigeo = ID_ubigeo
    ubigeo.Nombre_departamento = Nombre_departamento
    ubigeo.Nombre_provincia = Nombre_provincia
    ubigeo.Nombre_distrito = Nombre_distrito

    db.session.commit()
    return ubigeoSchema.jsonify(ubigeo)

@app.route('/ubigeo/<ID_ubigeo>', methods=['DELETE'])
def delete_ubigeo(ID_ubigeo):
    ubigeo = Ubigeo.query.get(ID_ubigeo)
    db.session.delete(ubigeo)
    db.session.commit()

    return 'Ubigeo eliminado'


# ------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------
# tabla elector
class Elector(db.Model):
    __tablename__ = 'Elector'
    ID_elector = db.Column(db.String(15), primary_key=True, unique=True)
    DNI_elector = db.Column(db.Integer, unique=True, nullable=False, autoincrement=False)
    Nombre_elector = db.Column(db.String(70), nullable=False)
    Apellidos_elector = db.Column(db.String(70), nullable=False)
    Estado_elector = db.Column(db.Boolean, default=False)
    Tipo_elector = db.Column(db.String(70), nullable=False)
    Email_elector = db.Column(db.String(70), nullable=False)
    Telefono_elector = db.Column(db.Integer)
    Nacimiento_elector = db.Column(db.Date, nullable=False)
    Genero_elector = db.Column(db.String(70), nullable=False)
    Password_elector = db.Column(db.String(70), nullable=False)
    Direccion_elector = db.Column(db.String(70), nullable=False)
    Departamento_elector = db.Column(db.String(100), db.ForeignKey('Departamento.Nombre_departamento'), nullable=False, unique=False)
    ID_ubigeo_elector = db.Column(db.String(6), db.ForeignKey('Ubigeo.ID_ubigeo'), nullable=False, unique=False)

    def __init__(self, ID_elector, DNI_elector, Nombre_elector, Apellidos_elector, Estado_elector, Tipo_elector, Email_elector, Telefono_elector, Nacimiento_elector, Genero_elector, Password_elector, Direccion_elector, Departamento_elector, ID_ubigeo_elector):
        self.ID_elector = ID_elector
        self.DNI_elector = DNI_elector
        self.Nombre_elector = Nombre_elector
        self.Apellidos_elector = Apellidos_elector
        self.Estado_elector = Estado_elector
        self.Tipo_elector = Tipo_elector
        self.Email_elector = Email_elector
        self.Telefono_elector = Telefono_elector
        self.Nacimiento_elector = Nacimiento_elector
        self.Genero_elector = Genero_elector
        self.Password_elector = Password_elector
        self.Direccion_elector = Direccion_elector
        self.Departamento_elector = Departamento_elector
        self.ID_ubigeo_elector = ID_ubigeo_elector

db.create_all()

class ElectorSchema(ma.Schema):
    class Meta:
        fields = ('ID_elector', 'DNI_elector', 'Nombre_elector', 'Apellidos_elector', 'Estado_elector', 'Tipo_elector', 'Email_elector', 'Telefono_elector', 'Nacimiento_elector', 'Genero_elector', 'Password_elector', 'Direccion_elector', 'Departamento_elector', 'ID_ubigeo_elector')

electorSchema = ElectorSchema()
electoresSchema = ElectorSchema(many=True)

@app.route('/elector', methods=['POST'])
def add_elector():
    ID_elector = request.json['ID_elector']
    DNI_elector = request.json['DNI_elector']
    Nombre_elector = request.json['Nombre_elector']
    Apellidos_elector = request.json['Apellidos_elector']
    Estado_elector = request.json['Estado_elector']
    Tipo_elector = request.json['Tipo_elector']
    Email_elector = request.json['Email_elector']
    Telefono_elector = request.json['Telefono_elector']
    Nacimiento_elector = request.json['Nacimiento_elector']
    Genero_elector = request.json['Genero_elector']
    Password_elector = request.json['Password_elector']
    Direccion_elector = request.json['Direccion_elector']
    Departamento_elector = request.json['Departamento_elector']
    ID_ubigeo_elector = request.json['ID_ubigeo_elector']

    nuevo_elector = Elector(ID_elector, DNI_elector, Nombre_elector, Apellidos_elector, Estado_elector, Tipo_elector, Email_elector, Telefono_elector, Nacimiento_elector, Genero_elector, Password_elector, Direccion_elector, Departamento_elector, ID_ubigeo_elector)
    db.session.add(nuevo_elector)
    db.session.commit()

    return electorSchema.jsonify(nuevo_elector)


@app.route('/elector', methods=['GET'])
def get_elector():
    all_elector = Elector.query.all()
    result = electoresSchema.dump(all_elector)
    return jsonify(result)

@app.route('/elector/<ID_elector>', methods=['GET'])
def get_elector_by_id(ID_elector):
    elector = Elector.query.get(ID_elector)
    return electorSchema.jsonify(elector)

@app.route('/elector/<DNI_elector>', methods=['GET'])
def get_elector_by_dni(DNI_elector):
    elector = Elector.query.filter_by(DNI_elector=DNI_elector).first()
    return electorSchema.jsonify(elector)

@app.route('/elector/<ID_elector>', methods=['PUT'])
def update_elector(ID_elector):
    elector = Elector.query.get(ID_elector)

    ID_elector = request.json['ID_elector']
    DNI_elector = request.json['DNI_elector']
    Nombre_elector = request.json['Nombre_elector']
    Apellidos_elector = request.json['Apellidos_elector']
    Estado_elector = request.json['Estado_elector']
    Tipo_elector = request.json['Tipo_elector']
    Email_elector = request.json['Email_elector']
    Telefono_elector = request.json['Telefono_elector']
    Nacimiento_elector = request.json['Nacimiento_elector']
    Genero_elector = request.json['Genero_elector']
    Password_elector = request.json['Password_elector']
    Direccion_elector = request.json['Direccion_elector']
    Departamento_elector = request.json['Departamento_elector']
    ID_ubigeo_elector = request.json['ID_ubigeo_elector']

    elector.ID_elector = ID_elector
    elector.DNI_elector = DNI_elector
    elector.Nombre_elector = Nombre_elector
    elector.Apellidos_elector = Apellidos_elector
    elector.Estado_elector = Estado_elector
    elector.Tipo_elector = Tipo_elector
    elector.Email_elector = Email_elector
    elector.Telefono_elector = Telefono_elector
    elector.Nacimiento_elector = Nacimiento_elector
    elector.Genero_elector = Genero_elector
    elector.Password_elector = Password_elector
    elector.Direccion_elector = Direccion_elector
    elector.Departamento_elector = Departamento_elector
    elector.ID_ubigeo_elector = ID_ubigeo_elector

    db.session.commit()
    return electorSchema.jsonify(elector)

@app.route('/elector/<ID_elector>', methods=['DELETE'])
def delete_elector(ID_elector):
    elector = Elector.query.get(ID_elector)
    db.session.delete(elector)
    db.session.commit()
    return electorSchema.jsonify(elector)

# ------------------------------------------------------------------------------------------------------------------------------------

#tabla de partido politico
class Partido_politico(db.Model):
    __tablename__ = 'Partido_politico'
    ID_siglas_partido_politico = db.Column(db.String(10), primary_key=True, unique=True)
    Nombre_partido_politico = db.Column(db.String(50), nullable=False, unique=True)
    Foto_partido_politico = db.Column(db.String(500), nullable=False, unique=True)
    Direción_partido_politico = db.Column(db.String(100), nullable=False, unique=False)
    Web_partido_politico = db.Column(db.String(100), nullable=False, unique=True)
    Nombre_departamento = db.Column(db.String(100), db.ForeignKey('Departamento.Nombre_departamento'), nullable=False, unique=False)
    ID_ubigeo = db.Column(db.String(6), db.ForeignKey('Ubigeo.ID_ubigeo'), nullable=False, unique=False)

    def __init__(self, ID_siglas_partido_politico, Nombre_partido_politico, Foto_partido_politico, Direción_partido_politico, Web_partido_politico, Nombre_departamento, ID_ubigeo):
        self.ID_siglas_partido_politico = ID_siglas_partido_politico
        self.Nombre_partido_politico = Nombre_partido_politico
        self.Foto_partido_politico = Foto_partido_politico
        self.Direción_partido_politico = Direción_partido_politico
        self.Web_partido_politico = Web_partido_politico
        self.Nombre_departamento = Nombre_departamento
        self.ID_ubigeo = ID_ubigeo

db.create_all()

class Partido_politico_schema(ma.Schema):
    class Meta:
        fields = ('ID_siglas_partido_politico', 'Nombre_partido_politico', 'Foto_partido_politico', 'Direción_partido_politico', 'Web_partido_politico', 'Nombre_departamento', 'ID_ubigeo')
partido_politico_schema = Partido_politico_schema()
partidos_politicos_schema = Partido_politico_schema(many=True)

@app.route('/partido_politico', methods=['POST'])
def add_partido_politico():
    ID_siglas_partido_politico = request.json['ID_siglas_partido_politico']
    Nombre_partido_politico = request.json['Nombre_partido_politico']
    Foto_partido_politico = request.json['Foto_partido_politico']
    Direción_partido_politico = request.json['Direción_partido_politico']
    Web_partido_politico = request.json['Web_partido_politico']
    Nombre_departamento = request.json['Nombre_departamento']
    ID_ubigeo = request.json['ID_ubigeo']

    nuevo_partido_politico = Partido_politico(ID_siglas_partido_politico, Nombre_partido_politico, Foto_partido_politico, Direción_partido_politico, Web_partido_politico, Nombre_departamento, ID_ubigeo)

    db.session.add(nuevo_partido_politico)
    db.session.commit()
        
    return partido_politico_schema.jsonify(nuevo_partido_politico)

@app.route('/partido_politico', methods=['GET'])
def get_partido_politico():
    all_partido_politico = Partido_politico.query.all()
    result = partidos_politicos_schema.dump(all_partido_politico)
    return jsonify(result)

@app.route('/partido_politico/<ID_siglas_partido_politico>', methods=['GET'])
def get_partido_politico_by_id(ID_siglas_partido_politico):
    partido_politico = Partido_politico.query.get(ID_siglas_partido_politico)
    return partido_politico_schema.jsonify(partido_politico)

@app.route('/partido_politico/<ID_siglas_partido_politico>', methods=['PUT'])
def update_partido_politico(ID_siglas_partido_politico):
    partido_politico = Partido_politico.query.get(ID_siglas_partido_politico)

    ID_siglas_partido_politico = request.json['ID_siglas_partido_politico']
    Nombre_partido_politico = request.json['Nombre_partido_politico']
    Foto_partido_politico = request.json['Foto_partido_politico']
    Direción_partido_politico = request.json['Direción_partido_politico']
    Web_partido_politico = request.json['Web_partido_politico']
    Nombre_departamento = request.json['Nombre_departamento']
    ID_ubigeo = request.json['ID_ubigeo']

    partido_politico.ID_siglas_partido_politico = ID_siglas_partido_politico
    partido_politico.Nombre_partido_politico = Nombre_partido_politico
    partido_politico.Foto_partido_politico = Foto_partido_politico
    partido_politico.Direción_partido_politico = Direción_partido_politico
    partido_politico.Web_partido_politico = Web_partido_politico
    partido_politico.Nombre_departamento = Nombre_departamento
    partido_politico.ID_ubigeo = ID_ubigeo

    db.session.commit()
    return partido_politico_schema.jsonify(partido_politico)

@app.route('/partido_politico/<ID_siglas_partido_politico>', methods=['DELETE'])
def delete_partido_politico(ID_siglas_partido_politico):
    partido_politico = Partido_politico.query.get(ID_siglas_partido_politico)
    db.session.delete(partido_politico)
    db.session.commit()

    return partido_politico_schema.jsonify(partido_politico)
# ------------------------------------------------------------------------------------------------------------------------------------

# tabla candidato

class Candidato(db.Model):
    __tablename__ = 'Candidato'
    ID_candidato = db.Column(db.Integer, primary_key=True, unique=False, nullable=True, autoincrement=False)
    ID_candidato_elector = db.Column(db.String(15), db.ForeignKey('Elector.ID_elector'), nullable=False)
    DNI_candidato_elector = db.Column(db.Integer, db.ForeignKey('Elector.DNI_elector'), nullable=False)
    ID_partido_politico = db.Column(db.String(10), db.ForeignKey('Partido_politico.ID_siglas_partido_politico'), nullable=False)
    Nombre_candidato_elector = db.Column(db.String(70), nullable=False)
    Apellidos_candidato_elector = db.Column(db.String(70), nullable=False)
    Foto_candidato = db.Column(db.String(500), unique=True, nullable=False)
    Hoja_de_vida_candidato = db.Column(db.String(500), nullable=True)
    Propuesta_candidato = db.Column(db.String(500), nullable=True)
    Nombre_departamento = db.Column(db.String(100), db.ForeignKey('Departamento.Nombre_departamento'), nullable=False)

    def __init__(self, ID_candidato, ID_candidato_elector, DNI_candidato_elector, Nombre_candidato_elector, Apellidos_candidato_elector, Foto_candidato, Hoja_de_vida_candidato, Propuesta_candidato, ID_partido_politico, Nombre_departamento):
        self.ID_candidato = ID_candidato
        self.ID_candidato_elector = ID_candidato_elector
        self.DNI_candidato_elector = DNI_candidato_elector
        self.Nombre_candidato_elector = Nombre_candidato_elector
        self.Apellidos_candidato_elector = Apellidos_candidato_elector
        self.Foto_candidato = Foto_candidato
        self.Hoja_de_vida_candidato = Hoja_de_vida_candidato
        self.Propuesta_candidato = Propuesta_candidato
        self.ID_partido_politico = ID_partido_politico
        self.Nombre_departamento = Nombre_departamento

db.create_all()

class Candidato_schema(ma.Schema):
    class Meta:
        fields = ('ID_candidato', 'ID_candidato_elector', 'DNI_candidato_elector', 'Nombre_candidato_elector', 'Apellidos_candidato_elector', 'Foto_candidato', 'Hoja_de_vida_candidato', 'Propuesta_candidato', 'ID_partido_politico', 'Nombre_departamento')
candidato_schema = Candidato_schema()
candidatos_schema = Candidato_schema(many=True)


@app.route('/candidato', methods=['POST'])
def add_candidato():
    ID_candidato = request.json['ID_candidato']
    ID_candidato_elector = request.json['ID_candidato_elector']
    DNI_candidato_elector = request.json['DNI_candidato_elector']
    Nombre_candidato_elector = request.json['Nombre_candidato_elector']
    Apellidos_candidato_elector = request.json['Apellidos_candidato_elector']
    Foto_candidato = request.json['Foto_candidato']
    Hoja_de_vida_candidato = request.json['Hoja_de_vida_candidato']
    Propuesta_candidato = request.json['Propuesta_candidato']
    ID_partido_politico = request.json['ID_partido_politico']
    Nombre_departamento = request.json['Nombre_departamento']

    nuevo_candidato = Candidato(ID_candidato, ID_candidato_elector, DNI_candidato_elector, Nombre_candidato_elector, Apellidos_candidato_elector, Foto_candidato, Hoja_de_vida_candidato, Propuesta_candidato, ID_partido_politico, Nombre_departamento)

    db.session.add(nuevo_candidato)
    db.session.commit()
        
    return candidato_schema.jsonify(nuevo_candidato)


@app.route('/candidato', methods=['GET'])
def get_candidato():
    all_candidatos = Candidato.query.all()
    result = candidatos_schema.dump(all_candidatos)
    return jsonify(result)

@app.route('/candidato/<ID_candidato>', methods=['GET'])
def get_candidato_by_id(ID_candidato):
    candidato = Candidato.query.get(ID_candidato)
    return candidato_schema.jsonify(candidato)

@app.route('/candidato/<ID_candidato>', methods=['PUT'])
def update_candidato(ID_candidato):
    candidato = Candidato.query.get(ID_candidato)

    ID_candidato = request.json['ID_candidato']
    ID_candidato_elector = request.json['ID_candidato_elector']
    DNI_candidato_elector = request.json['DNI_candidato_elector']
    Nombre_candidato_elector = request.json['Nombre_candidato_elector']
    Apellidos_candidato_elector = request.json['Apellidos_candidato_elector']
    Foto_candidato = request.json['Foto_candidato']
    Hoja_de_vida_candidato = request.json['Hoja_de_vida_candidato']
    Propuesta_candidato = request.json['Propuesta_candidato']
    ID_partido_politico = request.json['ID_partido_politico']
    Nombre_departamento = request.json['Nombre_departamento']

    candidato.ID_candidato = ID_candidato
    candidato.ID_candidato_elector = ID_candidato_elector
    candidato.DNI_candidato_elector = DNI_candidato_elector
    candidato.Nombre_candidato_elector = Nombre_candidato_elector
    candidato.Apellidos_candidato_elector = Apellidos_candidato_elector
    candidato.Foto_candidato = Foto_candidato
    candidato.Hoja_de_vida_candidato = Hoja_de_vida_candidato
    candidato.Propuesta_candidato = Propuesta_candidato
    candidato.ID_partido_politico = ID_partido_politico
    candidato.Nombre_departamento = Nombre_departamento

    db.session.commit()

    return candidato_schema.jsonify(candidato)

@app.route('/candidato/<ID_candidato>', methods=['DELETE'])
def delete_candidato(ID_candidato):
    candidato = Candidato.query.get(ID_candidato)
    db.session.delete(candidato)
    db.session.commit()

    return candidato_schema.jsonify(candidato)



# ------------------------------------------------------------------------------------------------------------------------------------

#tabla cédula

class Cedula(db.Model):
    __tablename__ = 'Cedula'
    ID_cedula = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    ID_elector_cedula = db.Column(db.String(15), db.ForeignKey('Elector.ID_elector'), nullable=False, unique=True)
    ID_partido_politico_cedula = db.Column(db.String(10), db.ForeignKey('Partido_politico.ID_siglas_partido_politico'), nullable=False)
    ID_candidato_cedula = db.Column(db.Integer, db.ForeignKey('Candidato.ID_candidato'), nullable=False)
    ID_ubigeo_cedula = db.Column(db.String(6), db.ForeignKey('Ubigeo.ID_ubigeo'), nullable=False)
    Fecha_cedula_voto = db.Column(db.DateTime, nullable=False)
 
    def __init__(self, ID_cedula,ID_elector_cedula, ID_partido_politico_cedula, ID_candidato_cedula, ID_ubigeo_cedula, Fecha_cedula_voto):
        self.ID_cedula = ID_cedula
        self.ID_elector_cedula = ID_elector_cedula
        self.ID_partido_politico_cedula = ID_partido_politico_cedula
        self.ID_candidato_cedula = ID_candidato_cedula
        self.ID_ubigeo_cedula = ID_ubigeo_cedula
        self.Fecha_cedula_voto = Fecha_cedula_voto

db.create_all()

class Cedula_schema(ma.Schema):
    class Meta:
        fields = ('ID_cedula', 'ID_elector_cedula', 'ID_partido_politico_cedula', 'ID_candidato_cedula', 'ID_ubigeo_cedula', 'Fecha_cedula_voto')
cedula_schema = Cedula_schema()
cedulas_schema = Cedula_schema(many=True)

@app.route('/cedula', methods=['POST'])
def add_cedula():
    ID_cedula = request.json['ID_cedula']
    ID_elector_cedula = request.json['ID_elector_cedula']
    ID_partido_politico_cedula = request.json['ID_partido_politico_cedula']
    ID_candidato_cedula = request.json['ID_candidato_cedula']
    ID_ubigeo_cedula = request.json['ID_ubigeo_cedula']
    Fecha_cedula_voto = request.json['Fecha_cedula_voto']

    nuevo_cedula = Cedula(ID_cedula, ID_elector_cedula, ID_partido_politico_cedula, ID_candidato_cedula, ID_ubigeo_cedula, Fecha_cedula_voto)

    db.session.add(nuevo_cedula)
    db.session.commit()
        
    return cedula_schema.jsonify(nuevo_cedula)

@app.route('/cedula', methods=['GET'])
def get_cedulas():
    cedulas = Cedula.query.all()
    return cedulas_schema.jsonify(cedulas)

@app.route('/cedula/<ID_cedula>', methods=['GET'])
def get_cedula(ID_cedula):
    cedula = Cedula.query.get(ID_cedula)
    return cedula_schema.jsonify(cedula)