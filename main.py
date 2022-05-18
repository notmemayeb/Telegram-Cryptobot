import requests
import telebot
from auth_data import token
from datetime import datetime

hour_emoji = u"\U0001F551"
date_emoji = u"\U0001F5D3"
dollar = u"\U0001F4B2"
link = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD'

def get_data(url):
    req = requests.get(url)
    response = req.json()
    btc_price = round(response['BTC']['USD'],2)
    eth_price = round(response['ETH']['USD'],2)

    return btc_price, eth_price

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hello! Would you like to know the value of cryptocurrencies? Type "/price" to find it out!')

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text.lower() == '/price':
            try:
                btc, eth = get_data(link)
                date = datetime.now().strftime('%Y-%m-%d')
                hour = datetime.now().strftime('%H:%M')
                bot.send_message(
                    message.chat.id,
                    f'{date_emoji}Today is {date}\n{hour_emoji}Tt\'s {hour}\n{dollar}Bitcoin price is {btc}$\n{dollar}Etherium price is {eth}$'
                )
            except Exception as exc:
                print(exc)
                bot.send_message(message.chat.id, 'Damn...Something went wrong!')
        else:
            bot.send_message(message.chat.id, 'Yo! You wrote wrong command!')
    bot.polling()

def main():
    telegram_bot(token)

if __name__ == '__main__':
    main()