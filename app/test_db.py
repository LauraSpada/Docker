import os
from dotenv import load_dotenv
from mongoengine import connect, get_connection

load_dotenv()

connect(
    db=os.getenv("MONGO_DB"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    authentication_source=os.getenv("MONGO_AUTH_SOURCE")
)

try:
    conn = get_connection()
    print("Conexão realizada com sucesso!")
    print(conn.server_info())
except Exception as e:
    print("Falha na conexão!")
    print(e)
