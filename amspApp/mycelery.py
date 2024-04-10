from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from amsp.settings import SESSION_REDIS_PASSWORD, SESSION_REDIS_HOST

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amsp.settings')

# app = Celery('tasks', broker='redis://:'+SESSION_REDIS_PASSWORD+'@'+SESSION_REDIS_HOST+'//')

app = Celery('tasks',
             broker='redis://'+SESSION_REDIS_PASSWORD+'@'+SESSION_REDIS_HOST+'//',
             # backend='redis://:'+SESSION_REDIS_PASSWORD+'@'+SESSION_REDIS_HOST+'//',
             include=['amspApp.tasks']
             )


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.


# app.control.discard_all()

app.autodiscover_tasks()
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
    # print("celery started")



@app.task(bind=True)
def debug_task(self):
    pass
    # print('Request: {0!r}'.format(self.request))