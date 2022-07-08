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
@cross_origin()
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
@cross_origin()
def get_candidato():
    all_candidatos = Candidato.query.all()
    result = candidatos_schema.dump(all_candidatos)
    return jsonify(result)

@app.route('/candidato/<ID_candidato>', methods=['GET'])
@cross_origin()
def get_candidato_by_id(ID_candidato):
    candidato = Candidato.query.get(ID_candidato)
    return candidato_schema.jsonify(candidato)

@app.route('/candidato/<ID_candidato>', methods=['PUT'])
@cross_origin()
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
@cross_origin()
def delete_candidato(ID_candidato):
    candidato = Candidato.query.get(ID_candidato)
    db.session.delete(candidato)
    db.session.commit()

    return candidato_schema.jsonify(candidato)
