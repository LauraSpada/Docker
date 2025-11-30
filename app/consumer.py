import pika
import os
import time
import json
import uuid
from datetime import datetime

# ===============================
# CONFIG
# ===============================
RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

QUEUE_NAME = "eventos"

# ===============================
# RETRY PARA CONEXÃO
# ===============================
def connect_with_retry(retries=10, delay=3):
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

    for attempt in range(1, retries + 1):
        try:
            print(f"[Consumer] Tentando conectar ao RabbitMQ ({attempt}/{retries})...")
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    port=RABBIT_PORT,
                    credentials=credentials,
                )
            )
        except Exception as e:
            print(f"[Consumer] Falha na conexão: {e}")
            time.sleep(delay)

    raise Exception("Não foi possível conectar ao RabbitMQ após várias tentativas.")


# ===============================
# CALLBACK
# ===============================
def callback(ch, method, properties, body):
    try:
        event = json.loads(body.decode())
        print(f"\n[Consumer] Evento recebido:")
        print(json.dumps(event, indent=4))
    except:
        print(f"[Consumer] Mensagem recebida (raw): {body.decode()}")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    connection = connect_with_retry()
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print("[Consumer] Aguardando mensagens...")
    channel.start_consuming()
