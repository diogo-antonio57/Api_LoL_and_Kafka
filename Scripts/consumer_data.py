# Import Libraries
from kafka import KafkaConsumer

# kafka Parameters
TOPIC = 'League_of_Legends'

print('Connecting to kafka')
consumer = KafkaConsumer(TOPIC)
print('Connected to kafka')
print(f"Reading messages from the topic {TOPIC}")

for msg in consumer:

    # Extract information from kafka
    message = msg.value.decode('utf-8')

    # tranform messagem in variables
    (user_id, name, level, campeao1, maestria1, campeao2, maestria2, campeao3, maestria3) = message.split(',')
    txt = open('/home/diogo/Documentos/Projetos Python/Api_LoL_and_Kafka/data/userID.txt', 'w')


    print(f'{user_id},{name},{level}')