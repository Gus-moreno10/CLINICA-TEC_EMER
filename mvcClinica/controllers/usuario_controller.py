from functools import wraps

from flask import Blueprint, redirect, request, session, url_for

from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("usuario.login"))
        return view(*args, **kwargs)

    return wrapped_view


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if "usuario_id" not in session:
                return redirect(url_for("usuario.login"))
            if session.get("usuario_rol") not in roles:
                return redirect(url_for("consulta.index"))
            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@usuario_bp.route("/")
@login_required
@role_required("admin")
def index():
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)


@usuario_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        rol = request.form["rol"].strip()

        if nombre and username and password and rol and not Usuario.get_by_username(username):
            usuario = Usuario(nombre, username, password, rol)
            usuario.save()
            return redirect(url_for("usuario.index"))

    return usuario_view.create()


@usuario_bp.route("/edit/<int:id_usuario>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit(id_usuario):
    usuario = Usuario.get_by_id(id_usuario)
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        rol = request.form["rol"].strip()

        usuario_existente = Usuario.get_by_username(username)
        if usuario_existente and usuario_existente.id_usuario != usuario.id_usuario:
            return usuario_view.edit(usuario)

        usuario.update(
            nombre=nombre,
            username=username,
            password=password if password else None,
            rol=rol,
        )
        return redirect(url_for("usuario.index"))

    return usuario_view.edit(usuario)


@usuario_bp.route("/delete/<int:id_usuario>")
@login_required
@role_required("admin")
def delete(id_usuario):
    usuario = Usuario.get_by_id(id_usuario)
    if usuario:
        usuario.delete()
    return redirect(url_for("usuario.index"))


@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        usuario = Usuario.get_by_username(username)
        if usuario and usuario.verify_password(password):
            session["usuario_id"] = usuario.id_usuario
            session["usuario_nombre"] = usuario.nombre
            session["usuario_rol"] = usuario.rol
            return redirect(url_for("consulta.index"))

        return usuario_view.login(error="Usuario o contrasena incorrectos")

    return usuario_view.login()


@usuario_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("usuario.login"))
