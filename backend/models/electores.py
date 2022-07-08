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
    vector_elector = db.Column(db.String(70), nullable=False)

    def __init__(self, ID_elector, DNI_elector, Nombre_elector, Apellidos_elector, Estado_elector, Tipo_elector, Email_elector, Telefono_elector, Nacimiento_elector, Genero_elector, Password_elector, Direccion_elector, Departamento_elector, ID_ubigeo_elector, vector_elector):
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
        self.vector_elector = vector_elector

db.create_all()

class ElectorSchema(ma.Schema):
    class Meta:
        fields = ('ID_elector', 'DNI_elector', 'Nombre_elector', 'Apellidos_elector', 'Estado_elector', 'Tipo_elector', 'Email_elector', 'Telefono_elector', 'Nacimiento_elector', 'Genero_elector', 'Password_elector', 'Direccion_elector', 'Departamento_elector', 'ID_ubigeo_elector', 'vector_elector')

electorSchema = ElectorSchema()
electoresSchema = ElectorSchema(many=True)

@app.route('/elector/nuevo', methods=['POST'])
@cross_origin()
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
    vector_elector = request.json['vector_elector']

    nuevo_elector = Elector(ID_elector, DNI_elector, Nombre_elector, Apellidos_elector, Estado_elector, Tipo_elector, Email_elector, Telefono_elector, Nacimiento_elector, Genero_elector, Password_elector, Direccion_elector, Departamento_elector, ID_ubigeo_elector, vector_elector)
    db.session.add(nuevo_elector)
    db.session.commit()

    return electorSchema.jsonify(nuevo_elector)


@app.route('/elector', methods=['GET'])
@cross_origin()
def get_elector():
    all_elector = Elector.query.all()
    result = electoresSchema.dump(all_elector)
    return jsonify(result)

@app.route('/elector/<ID_elector>', methods=['GET'])
@cross_origin()
def get_elector_by_id(ID_elector):
    elector = Elector.query.get(ID_elector)
    return electorSchema.jsonify(elector)

@app.route('/elector/<DNI_elector>', methods=['GET'])
@cross_origin()
def get_elector_by_dni(DNI_elector):
    elector = Elector.query.filter_by(DNI_elector=DNI_elector).first()
    return electorSchema.jsonify(elector)

@app.route('/elector/editar/<ID_elector>', methods=['PUT'])
@cross_origin()
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
    vector_elector = request.json['vector_elector']


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
    elector.vector_elector = vector_elector


    db.session.commit()
    return electorSchema.jsonify(elector)

@app.route('/elector/<ID_elector>', methods=['DELETE'])
@cross_origin()
def delete_elector(ID_elector):
    elector = Elector.query.get(ID_elector)
    db.session.delete(elector)
    db.session.commit()
    return electorSchema.jsonify(elector)