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

def format_datetime(value, format='short'):
    """Filtro que transforma un datetime en str con formato.

    El filtro es para ser usado en plantillas JINJA2.
    Los formatos posibles son los siguientes:
    * short: dd/mm/aaaa
    * full: dd de mm de aaaa

    :param datetime value: Fecha a ser transformada.
    :param format: Formato con el que mostrar la fecha. Valores posibles: short y full.
    :return: Un string con formato de la fecha.
    """

    value_str = None
    if not value:
        value_str = ''
    if format == 'short':
        value_str = value.strftime('%d/%m/%Y')
    elif format == 'full':
        value_str = value.strftime('%d de %m de %Y')
    elif format == 'fecha_hora':
        value_str = value.strftime('%H:%M:%S UTC %d/%m/%Y')
    else:
        value_str = ''
    return value_str


