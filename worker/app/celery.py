from celery import Celery
from .config import BACKEND_URL, BROKER_URL

app = Celery('tasks',
             broker=BROKER_URL,
             backend=BACKEND_URL,
             include=['app.tasks'])

if __name__ == '__main__':
    app.start()
