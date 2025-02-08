
import telebot
import requests
from datetime import datetime
import logging

logging.basicConfig(filename='bot_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Portas requests
token = "8031326232:AAGcV8rQzJEpBt81zg7rkXNhi9rE-jO5BPk"
chat_id = "-1002317475296"
url = 'https://dic.systemhb.net/api/venda/aplicar'

# Requisição
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Token-Auth': 'ok2gZV49WVPbre4%5MXc2nWR@joQOd',
    'Cookie': 'SAS=t0c3r895c3bog01tb18ev5cg0g; xke=23832d371339119a7b58f9960e7a71fd',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
 
bot = telebot.TeleBot(token)

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Registrar
def post_sell(nickname, patente, valor):
    logging.info(f"Request: nickname={nickname}, patente={patente}, valor={valor}")

    # Corpo da requisição
    body = {
        'nickname': nickname,
        'patente': patente,
        'valor': valor
    }

    try:
        # Retorno 
        response = requests.post(url, headers=headers, data=body)

        # Status da venda
        if response.status_code == 200: 
            bot.send_message(chat_id, f"Venda registrada com sucesso! \nPatente: {patente} \nNickname: {nickname} \nValor: {valor} \nData/Hora: {get_timestamp()}")
            logging.info(f"Venda registrada com sucesso! Patente: {patente}, Nickname: {nickname}, Valor: {valor}")
            logging.info(f"Response status: {response.status_code}")
            logging.info(f"Response body: {response.text}")
        else:
            bot.send_message(chat_id, f"Erro ao registrar a venda. Código de status: {response.status_code}")
            logging.error(f"Erro ao registrar a venda. Código de status: {response.status_code}")
            logging.error(f"Response body: {response.text}")

    except Exception as e:
        bot.send_message(chat_id, f"Erro ao realizar a requisição: {e}")
        logging.error(f"Erro ao realizar a requisição: {e}")

@bot.message_handler(commands=['venda'])
def handle_venda(message):
    api_url = url
    try:
        # Request
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Request success
            data = response.json()
            nickname = data.get('nickname')
            patente = data.get('patente')
            valor = data.get('valor')

            # Chama registro
            post_sell(nickname, patente, valor)
        else:
            bot.send_message(chat_id, f"Erro ao obter as informações da venda. Código de status: {response.status_code}")
            logging.error(f"Erro ao obter as informações da venda. Código de status: {response.status_code}")
            logging.error(f"Response body: {response.text}")

    except Exception as e:
        bot.send_message(chat_id, f"Erro ao realizar a requisição: {e}")
        logging.error(f"Erro ao realizar a requisição: {e}")

bot.polling()
