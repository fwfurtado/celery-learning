import time

from celery.result import AsyncResult

from task import add

result = add.delay(1, 2)

while True:
    promise = AsyncResult(result.task_id)
    status = promise.status

    print(status)

    if 'SUCCESS' in status:
        print(f'result after 5 seconds wait {result.get()}')
        break
    if 'FAILURE' in status:
        print('Wrong happens', promise)
        break

    time.sleep(5)
