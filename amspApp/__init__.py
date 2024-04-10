from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .mycelery import app as celery_app

__all__ = ('celery_app',)

"""
https://stackoverflow.com/questions/25865270/how-to-install-python-mysqldb-module-using-pip
"""
import pymysql
pymysql.install_as_MySQLdb()
