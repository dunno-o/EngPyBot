import random
from telebot import types
import os
from use import bot, query_handler_back, answer_to_question, give_task_by_id, \
                question_to_user, query_from_user, words


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, пиши /help')


@bot.message_handler(commands=["help"])
def send_help_info(message):
    help_info = '- Для выдачи задания тестовой части отправьте команду /give_task\n' \
                '- Для выдачи конкретного задания отправьте команду /find_task, а затем на отправленное вам ' \
                'сообщение ответьте id нужного задания (его можно посмотреть на сатйе РЕШУ ЕГЭ)\n' \
                '- Для выдачи слова отправьте команду /give_word\n' \
                'Подробнее читайте в README'

    bot.send_message(message.chat.id, help_info)


@bot.message_handler(commands=["give_task"])
def choose_task_type(message):
    markup = types.InlineKeyboardMarkup(row_width=4)

    item = types.InlineKeyboardButton("Audio task", callback_data="audio")
    markup.row(item)

    item = types.InlineKeyboardButton("Reading task", callback_data="reading")
    markup.row(item)

    item = types.InlineKeyboardButton("Grammar task", callback_data="grammar")
    markup.row(item)

    bot.send_message(message.chat.id, "Which task would you like to solve?",
                     reply_markup=markup)


@bot.message_handler(commands=["give_word"])
def choose_task_type(message):
    choice = random.choice(words)
    path = os.path.join(os.path.join(os.getcwd(), 'words'), choice)
    meaning = ''
    with open(path + '/meaning', 'r') as f:
        for line in f:
            meaning += line
    meaning = meaning.split('|')
    bot.send_message(message.chat.id, choice + '\n' + '\n' + str(meaning[0]) + '\n' + str(meaning[1]))
    audio = open(path + '/' + choice + '.mp3', 'rb')
    bot.send_voice(message.chat.id, audio)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    query_handler_back(call)


@bot.message_handler(commands=["find_task"])
def button_message(message):
    sent_message = bot.send_message(message.chat.id, "Write the required task id in reply message")
    query_from_user[sent_message.id] = message.chat.id


@bot.message_handler(content_types=["text"])
def filter_of_answers(message):
    if message.reply_to_message is not None:
        if message.reply_to_message.id in question_to_user and \
                question_to_user[message.reply_to_message.id][0] == message.chat.id:
            answer_to_question(message)
        if message.reply_to_message.id in query_from_user and \
                query_from_user[message.reply_to_message.id] == message.chat.id:
            give_task_by_id(message)


bot.polling(none_stop=True, interval=0)
