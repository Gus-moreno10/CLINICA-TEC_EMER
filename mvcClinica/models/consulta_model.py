from database import db


class Consulta(db.Model):
    __tablename__ = "consultas"

    id_consulta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    diagnostico = db.Column(db.String(200), nullable=False)
    tratamiento = db.Column(db.String(200), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey("medicos.id_medico"), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey("pacientes.id_paciente"), nullable=False)

    medico = db.relationship("Medico", back_populates="consultas")
    paciente = db.relationship("Paciente", back_populates="consultas")

    def __init__(self, fecha, diagnostico, tratamiento, id_medico, id_paciente):
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.id_medico = id_medico
        self.id_paciente = id_paciente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Consulta.query.order_by(Consulta.fecha.desc()).all()

    @staticmethod
    def get_by_id(id_consulta):
        return Consulta.query.get(id_consulta)

    @staticmethod
    def get_by_fecha(fecha):
        return Consulta.query.filter_by(fecha=fecha).order_by(Consulta.id_consulta.desc()).all()

    def update(self, fecha=None, diagnostico=None, tratamiento=None, id_medico=None, id_paciente=None):
        if fecha:
            self.fecha = fecha
        if diagnostico:
            self.diagnostico = diagnostico
        if tratamiento:
            self.tratamiento = tratamiento
        if id_medico:
            self.id_medico = id_medico
        if id_paciente:
            self.id_paciente = id_paciente

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
