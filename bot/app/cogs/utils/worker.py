from celery import Celery

from ..configs.worker import BROKER_URL, BACKEND_URL

celery_app: Celery = Celery('worker', broker=BROKER_URL, backend=BACKEND_URL)

