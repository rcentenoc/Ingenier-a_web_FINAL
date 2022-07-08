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
@cross_origin()
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
@cross_origin()
def get_partido_politico():
    all_partido_politico = Partido_politico.query.all()
    result = partidos_politicos_schema.dump(all_partido_politico)
    return jsonify(result)

@app.route('/partido_politico/<ID_siglas_partido_politico>', methods=['GET'])
@cross_origin()
def get_partido_politico_by_id(ID_siglas_partido_politico):
    partido_politico = Partido_politico.query.get(ID_siglas_partido_politico)
    return partido_politico_schema.jsonify(partido_politico)

@app.route('/partido_politico/<ID_siglas_partido_politico>', methods=['PUT'])
@cross_origin()
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
@cross_origin()
def delete_partido_politico(ID_siglas_partido_politico):
    partido_politico = Partido_politico.query.get(ID_siglas_partido_politico)
    db.session.delete(partido_politico)
    db.session.commit()

    return partido_politico_schema.jsonify(partido_politico)