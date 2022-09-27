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

import datetime

from sqlalchemy.exc import IntegrityError
from app import db

class Punto(db.Model):
    __tablename__ = 'punto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    notas = db.Column(db.String, nullable=True)
    grupos = db.relationship("Grupo")
    parent_id = db.Column(db.Integer, db.ForeignKey('punto.id', ondelete='CASCADE'))
    children = db.relationship("Punto")

    def __init__(self, nombre, estado, notas, grupos):
        self.nombre = nombre
        self.estado = estado
        self.notas = notas
        self.grupos = grupos

    def __repr__(self):
        return f'Punto({self.nombre})'

    def __str__(self):
        return self.nombre

    @staticmethod
    def get_all():
        return Punto.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Punto.query.get(id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Grupo(db.Model):
    __tablename__ = 'grupo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    notas = db.Column(db.String, nullable=True)
    punto = db.Column(db.Integer, db.ForeignKey('punto.id', ondelete='CASCADE'))
    parent_id = db.Column(db.Integer, db.ForeignKey('grupo.id', ondelete='CASCADE'))
    children = db.relationship("Grupo")
    dispositivos = db.relationship('Dispositivo', foreign_keys='Dispositivo.grupo_id', backref='grupo', lazy='dynamic', cascade='all, delete-orphan')
    distancia = db.Column(db.Float(precision=6), nullable=True)

    def __init__(self, nombre, notas, distancia):
        self.nombre = nombre
        self.notas = notas
        self.distancia = distancia

    def __repr__(self):
        return f'Grupo({self.nombre})'

    def __str__(self):
        return self.nombre

    @staticmethod
    def get_all():
        return Grupo.query.order_by(Grupo.id.asc()).all()

    @staticmethod
    def get_by_id(id):
        return Grupo.query.get(id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Dispositivo(db.Model):
    __tablename__ = 'dispositivo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    notas = db.Column(db.String, nullable=True)
    posicion = db.Column(db.Integer)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id', ondelete='CASCADE'))

    def __init__(self, nombre, notas):
        self.nombre = nombre
        self.notas = notas

    def __repr__(self):
        return f'({self.nombre},{self.id})'

    def __str__(self):
        return self.nombre
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Dispositivo.query.order_by(Dispositivo.id.asc()).all()

    @staticmethod
    def get_by_id(id):
        return Dispositivo.query.get(id)

class Medicion(db.Model):
    __tablename__ = 'medicion'

    id = db.Column(db.Integer, primary_key=True)
    medicion = db.Column(db.String, nullable=False)
    notas = db.Column(db.String, nullable=True)
    disp_id = db.Column(db.Integer, db.ForeignKey('dispositivo.id', ondelete='CASCADE'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, medicion, notas, disp_id):
        self.medicion = medicion
        self.notas = notas
        self.disp_id = disp_id

    def __repr__(self):
        return f'Medicion({self.medicion},{self.id})'

    def __str__(self):
        return self.medicion

class Calculo(db.Model):
    __tablename__ = 'calculo'

    #rango: muy bajo, bajo, medio, alto, muy alto, saturado.

    id = db.Column(db.Integer, primary_key=True)
    rango = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id', ondelete='SET NULL'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, rango, grupo_id, nombre):
        self.rango = rango
        self.grupo_id = grupo_id
        self.nombre = nombre

    def __repr__(self):
        return f'Calculo({self.rango},{self.id})'

    def __str__(self):
        return self.rango

    @staticmethod
    def get_by_id(id):
        return Calculo.query.get(id)

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Calculo.query.order_by(Calculo.created.desc()). \
            paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_all():
        return Calculo.query.order_by(Calculo.id.asc()).all()
