FROM python:3

COPY ./app /app
COPY ./requirements.txt .
COPY ./rrrocket_retriever.py .
COPY ./.env.compose.worker .env

# Setup python venv and put it at the front of PATH.
ENV VENV_PATH=/opt/venv
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN python rrrocket_retriever.py

CMD ["celery", "-A", "app.celery", "worker", "-l", "INFO"]