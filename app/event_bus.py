# event_bus.py

import pika
import json

RABBITMQ_HOST = 'localhost'
EXCHANGE = 'events'

#  Envoi d’un message vers RabbitMQ
def publish_event(routing_key, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(data)
    )
    connection.close()
    print(f" Message envoyé : {routing_key} → {data}")

#  Réception d’un message depuis RabbitMQ
def consume_event(routing_key, callback_function):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=routing_key)

    def on_message(ch, method, properties, body):
        data = json.loads(body)
        print(f" Message reçu : {method.routing_key} → {data}")
        callback_function(data)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    print(f"En attente de messages : {routing_key}")
    channel.start_consuming()
