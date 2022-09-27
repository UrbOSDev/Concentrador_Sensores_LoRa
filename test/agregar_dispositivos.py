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
from models import Grupo, Dispositivo

def run():
    grupo = Grupo('Grupo1','')
    db.session.add(grupo)
    db.session.commit()
    aaaa = Dispositivo('AAAA','',1)
    db.session.add(aaaa)
    db.session.commit()
    aaab = Dispositivo('AAAB','',1)
    db.session.add(aaab)
    db.session.commit()
    aaac = Dispositivo('AAAC','',1)
    db.session.add(aaac)
    db.session.commit()


if __name__ == '__main__':
    run()



