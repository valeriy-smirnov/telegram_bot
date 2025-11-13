import telebot
from config import TG_TOKEN, keys
from extensions import APIException, APIConverter

bot = telebot.TeleBot(TG_TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<название валюты для перевода> \
<название валюты в которую будет перевод> \
<количество переведимой валюты>\n\
Узнать доступные валюты можно командой /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        
        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров.')
        quote, base, amount = values
        total = APIConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}\nВоспользуйтесь /help и /values')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {keys[quote]} будут стоить {total} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()        