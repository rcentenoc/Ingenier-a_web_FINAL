class Elecciones(db.Model):
    __tablename__ = 'Elecciones'
    ID_eleccion = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    Nombre_eleccion = db.Column(db.String(50), nullable=False)
    Fecha_eleccion = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID_eleccion, Nombre_eleccion, Fecha_eleccion):
        self.ID_eleccion = ID_eleccion
        self.Nombre_eleccion = Nombre_eleccion
        self.Fecha_eleccion = Fecha_eleccion

db.create_all()

class Elecciones_schema(ma.Schema):
    class Meta:
        fields = ('ID_eleccion', 'Nombre_eleccion', 'Fecha_eleccion')
eleccion_schema = Elecciones_schema()
elecciones_schema = Elecciones_schema(many=True)

@app.route('/eleccion', methods=['POST'])
@cross_origin()
def add_eleccion():
    ID_eleccion = request.json['ID_eleccion']
    Nombre_eleccion = request.json['Nombre_eleccion']
    Fecha_eleccion = request.json['Fecha_eleccion']
    
    nueva_eleccion = Elecciones(ID_eleccion, Nombre_eleccion, Fecha_eleccion)

    db.session.add(nueva_eleccion)
    db.session.commit()
        
    return eleccion_schema.jsonify(nueva_eleccion)

@app.route('/eleccion', methods=['GET'])
@cross_origin()
def get_elecciones():
    elecciones = Elecciones.query.all()
    return elecciones_schema.jsonify(elecciones)
