from datetime import datetime

from flask import Blueprint, redirect, request, url_for

from controllers.usuario_controller import login_required, role_required
from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint("consulta", __name__, url_prefix="/consultas")


@consulta_bp.route("/")
@login_required
def index():
    fecha_buscada = request.args.get("fecha", "").strip()
    if fecha_buscada:
        fecha = datetime.strptime(fecha_buscada, "%Y-%m-%d").date()
        consultas = Consulta.get_by_fecha(fecha)
    else:
        consultas = Consulta.get_all()

    return consulta_view.list(consultas, fecha_buscada)


@consulta_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion", "medico")
def create():
    if request.method == "POST":
        fecha_str = request.form["fecha"].strip()
        diagnostico = request.form["diagnostico"].strip()
        tratamiento = request.form["tratamiento"].strip()
        id_medico = request.form["id_medico"].strip()
        id_paciente = request.form["id_paciente"].strip()

        if fecha_str and diagnostico and tratamiento and id_medico and id_paciente:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            consulta = Consulta(
                fecha=fecha,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                id_medico=int(id_medico),
                id_paciente=int(id_paciente),
            )
            consulta.save()
            return redirect(url_for("consulta.index"))

    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.create(medicos, pacientes)


@consulta_bp.route("/edit/<int:id_consulta>", methods=["GET", "POST"])
@login_required
@role_required("admin", "recepcion", "medico")
def edit(id_consulta):
    consulta = Consulta.get_by_id(id_consulta)
    if request.method == "POST":
        fecha_str = request.form["fecha"].strip()
        diagnostico = request.form["diagnostico"].strip()
        tratamiento = request.form["tratamiento"].strip()
        id_medico = request.form["id_medico"].strip()
        id_paciente = request.form["id_paciente"].strip()
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

        consulta.update(
            fecha=fecha,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            id_medico=int(id_medico),
            id_paciente=int(id_paciente),
        )
        return redirect(url_for("consulta.index"))

    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return consulta_view.edit(consulta, medicos, pacientes)


@consulta_bp.route("/delete/<int:id_consulta>")
@login_required
@role_required("admin")
def delete(id_consulta):
    consulta = Consulta.get_by_id(id_consulta)
    consulta.delete()
    return redirect(url_for("consulta.index"))
