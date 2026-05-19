from flask import Blueprint, redirect, request, url_for

from controllers.usuario_controller import login_required, role_required
from models.paciente_model import Paciente
from views import paciente_view

paciente_bp = Blueprint("paciente", __name__, url_prefix="/pacientes")


@paciente_bp.route("/")
@login_required
def index():
    pacientes = Paciente.get_all()
    return paciente_view.list(pacientes)


@paciente_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion")
def create():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        edad = request.form["edad"].strip()
        direccion = request.form["direccion"].strip()
        telefono = request.form["telefono"].strip()

        if nombre and edad and direccion and telefono:
            paciente = Paciente(nombre, int(edad), direccion, telefono)
            paciente.save()
            return redirect(url_for("paciente.index"))

    return paciente_view.create()


@paciente_bp.route("/edit/<int:id_paciente>", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion")
def edit(id_paciente):
    paciente = Paciente.get_by_id(id_paciente)
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        edad = request.form["edad"].strip()
        direccion = request.form["direccion"].strip()
        telefono = request.form["telefono"].strip()

        paciente.update(
            nombre=nombre,
            edad=int(edad),
            direccion=direccion,
            telefono=telefono,
        )
        return redirect(url_for("paciente.index"))

    return paciente_view.edit(paciente)


@paciente_bp.route("/delete/<int:id_paciente>")
@login_required
@role_required("admin")
def delete(id_paciente):
    paciente = Paciente.get_by_id(id_paciente)
    paciente.delete()
    return redirect(url_for("paciente.index"))
