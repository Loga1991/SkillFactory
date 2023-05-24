import telebot
from config import keys, token
from extensions import ConvertionException, CryptoConverter

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты цену которой он хочет узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список доступных валют:/values"
    bot.reply_to (massage, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler()
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException("Слишком много параметров")
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду.\n{e}')
    else:
        text = f'Цена за {amount} {quote} = {float(total_base)*float(amount)} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
