from celery import Celery
from redis import Redis

from celery.signals import task_success

app = Celery('tasks', broker='redis://@redis:6379/0', backend="redis://@redis:6379/0")
app.autodiscover_tasks(force=True)

redis_client = Redis(host='redis', port=6379, db=0)


@task_success.connect
def track_completed_tasks(sender=None, result=None, **kwargs):
    user_id = result.get("user_id")
    task_name = sender.name

    if user_id and task_name:
        redis_client.hincrby(user_id, "task", 1)


@app.task(name="calculate_text_lenght")
def calculate_text_lenght(text, user_id):
    return {'len': len(text), 'user_id': user_id}


def get_tasks_count(user_id: int | str) -> dict:
    # Получаем количество задач из Redis
    completed_tasks = redis_client.hget(user_id, "task")
    if completed_tasks is None:
        completed_tasks = 0  # Если данных нет, возвращаем 0

    return {"user_id": user_id, "completed_tasks": int(completed_tasks)}