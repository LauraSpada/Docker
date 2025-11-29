# instalação do projeto
    docker compose up -d

# rodar toda a aplicação
    docker-compose up

# menu interativo (app/main.py)
    docker-compose run --build app
        ou
    docker-compose exec app bash
    python app/main.py

# RabbitMQ
    docker-compose up -d rabbitmq

# acessar o painel do RabbitMQ
    http://localhost:15672
        user: guest
        password: guest
