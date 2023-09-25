# Projeto League of Legends API - Diamante Elo Stream

Este projeto é uma aplicação Python que obtém informações da API do League of Legends no elo diamante e gera uma fonte de stream em tempo real. Além disso, ele obtém informações dos jogadores através do ID guardado no arquivo `userID.txt`. Para realizar essa tarefa, utilizamos as seguintes tecnologias: Python, PySpark, Spark Stream e Apache Kafka.

## Pré-requisitos

Antes de executar este projeto, certifique-se de ter as seguintes ferramentas e bibliotecas instaladas:

- Python 3.x
- PySpark
- Spark Stream
- Apache Kafka

Você também precisará de uma chave de API válida do League of Legends para acessar os dados dos jogadores. Certifique-se de configurar essa chave no arquivo de configuração antes de executar o projeto.

## Configuração

1. Clone este repositório para sua máquina local:

   ```
   git clone https://github.com/diogo-antonio57/Api_LoL_and_Kafka.git
   ```

2. Acesse o diretório do projeto:

   ```
   cd Api_Lol_and_Kafka
   ```

3. Crie um arquivo `.env` para armazenar sua chave de API do League of Legends:

   ```
   auth = 'chave-api'
   ```

4. Crie um arquivo `userID.txt` e adicione os IDs dos jogadores que deseja monitorar, um por linha.

## Execução

1. Inicie o Apache Kafka no seu sistema:

   ```
   kafka-server-start.sh config/server.properties
   ```

2. Inicie o produtor de dados executando o seguinte comando:

   ```
   python data_producer.py
   ```

   Isso começará a enviar dados de jogadores para o tópico Kafka.

3. Inicie o consumidor de dados em tempo real usando Spark Stream:

   ```
   spark-submit data_consumer.py
   ```

   O consumidor irá processar os dados em tempo real e gerar saídas de stream com informações dos jogadores no elo diamante.

---
