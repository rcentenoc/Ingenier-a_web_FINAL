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
@cross_origin()
def add_departamento():
    ID_departamento = request.json['ID_departamento']
    Nombre_departamento = request.json['Nombre_departamento']

    new_departamento = Departamento(ID_departamento, Nombre_departamento)

    db.session.add(new_departamento)
    db.session.commit()
    return Departamento_schema.jsonify(new_departamento)

@app.route('/departamento', methods=['GET'])
@cross_origin()
def get_departamento():
    all_departamentos = Departamento.query.all()
    result = Departamentos_schema.dump(all_departamentos)
    return jsonify(result)

@app.route('/departamento/<Nombre_departamento>', methods=['GET'])
@cross_origin()
def get_departamento_by_name(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)
    return Departamento_schema.jsonify(departamento)

@app.route('/departamento/<Nombre_departamento>', methods=['PUT'])
@cross_origin()
def update_departamento(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)

    Nombre_departamento = request.json['Nombre_departamento']

    departamento.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return Departamento_schema.jsonify(departamento)

@app.route('/departamento/<Nombre_departamento>', methods=['DELETE'])
@cross_origin()
def delete_departamento(Nombre_departamento):
    departamento = Departamento.query.get(Nombre_departamento)
    db.session.delete(departamento)
    db.session.commit()

    return 'Departamento eliminado'