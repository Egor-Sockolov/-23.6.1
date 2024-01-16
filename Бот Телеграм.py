import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, APIException
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, @{message.chat.username}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    markup.add(btn1)
    bot.send_message(message.chat.id, f"Я умею конвертировать некоторые валюты. Для начала ознакомься с тем что я умею c помощью команды /help", reply_markup=markup)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы воспроизвести конвертацию отправь мне данные в следующем формате: \n<Имя валюты, цену которой ты хочешь узнать> \
<Имя валюты в которой надо узнать цену первой> \
<Количество первой валюты>'
    bot.reply_to(message, text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btv1 = types.KeyboardButton("/values")
    markup.add(btv1)
    bot.send_message(message.chat.id, f'Для ознакомления с списков валют используй команду /values', reply_markup=markup)


# Вывод всех доступных валют построчно
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# стоимость одного Биткоина в Долларах
# fsym=BTC&tsym=USD

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        get_prise = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {get_prise}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)


