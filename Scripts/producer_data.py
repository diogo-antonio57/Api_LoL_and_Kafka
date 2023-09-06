# Import libraries
import random
from time import sleep, time, ctime
from kafka import KafkaProducer
import requests
import dotenv
import os

list_mastery = []

# Encontra o arquivo .env e direcionamento das variáveis
dotenv.load_dotenv(dotenv.find_dotenv())
auth = os.getenv('auth')

# Get the usernames from .txt
username_id_list = []
txt = open('/home/diogo/Documentos/Projetos Python/Api_LoL_and_Kafka/data/userID.txt', 'r')

for line in txt:
    username = line.replace('\n','')
    username_id_list.append(username)

# Create the producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
TOPIC = 'League_of_Legends'

# for Id in range(len(username_id_list)):
for n in range(15):

    # print(random.choice(username_id_list))
    user_id = random.choice(username_id_list)
    
    # Get the username and level 
    url = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/{user_id}?api_key={auth}'
    response = requests.get(url)
    json_content = response.json()
    name = json_content['name']
    level = json_content['summonerLevel']

    # Get the top 3 champions with highest mastery
    url = f'https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}/top?api_key={auth}'
    response = requests.get(url)
    json_content = response.json()
    for line in json_content:
        list_mastery.append((line['championId'], line['championPoints']))

    campeao1 = list_mastery[0][0]
    maestria1 = list_mastery[0][1]

    campeao2 = list_mastery[1][0]
    maestria2 = list_mastery[1][1]

    campeao3 = list_mastery[2][0]
    maestria3 = list_mastery[2][1]

    # Create the message
    message = '{' + f"'user_id':'{user_id}','name':'{name}','level':{level},'campeao1':'{campeao1}',"\
                    f"'maestria1':{maestria1},'campeao2':'{campeao2}','maestria2':{maestria2},"\
                    f"'campeao3':'{campeao3}','maestria':{maestria3}" + '},'

    print(message)
    message = bytearray(message.encode("utf-8"))

    # Producer send message for topic
    producer.send(TOPIC, message)

    sleep(3)
