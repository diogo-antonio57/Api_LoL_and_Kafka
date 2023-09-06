# Import libraries
import requests
import dotenv
import os

# Encontra o arquivo .env e direcionamento das variáveis
dotenv.load_dotenv(dotenv.find_dotenv())
auth = os.getenv('auth')

# Loop FOR that get usernames in diamond I - IV
rank_list = ['I', 'II', 'III', 'IV']
# rank_list = ['I']

for rank in rank_list:

    url = f'https://br1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/{rank}?page=1&api_key={auth}'

    # Requests the content of API
    response = requests.get(url)
    json_content = response.json()

    # write names in file .txt
    user_id = open('/home/diogo/Documentos/Projetos Python/Api_LoL_and_Kafka/data/userID.txt', 'a+')

    for line in json_content:
        user_id.write(line['summonerId'])
        user_id.write('\n')
