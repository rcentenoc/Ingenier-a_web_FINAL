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
@cross_origin()
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
@cross_origin()
def get_ubigeo():
    all_ubigeos = Ubigeo.query.all()
    result = ubigeosSchema.dump(all_ubigeos)
    return jsonify(result)

@app.route('/ubigeo/<ID_ubigeo>', methods=['GET'])
@cross_origin()
def get_ubigeo_by_id(ID_ubigeo):
    ubigeo = Ubigeo.query.get(ID_ubigeo)
    return ubigeoSchema.jsonify(ubigeo)

@app.route('/ubigeo/<ID_ubigeo>', methods=['PUT'])
@cross_origin()
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
@cross_origin()
def delete_ubigeo(ID_ubigeo):
    ubigeo = Ubigeo.query.get(ID_ubigeo)
    db.session.delete(ubigeo)
    db.session.commit()

    return 'Ubigeo eliminado'