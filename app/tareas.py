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

import time
import serial
import os

from .logging_settings import loggerUTSG
from . import db
from .models import Medicion, Dispositivo

def lectura_serial(app):
    with app.app_context():
        serialPort = serial.Serial(port = '/dev/ttyS0', baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        dispositivos = {}
        mediciones = {}
        disp = db.session.query(Dispositivo).all()
        for d in disp:
            dispositivos[d.nombre] = d.id
            mediciones[d.nombre] = '0'
        while True:
            #loggerUTSG.warning('lectura_serial')
            if(serialPort.in_waiting > 0):
                #loggerUTSG.warning('lectura_serial ya no espera')
                serialString = serialPort.readline()
                try:
                    cadena = serialString.decode('ascii')
                    cadena = cadena.replace(' ','')
                    cadena = bytes.fromhex(cadena)
                    cadena = cadena.decode('ascii')
                    dispositivo = cadena[0:4]
                    #loggerUTSG.warning(cadena)
                    #loggerUTSG.warning(dispositivo)
                    if dispositivo in dispositivos:
                        medida = cadena[-1]
                        #loggerUTSG.warning(medida)
                        disp_id = dispositivos[dispositivo]
                        if medida != mediciones[dispositivo]:
                            med = Medicion(medida,'',disp_id)
                            db.session.add(med)
                            db.session.commit()
                            mediciones[dispositivo] = medida
                except:
                    print(serialString)
                    loggerUTSG.warning(serialString)
    return True

def calculo_md(app):
    with app.app_context():
        ciclos_calculo = app.config.get('CICLOS_CALCULOS', False)
        if ciclos_calculo:
            suma_ciclos = 0
            while True:
                if suma_ciclos >= ciclos_calculo:
                    suma_ciclos = 0
                    loggerUTSG.warning('Calculo')
                else:
                    time.sleep(1)
                    suma_ciclos += 1 
    return True

def revision_dbt(app):
    # metodo para revisar la db
    with app.app_context():
        ciclos = app.config.get('CICLOS_REVISION_DB', False)
        if ciclos:
            suma_ciclos = 0
            while True:
                if suma_ciclos >= ciclos:
                    suma_ciclos = 0
                    loggerUTSG.warning('Revision DB')
                else:
                    time.sleep(1)
                    suma_ciclos += 1
    return True
