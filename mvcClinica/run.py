from flask import Flask, request, redirect, url_for, session
from controllers import medico_controller, paciente_controller, consulta_controller, usuario_controller
from database import db
from models.usuario_model import Usuario

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clinica-medica-secret-key"

db.init_app(app)

app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(consulta_controller.consulta_bp)
app.register_blueprint(usuario_controller.usuario_bp)


def initialize_database():
    db.create_all()
    inspector = db.inspect(db.engine)
    columns = [column["name"] for column in inspector.get_columns("usuarios")] if inspector.has_table("usuarios") else []
    if "rol" not in columns:
        db.session.execute(db.text("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) NOT NULL DEFAULT 'recepcion'"))
        db.session.commit()

    usuario_inicial = Usuario.get_by_username("gustavo")
    if not usuario_inicial:
        usuario_inicial = Usuario("Gustavo", "gustavo", "10935022", "admin")
        usuario_inicial.save()
    else:
        usuario_inicial.rol = "admin"
        db.session.commit()


@app.context_processor
def inject_active_path():
    def is_active(path):
        return "active" if request.path == path else ""

    return dict(
        is_active=is_active,
        usuario_nombre=session.get("usuario_nombre"),
        usuario_rol=session.get("usuario_rol"),
    )


@app.route("/")
def home():
    return redirect(url_for("usuario.login"))


if __name__ == "__main__":
    with app.app_context():
        initialize_database()
    app.run(debug=True)
