from celery import Celery
from redis import Redis

from celery.signals import task_success

app = Celery('tasks', broker='redis://@localhost:6379/0', backend="redis://")
app.autodiscover_tasks(force=True)

redis_client = Redis(host='localhost', port=6379, db=0)


@task_success.connect
def track_completed_tasks(sender=None, result=None, **kwargs):
    user_id = result.get("user_id")
    task_name = sender.name

    if user_id and task_name:
        redis_client.hincrby(user_id, "task", 1)


@app.task(name="calculate_text_lenght")
def calculate_text_lenght(text, user_id):
    return {'len': len(text), 'user_id': user_id}
