from flask import Blueprint, redirect, request, url_for

from models.medico_model import Medico
from controllers.usuario_controller import login_required, role_required
from views import medico_view

medico_bp = Blueprint("medico", __name__, url_prefix="/medicos")


@medico_bp.route("/")
@login_required
def index():
    medicos = Medico.get_all()
    return medico_view.list(medicos)


@medico_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion")
def create():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        especialidad = request.form["especialidad"].strip()
        telefono = request.form["telefono"].strip()
        correo = request.form["correo"].strip()

        if nombre and especialidad and telefono and correo:
            medico = Medico(nombre, especialidad, telefono, correo)
            medico.save()
            return redirect(url_for("medico.index"))

    return medico_view.create()


@medico_bp.route("/edit/<int:id_medico>", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion")
def edit(id_medico):
    medico = Medico.get_by_id(id_medico)
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        especialidad = request.form["especialidad"].strip()
        telefono = request.form["telefono"].strip()
        correo = request.form["correo"].strip()

        medico.update(
            nombre=nombre,
            especialidad=especialidad,
            telefono=telefono,
            correo=correo,
        )
        return redirect(url_for("medico.index"))

    return medico_view.edit(medico)


@medico_bp.route("/delete/<int:id_medico>")
@login_required
@role_required("admin")
def delete(id_medico):
    medico = Medico.get_by_id(id_medico)
    medico.delete()
    return redirect(url_for("medico.index"))
