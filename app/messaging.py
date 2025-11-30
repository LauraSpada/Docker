import pika
import os
import json
import uuid
from datetime import datetime

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")

def publish_event(event_type, payload):
    event = {
        "eventId": str(uuid.uuid4()),
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload
    }

    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue="eventos", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="eventos",
        body=json.dumps(event)
    )

    connection.close()
