import os
import gevent.socket
import redis.connection

from amsp import settings

redis.connection.socket = gevent.socket

os.environ.update(DJANGO_SETTINGS_MODULE='amsp.settings')
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

application = uWSGIWebsocketServer()
