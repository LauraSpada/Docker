import pika
import os
import time
import json

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

QUEUE_NAME = "eventos"

def connect_with_retry():
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)

    while True:
        try:
            print("[Consumer] Tentando conectar ao RabbitMQ...", flush=True)
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    port=RABBIT_PORT,
                    credentials=credentials,
                    heartbeat=30,
                    blocked_connection_timeout=300
                )
            )
            print("[Consumer] Conectado ao RabbitMQ!", flush=True)
            return conn

        except Exception as e:
            print(f"[Consumer] Falha na conexão: {e}", flush=True)
            time.sleep(3)

def callback(ch, method, properties, body):
    try:
        event = json.loads(body.decode())
        print("\n[Consumer] Evento recebido:", flush=True)
        print(json.dumps(event, indent=4), flush=True)
    except Exception as e:
        print(f"[Consumer] Erro ao processar mensagem: {e}", flush=True)

if __name__ == "__main__":
    print("[Consumer] Iniciando consumer...", flush=True)

    while True:
        try:
            connection = connect_with_retry()
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE_NAME, durable=True)

            print("[Consumer] Aguardando mensagens...", flush=True)

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback,
                auto_ack=True
            )

            channel.start_consuming()

        except Exception as e:
            print(f"[Consumer] Erro inesperado: {e}", flush=True)
            print("[Consumer] Reiniciando consumer em 3 segundos...", flush=True)
            time.sleep(3)
