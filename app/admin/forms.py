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

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, PasswordField, SelectField, FloatField, SelectMultipleField, IntegerField)
from wtforms.validators import DataRequired, Length, Optional, Email
#from ..models import Grupo

class GrupoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired('Dato requerido'), Length(max=128)])
    notas = TextAreaField('Notas')
    parent_id = SelectField('Grupo', coerce=int, validators=[Optional()])
    distancia = FloatField('Distancia')
    dispositivos = SelectMultipleField(u'Dispositivos', coerce=int, validators=[Optional()])
    quitar_dispositivos = BooleanField('Quitar dispositivos')
    submit = SubmitField('Guardar')

class PuntoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired('Dato requerido'), Length(max=128)])
    notas = TextAreaField('Notas')
    submit = SubmitField('Guardar')

class DispositivoForm(FlaskForm):
    
    nombre = StringField('Nombre', validators=[DataRequired('Dato requerido'), Length(max=128)])
    notas = TextAreaField('Notas')
    posicion = IntegerField(u'Posición')
    submit = SubmitField('Guardar')

class UserAdminForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[Optional()])
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
    
class CrearUsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
