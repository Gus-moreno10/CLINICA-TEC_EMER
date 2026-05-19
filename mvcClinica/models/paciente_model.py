from database import db


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    consultas = db.relationship("Consulta", back_populates="paciente")

    def __init__(self, nombre, edad, direccion, telefono):
        self.nombre = nombre
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Paciente.query.all()

    @staticmethod
    def get_by_id(id_paciente):
        return Paciente.query.get(id_paciente)

    def update(self, nombre=None, edad=None, direccion=None, telefono=None):
        if nombre:
            self.nombre = nombre
        if edad is not None and edad != "":
            self.edad = edad
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
