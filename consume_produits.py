# consume_products.py (à placer dans l’API Orders)

import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Message reçu : {method.routing_key} → {message}")
    print(f"[ PRODUIT] Message complet reçu : {json.dumps(message, indent=2)}")

def main():
    print("En attente des événements RabbitMQ (products.created, products.updated, products.deleted)...")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='topic')
    queue_name = 'orders_listen_products'
    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange='events', queue=queue_name, routing_key='products.created')
    channel.queue_bind(exchange='events', queue=queue_name, routing_key='products.updated')
    channel.queue_bind(exchange='events', queue=queue_name, routing_key='products.deleted')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
