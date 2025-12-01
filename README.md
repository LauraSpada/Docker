## DOCKER
    Trabalho sobre conteiners utilizando o framework Docker.
    **objetivo**: executar um único comando e ter o ambiente pronto para testes.

### instalação do projeto
    docker compose up -d

### rodar toda a aplicação
    docker-compose up

### RabbitMQ (message broker)
    docker-compose up -d rabbitmq

    - acessar o painel do RabbitMQ para ver os logs da fila 'eventos'
    http://localhost:15672
        user: guest
        password: guest

### acessar a flask_api
    - testando a saúde do serviço
        curl -X GET http://localhost:5000/health

    - acessando o endpoint da api
        http://localhost:5000/restaurantes

    - exemplos de CRUD para teste (Restaurante e Opção)

        - listar um restaurante
        curl -X GET http://localhost:5000/restaurantes/<id>

        - adicionar um restaurante
        curl -X POST http://localhost:5000/restaurantes -H "Content-Type: application/json" -d '{"nome":"Restaurante Teste","descricao":"Comida deliciosa","telefone":"123456789","localizacao":"Rua Teste, 123","opcoes":[{"nome":"Prato A","ingredientes":"Ingrediente 1, Ingrediente 2","preco":25.5}]}'

        - atualizar o campo de um restaurante
        curl -X PUT http://localhost:5000/restaurantes/<id> -H "Content-Type: application/json" -d '{"telefone":"987654321"}' 

        - deletar restaurante
        curl -X DELETE http://localhost:5000/restaurantes/<id>

        - adicionar uma opção a um restaurante
        curl -X POST http://localhost:5000/restaurantes/<id>/opcoes -H "Content-Type: application/json" -d '{"nome":"Prato B","ingredientes":"Ingrediente X, Ingrediente Y","preco":30.0}'

        - opções por restaurante
        curl -X GET http://localhost:5000/restaurantes/<id>/opcoes

        - atualizar uma opção
        curl -X PUT http://localhost:5000/restaurantes/<id>/opcoes/<nome_opcao> -H "Content-Type: application/json" -d '{"preco":35.0}'

        - deletar opção
        curl -X DELETE http://localhost:5000/restaurantes/<id>/opcoes/<nome_opcao>

### ver os códigos http que a api envia
    docker logs -f flask_api

### ver os logs que o consumer recebe
    docker logs -f consumer

### derrubar os conteiners 
    docker compose down
