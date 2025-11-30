# instalação do projeto
    docker compose up -d

# rodar toda a aplicação
    docker-compose up

# menu interativo (app/main.py)
    docker-compose run --build app
    ou
    docker-compose run app
        
# RabbitMQ
    docker-compose up -d rabbitmq

# acessar o painel do RabbitMQ para ver os logs da fila 'event'
    http://localhost:15672
        user: guest
        password: guest

# ver os logs do consumer
    docker logs -f event_consumer

# derrubar os conteiners 
    docker compose down
