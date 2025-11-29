import os
from dotenv import load_dotenv
from messaging import publish_message
from mongoengine import (
    Document, EmbeddedDocument,
    StringField, DateTimeField, IntField, FloatField,
    ListField, EmbeddedDocumentField, ReferenceField, connect
)

from datetime import datetime

load_dotenv()

connect(
    db=os.getenv("MONGO_DB"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    authentication_source=os.getenv("MONGO_AUTH_SOURCE")
)

#---------------------

class Opcao(EmbeddedDocument):
    nome = StringField(required=True, max_length=100)
    ingredientes = StringField(max_length=250)
    preco = FloatField(required=True)

    def __str__(self):
        return f"{self.nome}/{self.ingredientes}/{self.preco}"

class Restaurante(Document):
    nome = StringField(required=True, max_length=100)
    descricao = StringField(required=True, max_length=100)
    telefone = StringField(max_length=20)
    localizacao = StringField(max_length=20)
    opcoes = ListField(EmbeddedDocumentField(Opcao))
   
    def __str__(self):
        return f"{self.nome} - {self.email} - {self.telefone}"

#----------------------

def criar_Restaurante():
    nome = input("Nome do Restaurante: ")
    descricao = input("Descrição: ")
    telefone = input("Telefone: ")
    localizacao = input("Localização: ")

    restaurante = Restaurante(nome=nome, descricao=descricao, telefone=telefone, localizacao=localizacao)
    restaurante.save()

    publish_message("log_acoes", f"Restaurante criado: {nome}")

    print(f"Restaurante '{nome}' cadastrado com sucesso!")

def adicionar_Opcao():
    listar_Restaurantes()
    nome_res = input("Digite o nome do Restaurante: ")
    restaurante = Restaurante.objects(nome=nome_res).first()
    if not restaurante:
        print("Restaurante não encontrado!")
        return
    print("--Digite as credencias de Opção--")
    nome = input("Nome: ")
    ingredientes = input("Ingredientes: ")
    preco = input("Preço: ")
    nova_opcao = Opcao(nome=nome, ingredientes=ingredientes, preco=preco)
    restaurante.opcoes.append(nova_opcao)
    restaurante.save()

    publish_message("log_acoes", f"Opção adicionada: {nome}")

    print(f"Opção '{nome}'adicionada ao restaurante {restaurante.nome}!")

#--------------

def listar_Restaurantes():
    if Restaurante.objects.count() > 0:
        print("\n>---Restaurantes---<")
        for r in Restaurante.objects:
            print(f"-> {r.nome} | {r.descricao} | {r.telefone} | {r.localizacao} | id {r.id} |")
    else:
        print("Nenhum Restaurante cadastrado")

def listar_RestauranteId():
    listar_Restaurantes()
    id_res = input("Digite o ID do Restaurante: ")

    try:
        restaurante = Restaurante.objects(id=id_res).first()
    except:
        print("ID inválido!")
        return

    if not restaurante:
        print("Restaurante não encontrado!")
        return

    print("\n>---Restaurante Encontrado---<")
    print(f"Nome: {restaurante.nome}")
    print(f"Descrição: {restaurante.descricao}")
    print(f"Telefone: {restaurante.telefone}")
    print(f"Localização: {restaurante.localizacao}")
    print(f"ID: {restaurante.id}")

def listar_Opcoes_Restaurante():
    listar_Restaurantes()
    nome_res = input("Digite o nome do Restaurante: ")
    restaurante = Restaurante.objects(nome=nome_res).first()
    if not restaurante:
        print("Restaurante não encontrado!")
        return
    if not restaurante.opcoes:
        print("Nenhuma Opção cadastrada")
        return
   
    print(f"\n>---Opções do Restaurante '{nome_res}'---<")
    for o in restaurante.opcoes:
        print(f"-> {o.nome} | {o.ingredientes} | {o.preco} |")

def listar_OpcaoId():
    listar_Restaurantes()
    id_res = input("Digite o ID do Restaurante: ")

    try:
        restaurante = Restaurante.objects(id=id_res).first()
    except:
        print("ID inválido!")
        return

    if not restaurante:
        print("Restaurante não encontrado!")
        return

    if not restaurante.opcoes:
        print("Nenhuma opção cadastrada neste restaurante!")
        return

    print(f"\nOpções de {restaurante.nome}:")
    for i, o in enumerate(restaurante.opcoes):
        print(f"{i} - {o.nome} | {o.ingredientes} | {o.preco}")

    print()
    idx = input("Digite o índice da opção: ")

    if not idx.isdigit() or int(idx) >= len(restaurante.opcoes):
        print("Índice inválido!")
        return

    opcao = restaurante.opcoes[int(idx)]

    print("\n>---Opção Encontrada---<")
    print(f"Nome: {opcao.nome}")
    print(f"Ingredientes: {opcao.ingredientes}")
    print(f"Preço: R$ {opcao.preco}")

#-----------------

def atualizar_Restaurante():
    listar_Restaurantes()
    restaurante_nome = input("Digite o Nome do restaurante a ser atualizado: ")
    restaurante = Restaurante.objects(nome=restaurante_nome).first()
    if not restaurante:
        print("Restaurante não encontrado!")
        return
    novo_telefone = input(f"Novo Telefone para '{restaurante.nome}': ")
    restaurante.telefone = novo_telefone
    restaurante.save()

    publish_message("log_acoes", f"Restaurante atualizado: {restaurante.nome}")

    print(f"Telefone atualizado para {novo_telefone}!")

def atualizar_Opcao():
    listar_Restaurantes()
    nome_res = input("Digite o nome do Restaurante: ")
    restaurante = Restaurante.objects(nome=nome_res).first()
    if not restaurante:
        print("Restaurante não encontrado!")
        return
    if not restaurante.opcoes:
        print(f"Restaurante '{nome_res}' sem Opções cadastradas!")
        return
   
    print(f"\n>---Opções do Restaurante '{nome_res}'---<")
    for o in restaurante.opcoes:
            print(f"-> {o.nome} | {o.preco} |")
   
    nome_opcao = input("Digite o nome da opção a ser atualizada: ")
    opcao = next((o for o in restaurante.opcoes if o.nome == nome_opcao), None)
    if not opcao:
        print("Opção não encontrada!")
        return
    novo_preco = input(f"Novo Preço para '{opcao.nome}': ")
    novo_preco = float(novo_preco)
    opcao.preco = novo_preco
    restaurante.save()

    publish_message("log_acoes", f"Restaurante atualizado: {opcao.nome}")

    print(f"Preço atualizado para {novo_preco}!")

#-------------------

def deletar_Restaurante():
    listar_Restaurantes()
    nome_res = input("Digite o Nome do Restaurante a ser deletado: ")
    restaurante = Restaurante.objects(nome=nome_res).first()
    if not restaurante:
        print(f"Restaurante '{nome_res}' não encontrado!")
        return
    restaurante.delete()

    publish_message("log_acoes", f"Restaurante deletado: {nome_res}")

    print(f"O Restaurante '{nome_res}' e todas as suas opções foram removidas!")

def deletar_Opcao():
    listar_Restaurantes()
    nome_res = input("Digite o nome do Restaurante: ")
    restaurante = Restaurante.objects(nome=nome_res).first()
    if not restaurante:
        print("Restaurante não encontrado!")
        return
    if not restaurante.opcoes:
        print(f"Restaurante '{nome_res}' sem Opções cadastradas!")
        return
    print(f"\n>---Opções do Restaurante '{nome_res}'---<")
    for o in restaurante.opcoes:
        print(f"- {o.nome} | {o.preco} |")

    nome_opcao = input("Digite o nome da opção a ser deletada: ")
    opcao = next((o for o in restaurante.opcoes if o.nome == nome_opcao), None)
    if not opcao:
        print("Opção não encontrada!")
        return
    restaurante.opcoes = [o for o in restaurante.opcoes if o.nome != nome_opcao]
    restaurante.save()

    publish_message("log_acoes", f"Restaurante deletado: {nome_opcao}")

    print(f"A opção '{nome_opcao}' foi removida do Restaurante '{nome_res}'!")

#---------------------

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print()
        print("1 - Criar Restaurante")
        print("2 - Adicionar Opção")
        print()
        print("3 - Listar Restaurantes")
        print("4 - Listar um Restaurante")
        print("5 - Listar Opções por Restaurante")
        print("6 - Listar uma opção")
        print()
        print("7 - Atualizar Restaurante")
        print("8 - Atualizar Opção")
        print()
        print("9 - Deletar Restaurante")
        print("10 - Deletar Opção")
        print()
        print("0 - Sair")
        print()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_Restaurante()
        elif opcao == "2":
            adicionar_Opcao()

        elif opcao == "3":
            listar_Restaurantes()
        elif opcao == "4":
            listar_RestauranteId()
        elif opcao == "5":
            listar_Opcoes_Restaurante()
        elif opcao == "6":
            listar_OpcaoId()

        elif opcao == "7":
            atualizar_Restaurante()
        elif opcao == "8":
            atualizar_Opcao()

        elif opcao == "9":
            deletar_Restaurante()
        elif opcao == "10":
            deletar_Opcao()
       
        elif opcao == "0":
            print("Saindo da aplicação...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
   