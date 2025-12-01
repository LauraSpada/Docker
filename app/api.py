import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from mongoengine import (
    Document, EmbeddedDocument,
    StringField, FloatField,
    ListField, EmbeddedDocumentField,
    connect
)
from events import publish_event  
load_dotenv()

connect(
    db=os.getenv("MONGO_DB"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    authentication_source=os.getenv("MONGO_AUTH_SOURCE")
)

app = Flask(__name__)
CORS(app)

class Opcao(EmbeddedDocument):
    nome = StringField(required=True, max_length=100)
    ingredientes = StringField(max_length=250)
    preco = FloatField(required=True)

class Restaurante(Document):
    nome = StringField(required=True, max_length=100)
    descricao = StringField(required=True)
    telefone = StringField(max_length=20)
    localizacao = StringField(max_length=100)
    opcoes = ListField(EmbeddedDocumentField(Opcao))

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/restaurantes")
def criar_restaurante():
    data = request.json
    restaurante = Restaurante(**data).save()

    publish_event(
        event_type="restaurante.criado",
        payload={
            "id": str(restaurante.id),
            "nome": restaurante.nome,
            "endereco": restaurante.localizacao
        }
    )

    return jsonify({"message": "Restaurante criado!", "id": str(restaurante.id)}), 201

@app.get("/restaurantes")
def listar_restaurantes():
    restaurantes = [
        {
            "id": str(r.id),
            "nome": r.nome,
            "descricao": r.descricao,
            "telefone": r.telefone,
            "localizacao": r.localizacao,
            "opcoes": [
                {"nome": o.nome, "ingredientes": o.ingredientes, "preco": o.preco}
                for o in r.opcoes
            ]
        }
        for r in Restaurante.objects
    ]
    return jsonify(restaurantes), 200

@app.get("/restaurantes/<id>")
def listar_restaurante_id(id):
    restaurante = Restaurante.objects(id=id).first()
    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    return jsonify({
        "id": str(restaurante.id),
        "nome": restaurante.nome,
        "descricao": restaurante.descricao,
        "telefone": restaurante.telefone,
        "localizacao": restaurante.localizacao,
        "opcoes": [
            {"nome": o.nome, "ingredientes": o.ingredientes, "preco": o.preco}
            for o in restaurante.opcoes
        ]
    }), 200

@app.put("/restaurantes/<id>")
def atualizar_restaurante(id):
    data = request.json
    restaurante = Restaurante.objects(id=id).first()

    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    restaurante.update(**data)
    restaurante.reload()

    publish_event(
        event_type="restaurante.atualizado",
        payload={
            "id": str(restaurante.id),
            "nome": restaurante.nome,
            "telefone": restaurante.telefone
        }
    )

    return jsonify({"message": "Restaurante atualizado!"}), 200

@app.delete("/restaurantes/<id>")
def deletar_restaurante(id):
    restaurante = Restaurante.objects(id=id).first()

    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    restaurante.delete()

    publish_event(
        event_type="restaurante.deletado",
        payload={"id": id}
    )

    return jsonify({"message": "Restaurante removido!"}), 200


@app.post("/restaurantes/<id>/opcoes")
def adicionar_opcao(id):
    restaurante = Restaurante.objects(id=id).first()
    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    data = request.json
    opcao = Opcao(**data)

    restaurante.opcoes.append(opcao)
    restaurante.save()

    publish_event(
        event_type="opcao.criado",
        payload={
            "restaurante": id,
            "nome": opcao.nome,
            "preco": opcao.preco
        }
    )

    return jsonify({"message": "Opção adicionada!"}), 201

@app.get("/restaurantes/<id>/opcoes")
def listar_opcoes_restaurante(id):

    try:
        restaurante = Restaurante.objects(id=id).first()
    except Exception:
        return jsonify({"erro": "ID inválido"}), 400

    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    opcoes = [
        {"nome": o.nome, "ingredientes": o.ingredientes, "preco": o.preco}
        for o in restaurante.opcoes
    ]

    return jsonify(opcoes), 200

@app.put("/restaurantes/<id>/opcoes/<nome_opcao>")
def atualizar_opcao(id, nome_opcao):
    restaurante = Restaurante.objects(id=id).first()
    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    opcao = next((o for o in restaurante.opcoes if o.nome == nome_opcao), None)
    if not opcao:
        return jsonify({"erro": "Opção não encontrada!"}), 404

    data = request.json
    opcao.ingredientes = data.get("ingredientes", opcao.ingredientes)
    opcao.preco = data.get("preco", opcao.preco)

    restaurante.save()

    publish_event(
        event_type="opcao.atualizado",
        payload={
            "restaurante": id,
            "nome": opcao.nome,
            "preco": opcao.preco
        }
    )

    return jsonify({"message": "Opção atualizada!"}), 200

@app.delete("/restaurantes/<id>/opcoes/<nome_opcao>")
def deletar_opcao(id, nome_opcao):
    restaurante = Restaurante.objects(id=id).first()
    if not restaurante:
        return jsonify({"erro": "Restaurante não encontrado!"}), 404

    nova_lista = [o for o in restaurante.opcoes if o.nome != nome_opcao]

    if len(nova_lista) == len(restaurante.opcoes):
        return jsonify({"erro": "Opção não encontrada!"}), 404

    restaurante.opcoes = nova_lista
    restaurante.save()

    publish_event(
        event_type="opcao.deletado",
        payload={"restaurante": id, "nome": nome_opcao}
    )

    return jsonify({"message": "Opção removida!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
