import os
from celery import Celery

# Django設定モジュールのパスを環境変数に設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration.settings')

app = Celery('django-chat-app')

# Redisをブローカーとして使用
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
#app.conf.broker_url = redis_url
#app.conf.broker_url = 'redis://redis:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
