# -*- coding: utf-8 -*-
##############################################################################
#
#    UrbOS ITS Traffic Sensors Gateway Software
#    Copyright (C) 2020-2022 UrbOS (<https://urbos.io>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import os

from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Grupo, Punto, Dispositivo
from . import admin_bp
from .forms import UserAdminForm, GrupoForm, PuntoForm, DispositivoForm, CrearUsuarioForm

from app.logging_settings import loggerUTSG

logger = logging.getLogger(__name__)


@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")

@admin_bp.route("/admin/usuarios/")
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/usuarios.html", users=users)

@admin_bp.route("/admin/crear_usuario/", methods=["GET", "POST"])
@login_required
@admin_required
def crear_usuario():
    form = CrearUsuarioForm()
    error = None
    if form.validate_on_submit():
        name = form.nombre.data
        email = form.email.data
        password = form.password.data
        is_admin = form.is_admin.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email, is_admin=is_admin)
            user.set_password(password)
            user.save()
            return redirect(url_for('admin.list_users'))
    return render_template("admin/usuario_crear_form.html", form=form, error=error)

@admin_bp.route("/admin/usuario/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        loggerUTSG.info(f'El usuario {user_id} no existe')
        abort(404)

    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        user.save()
        loggerUTSG.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/usuario_form.html", form=form, user=user)


@admin_bp.route("/admin/usuario/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    loggerUTSG.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        loggerUTSG.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    loggerUTSG.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))


@admin_bp.route("/admin/grupos/")
@login_required
@admin_required
def list_grupos():
    grupos = Grupo.get_all()
    return render_template("admin/grupos.html", grupos=grupos)

@admin_bp.route("/admin/crear_grupo/", methods=['GET', 'POST'])
@login_required
@admin_required
def crear_grupo():
    form = GrupoForm()
    form.parent_id.choices = [(g.id, g.nombre) for g in Grupo.get_all()]
    form.parent_id.choices.insert(0, (0,'Sin Grupo'))
    form.dispositivos.choices = [(d.id, d.nombre) for d in Dispositivo.get_all()]
    if form.validate_on_submit():
        nombre = form.nombre.data
        notas = form.notas.data
        parent_id = form.parent_id.data
        dispositivos = form.dispositivos.data
        loggerUTSG.warning(dispositivos)
        distancia = form.distancia.data or 0.0
        grupo = Grupo(nombre=nombre, notas=notas, distancia=distancia)
        grupo.save()
        if parent_id:
            grupo.parent_id = parent_id
            grupo.save()
        if dispositivos:
            for d in dispositivos:
                dispositivo = Dispositivo.get_by_id(d)
                dispositivo.grupo_id = grupo.id
                dispositivo.save()
        return redirect(url_for('admin.list_grupos'))
    return render_template("admin/grupo_crear_form.html", form=form)

@admin_bp.route("/admin/grupo/<int:grupo_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_grupo_form(grupo_id):
    grupo = Grupo.get_by_id(grupo_id)
    if grupo is None:
        logger.info(f'El grupo {grupo_id} no existe')
        abort(404)
    form = GrupoForm(obj=grupo)
    form.parent_id.choices = [(g.id, g.nombre) for g in Grupo.get_all() if g.id != grupo.id]
    form.parent_id.choices.insert(0, (0,'Sin Grupo'))
    form.dispositivos.choices = [(d.id, d.nombre) for d in Dispositivo.get_all()]
    grupo_padre = 'Sin grupo padre'
    if grupo.parent_id:
        gp = Grupo.get_by_id(grupo.parent_id)
        grupo_padre = gp.nombre
    if form.validate_on_submit():
        grupo.nombre = form.nombre.data
        grupo.notas = form.notas.data
        if form.distancia.data:
            grupo.distancia = form.distancia.data
        if form.parent_id.data:
            grupo.parent_id = form.parent_id.data
        else:
            grupo.parent_id = None
        grupo.save()
        dispositivos = form.dispositivos.data
        if dispositivos:
            if grupo.dispositivos:
                for disp in grupo.dispositivos:
                    disp.grupo_id = None
                    disp.save()
            for d in dispositivos:
                dispositivo = Dispositivo.get_by_id(d)
                dispositivo.grupo_id = grupo.id
                dispositivo.save()
        if form.quitar_dispositivos.data:
            loggerUTSG.warning(form.quitar_dispositivos.data)
            for disp in grupo.dispositivos:
                disp.grupo_id = None
                disp.save()
        return redirect(url_for('admin.list_grupos'))
    return render_template("admin/grupo_form.html", form=form, grupo=grupo, grupo_padre=grupo_padre)

@admin_bp.route("/admin/grupo/delete/<int:grupo_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_grupo(grupo_id):
    grupo = Grupo.get_by_id(grupo_id)
    if grupo is None:
        logger.info(f'El grupo {punto_id} no existe')
        abort(404)
    grupo.delete()
    return redirect(url_for('admin.list_grupos'))

@admin_bp.route("/admin/puntos/")
@login_required
@admin_required
def list_puntos():
    puntos = Punto.get_all()
    return render_template("admin/puntos.html", puntos=puntos)

@admin_bp.route("/admin/crear_punto/", methods=['GET', 'POST'])
@login_required
@admin_required
def crear_punto():
    form = PuntoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        notas = form.notas.data
        punto = Punto(nombre=nombre, estado='bajo', notas=notas, grupos=[])
        punto.save()
        return redirect(url_for('admin.list_puntos'))
    return render_template("admin/punto_crear_form.html", form=form)

@admin_bp.route("/admin/punto/<int:punto_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_punto_form(punto_id):
    punto = Punto.get_by_id(punto_id)
    if punto is None:
        logger.info(f'El punto {punto_id} no existe')
        abort(404)
    form = PuntoForm(obj=punto)
    if form.validate_on_submit():
        punto.nombre = form.nombre.data
        punto.notas = form.notas.data
        punto.save()
        return redirect(url_for('admin.list_puntos'))
    return render_template("admin/punto_form.html", form=form, punto=punto)

@admin_bp.route("/admin/punto/delete/<int:punto_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_punto(punto_id):
    punto = Punto.get_by_id(punto_id)
    if punto is None:
        logger.info(f'El punto {punto_id} no existe')
        abort(404)
    punto.delete()
    return redirect(url_for('admin.list_puntos'))




@admin_bp.route("/admin/dispositivos/")
@login_required
@admin_required
def list_dispositivos():
    dispositivos = Dispositivo.get_all()
    nombre_grupos = dict()
    for d in dispositivos:
        if d.grupo_id:
            g = Grupo.get_by_id(d.grupo_id)
            nombre_grupos[d.id] = g.nombre
        else:
            nombre_grupos[d.id] = 'Sin grupo'
    return render_template("admin/dispositivos.html", dispositivos=dispositivos, nombre_grupos=nombre_grupos)

@admin_bp.route("/admin/crear_dispositivo/", methods=['GET', 'POST'])
@login_required
@admin_required
def crear_dispositivo():
    form = DispositivoForm()
    #form.grupo_id.choices = [(g.id, g.nombre) for g in Grupo.query.order_by('nombre')]
    if form.validate_on_submit():
        nombre = form.nombre.data
        notas = form.notas.data
        #grupo_id = form.grupo_id.data
        #dispositivo = Dispositivo(nombre=nombre, notas=notas, grupo_id=grupo_id)
        dispositivo = Dispositivo(nombre=nombre, notas=notas)
        dispositivo.save()
        return redirect(url_for('admin.list_dispositivos'))
    return render_template("admin/dispositivo_crear_form.html", form=form)

@admin_bp.route("/admin/dispositivo/<int:dispositivo_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_dispositivo_form(dispositivo_id):
    dispositivo = Dispositivo.get_by_id(dispositivo_id)
    if dispositivo is None:
        logger.info(f'El dispositivo {dispositivo_id} no existe')
        abort(404)
    form = DispositivoForm(obj=dispositivo)
    nombre_grupo = 'Sin grupo'
    if dispositivo.grupo_id:
        gp = Grupo.get_by_id(dispositivo.grupo_id)
        nombre_grupo = gp.nombre
    if form.validate_on_submit():
        dispositivo.nombre = form.nombre.data
        dispositivo.notas = form.notas.data
        if form.posicion.data:
            dispositivo.posicion = form.posicion.data
        dispositivo.save()
        return redirect(url_for('admin.list_dispositivos'))
    return render_template("admin/dispositivo_form.html", form=form, dispositivo=dispositivo, nombre_grupo=nombre_grupo)

@admin_bp.route("/admin/dispositivo/delete/<int:dispositivo_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_dispositivo(dispositivo_id):
    dispositivo = Dispositivo.get_by_id(dispositivo_id)
    if dispositivo is None:
        logger.info(f'El dispositivo {dispositivo_id} no existe')
        abort(404)
    dispositivo.delete()
    return redirect(url_for('admin.list_dispositivos'))
