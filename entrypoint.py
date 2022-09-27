# -*- coding: utf-8 -*-
##############################################################################
#
#    UrbOS ITS Traffic Sesnors Gateway Software
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

import threading
import time
import serial
import os
import logging

from flask import send_from_directory
from sqlalchemy import event
from app import create_app
from app.models import Medicion, Dispositivo
from app.auth.models import User
from app import db
from app.tareas import lectura_serial, calculo_md, revision_dbt
from config import prod
from werkzeug.security import generate_password_hash

settings_module = prod
app = create_app(settings_module)

@event.listens_for(User.__table__, 'after_create')
def crear_usuario_admin(*args, **kwargs):
    contrasena = generate_password_hash('1234')
    db.session.add(User(name='admin', email='abc@domain.com', password=contrasena))
    db.session.commit()

def lectura_serial_sensores():
    res = lectura_serial(app)
    return res

def calculo_medidas():
    res = calculo_md(app)
    return res

def revision_database():
    res = revision_dbt(app)
    return res


lectura = threading.Thread(target=lectura_serial_sensores)
lectura.daemon = True
lectura.start()

calculo = threading.Thread(target=calculo_medidas)
calculo.daemon = True
calculo.start()

revision_db = threading.Thread(target=revision_database)
revision_db.daemon = True
revision_db.start()
