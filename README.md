Before running, ensure that amqp server and celery are running before starting app.

```
rabbitmq-server
source env/bin/activate && celery -A models.tasks worker --loglevel=info --detach
```