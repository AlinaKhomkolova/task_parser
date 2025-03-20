from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0')

# Настройка периодической задачи
app.conf.beat_schedule = {
    'fetch-codeforces-every-hour': {
        'task': 'src.celery.tasks.fetch_codeforces_data',
        'schedule': crontab(minute="0", hour="*"),  # Каждые 1 час (в начале часа)
    },
}

app.conf.result_backend = 'redis://localhost:6379/0'
