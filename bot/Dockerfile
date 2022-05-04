FROM python:3
RUN apt-get update && apt-get install -y libffi-dev python3-dev

# For organization and to keep import clean and IDE happy.
COPY ./app /app
COPY ./.env.compose.bot .env
COPY ./requirements.txt .

# Setup python venv and put it at the front of PATH.
ENV VENV_PATH=/opt/venv
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install -U pip
RUN pip install -r requirements.txt

WORKDIR /app

CMD ["python", "main.py"]
