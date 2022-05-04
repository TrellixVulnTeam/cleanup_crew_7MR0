import subprocess
import json
import gzip

from .celery import app


@app.task(name='process_replay')
def process_replay(file_path: str) -> dict:
    result = subprocess.check_output(['rrrocket', '-n', file_path])
    return gzip.compress(result)
