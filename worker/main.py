from celery import Celery

celery_app = Celery(
    "portatou",
    broker="amqp://user:pass@rabbitmq:5672//",
    backend="rpc://",
)
