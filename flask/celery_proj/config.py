from __future__ import absolute_import
from datetime import timedelta

CELERY_RESULT_BACKEND = 'redis://:123456qw@@127.0.0.1:6379/6'
BROKER_URL = 'redis://:123456qw@@127.0.0.1:6379/5'
CELERY_TIMEZONE = 'Asia/Shanghai'


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'proj.tasks.pullMsg',
         'schedule': timedelta(minutes=1),
         'args': 60
    },
}