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

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import current_user

from app.models import Grupo, Calculo
from app.logging_settings import loggerUTSG
from . import public_bp

@public_bp.route("/")
def index():
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    calculos = Calculo.all_paginated(page, per_page)
    return render_template("public/index.html", calculos=calculos)

@public_bp.route("/c/<string:cid>/", methods=['GET', 'POST'])
def show_calculo(cid):
    loggerUTSG.info('Mostrando un Calculo')
    if not isinstance(cid, int):
        cid = int(cid)
    calculo = Calculo.get_by_id(cid)
    if not calculo:
        loggerUTSG.info(f'El calculo {cid} no existe')
        abort(404)
    grupo = Grupo.get_by_id(calculo.grupo_id)
    return render_template("public/calculo_view.html", calculo=calculo, grupo=grupo)
