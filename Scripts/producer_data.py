# Import libraries
import random
from time import sleep, time, ctime
from kafka import KafkaProducer
import requests

list_mastery = []

# Read api key and url for get the usernames
with open('/home/diogo/Documentos/Projetos Python/Api_LoL_and_Kafka/data/auth.txt', 'r') as auth_txt:
    auth = auth_txt.readline()

# Get the usernames from .txt
username_id_list = []
txt = open('/home/diogo/Documentos/Projetos Python/Api_LoL_and_Kafka/data/username_ID.txt', 'r')

for line in txt:
    username = line.replace('\n','')
    username_id_list.append(username)

# Create the producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
TOPIC = 'League_of_Legends'

# for Id in range(len(username_id_list)):
for n in range(2):

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
    message = f'{user_id},{name},{level},{campeao1},{maestria1},{campeao2},{maestria2},{campeao3},{maestria3}'
    print(message)
    message = bytearray(message.encode("utf-8"))

    # Producer send message for topic
    producer.send(TOPIC, message)

    sleep(3)
