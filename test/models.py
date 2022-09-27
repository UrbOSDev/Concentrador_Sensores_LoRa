#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  models.py
#  
#  Copyright 2022 Cesar Lopez Aguillon <cesar@thunder>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import urbos_db as db
import datetime

from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey


class Grupo(db.Base):
    __tablename__ = 'grupo'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    notas = Column(String, nullable=True)

    def __init__(self, nombre, notas):
        self.nombre = nombre
        self.notas = notas

    def __repr__(self):
        return f'Grupo({self.nombre})'

    def __str__(self):
        return self.nombre


class Dispositivo(db.Base):
    __tablename__ = 'dispositivo'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    notas = Column(String, nullable=True)
    grupo_id = Column(Integer, ForeignKey('grupo.id', ondelete='CASCADE'))

    def __init__(self, nombre, notas, grupo_id):
        self.nombre = nombre
        self.notas = notas
        self.grupo_id = grupo_id

    def __repr__(self):
        return f'({self.nombre},{self.id})'

    def __str__(self):
        return self.nombre


class Medicion(db.Base):
    __tablename__ = 'medicion'

    id = Column(Integer, primary_key=True)
    medicion = Column(String, nullable=False)
    notas = Column(String, nullable=True)
    disp_id = Column(Integer, ForeignKey('dispositivo.id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, medicion, notas, disp_id):
        self.medicion = medicion
        self.notas = notas
        self.disp_id = disp_id

    def __repr__(self):
        return f'Medicion({self.medicion},{self.id})'

    def __str__(self):
        return self.medicion


class Calculo(db.Base):
    __tablename__ = 'calculo'

    #rango: muy bajo, bajo, medio, alto, muy alto, saturado.

    id = Column(Integer, primary_key=True)
    rango = Column(String, nullable=False)
    grupo_id = Column(Integer, ForeignKey('grupo.id', ondelete='SET NULL'))
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, rango, grupo_id):
        self.rango = rango
        self.grupo_id = grupo_id
