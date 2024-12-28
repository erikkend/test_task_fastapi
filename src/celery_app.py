from celery import Celery
app = Celery('tasks', broker='redis://@localhost:6379/0', backend="redis://")

app.autodiscover_tasks(force=True)


@app.task(name="calculate_text_lenght")
def calculate_text_lenght(text):
    return len(text)


