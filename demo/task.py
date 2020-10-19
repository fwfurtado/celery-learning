import time

from datetime import datetime

from celery import Celery
from celery.schedules import crontab

rabbit_url = 'amqp://k8s.local.technology:5672'

app = Celery('tasks', backend=rabbit_url, broker=rabbit_url)


def backoff(attempts):
    return 2 ** attempts


@app.task(name='tasks.add', bind=True, max_retry=4, soft_time_limit=5)
def add(self, a, b):
    result = a + b

    try:
        if (a == 1 and b == 2):
            raise ValueError('This is very simple. Stupid!')
    except ValueError as e:
        print(e)
        raise self.retry(exc=e, countdown=backoff(self.request.retries))

    print(f'{a} + {b} = {result}')

    time.sleep(10)

    return result


@app.task(name='tasks.send_email')
def send_email():
    try:
        messages_sent = 'example@email.com'
        print(f'Email message successfully sent, [{messages_sent}]')
    finally:
        print('Release resources')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(3.0, send_email)
    sender.add_periodic_task(crontab(minute='*/2'), cron_job.s(f'Now is {datetime.today()}'))

@app.task(name='tasks.cron_job')
def cron_job(message):
    print(f'Job! {message}')
