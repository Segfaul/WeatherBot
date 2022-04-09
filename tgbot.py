import telebot
import requests
from random import choice
from bs4 import BeautifulSoup
from cfg import token

bot = telebot.TeleBot(token)
#Ниже представлен массив с user-agent'ами для обхода блок-ки сайтом
user_agentz = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Avast/70.0.917.102', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 (KHTML, like Gecko) Chrome/36 Safari/538', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36']
HEADERS = {
    'user-agent': choice(user_agentz)
}


def Get_Weather():
    try:
        stats = []
        link = 'https://www.tomorrow.io/weather/ru'
        html = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(html.text, "html.parser")
        temp = soup.find(class_='_9oCDP5 DsY3vz').get_text()
        wtw = soup.find(class_='TMYuez').get_text()
        feels = soup.find(class_='ZeyXxG').get_text().split(' ')[-1]
        stats.append(temp); stats.append(wtw); stats.append(feels)
        return stats
    except Exception as e:
        print(repr(e))
        return []
    
@bot.message_handler(commands=['start'])
def Welcom_mess(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, f"&#128313 Приветствую, @{message.from_user.username} &#128313\nНапишите команду &#128073 /day и узнай погоду в своем городе\n", parse_mode='html')
    except Exception as e:
        print('------START------\n\n')
        print(repr(e))
        pass
    
@bot.message_handler(commands=['day'])
def Weather(message):
    try:
        stats = Get_Weather()
        if len(stats) > 0:
            bot.reply_to(message, f"Температура за окном: {stats[0]}\nОщущается как: {stats[-1]}\nСтатус: {stats[1]}", parse_mode='html')
        else:
            bot.reply_to(message, f"К сожалению, сервера временно недоступны\nЗагляните позже")
    except Exception as e:
        print('------WEATHER------\n\n')
        print(repr(e))
        pass
    
bot.polling(none_stop=True)
