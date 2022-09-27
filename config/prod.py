from .default import *

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'postgresql://flaskdb:1234@127.0.0.1:5432/flask'

ITEMS_PER_PAGE = 50

# cantidad de ciclos antes de revisar la DB / 1 ciclo = 1 segundo aprox
CICLOS_REVISION_DB = 3600

# cantidad de ciclos antes de calcular trafico / 1 ciclo = 1 segundo aprox
CICLOS_CALCULOS = 20

LOG_FILE = '/var/log/urbos/urbos_its_tsg.log'
