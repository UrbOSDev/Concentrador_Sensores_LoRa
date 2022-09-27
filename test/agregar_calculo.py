#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  agregar_dispositivos.py
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
from models import Calculo

#rango: muy bajo, bajo, medio, alto, muy alto, saturado.

def run():
    calculo1 = Calculo('muy bajo',1)
    db.session.add(calculo1)
    db.session.commit()
    calculo2 = Calculo('medio',1)
    db.session.add(calculo2)
    db.session.commit()
    calculo3 = Calculo('alto',1)
    db.session.add(calculo3)
    db.session.commit()


if __name__ == '__main__':
    run()



