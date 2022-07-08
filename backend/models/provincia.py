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
@cross_origin()
def add_provincia():
    ID_provincia = request.json['ID_provincia']
    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    new_provincia = Provincia(ID_provincia, Nombre_provincia, Nombre_departamento)

    db.session.add(new_provincia)
    db.session.commit()
    return provinciaSchema.jsonify(new_provincia)

@app.route('/provincia', methods=['GET'])
@cross_origin()
def get_provincia():
    all_provincias = Provincia.query.all()
    result = provinciasSchema.dump(all_provincias)
    return jsonify(result)

@app.route('/provincia/<Nombre_provincia>', methods=['GET'])
@cross_origin()
def get_provincia_by_name(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<ID_provincia>', methods=['GET'])
@cross_origin()
def get_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<Nombre_provincia>', methods=['PUT'])
@cross_origin()
def update_provincia(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)

    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    provincia.Nombre_provincia = Nombre_provincia
    provincia.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return provinciaSchema.jsonify(provincia)

@app.route('/provincia/<ID_provincia>', methods=['PUT'])
@cross_origin()
def update_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()

    Nombre_provincia = request.json['Nombre_provincia']
    Nombre_departamento = request.json['Nombre_departamento']

    provincia.Nombre_provincia = Nombre_provincia
    provincia.Nombre_departamento = Nombre_departamento

    db.session.commit()
    return provinciaSchema.jsonify(provincia)


@app.route('/provincia/<Nombre_provincia>', methods=['DELETE'])
@cross_origin()
def delete_provincia(Nombre_provincia):
    provincia = Provincia.query.get(Nombre_provincia)
    db.session.delete(provincia)
    db.session.commit()

    return 'Provincia eliminada'

@app.route('/provincia/<ID_provincia>', methods=['DELETE'])
@cross_origin()
def delete_provincia_by_id(ID_provincia):
    provincia = Provincia.query.filter_by(ID_provincia=ID_provincia).first()
    db.session.delete(provincia)
    db.session.commit()

    return 'Provincia eliminada'