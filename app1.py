import telebot


from conf import TOKEN, keys
from exeptions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'sos'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать нужные данные по валютам введите команду в следующем формате (через пробел):' \
           ' \n- Валюта, которую хотите получить  \n- Валюта, которую хотите обменять ' \
           '\n- Количество первой валюты\n \
 Список доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        text_l = message.text.lower()
        values = text_l.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры')

        base, quote, amount = values
        # print(values)
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

