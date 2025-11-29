import pika
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

def callback(ch, method, properties, body):
    print(f"[Consumer] Mensagem recebida: {body.decode()}")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='restaurante_criado', durable=True)
channel.basic_consume(queue='restaurante_criado', on_message_callback=callback, auto_ack=True)

print("[Consumer] Aguardando mensagens...")
channel.start_consuming()
