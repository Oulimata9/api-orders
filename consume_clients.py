# consume_clients.py (dans l'API Orders)

import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Message reçu : {method.routing_key} → {message}")
    # Ici, tu peux traiter le message (ex : log, base de données, ou autre action)

def main():
    print("En attente des événements RabbitMQ (clients.created, clients.updated)...")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='topic')
    queue_name = 'orders_listen_clients'
    channel.queue_declare(queue=queue_name, durable=True)

    # Lie la queue aux événements client
    channel.queue_bind(exchange='events', queue=queue_name, routing_key='clients.created')
    channel.queue_bind(exchange='events', queue=queue_name, routing_key='clients.updated')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
