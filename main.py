import telebot
import random
from telebot import types
import task_dict_path_script as ps

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

question_to_user = dict()
query_from_user = dict()
dict_of_paths = ps.dict_of_files([i for i in range(19, 29 + 1)], "Tasks/task")
unique_id = ps.dict_of_unique_id([i for i in range(19, 29 + 1)], "Tasks/task")


def answer_to_question(message):
    if message.text.replace(' ', '').upper() in question_to_user[message.reply_to_message.id][1]:
        bot.send_message(message.chat.id, 'OK')
        question_to_user.pop(message.reply_to_message.id)
    else:
        bot.send_message(message.chat.id, 'WA, try again')


def give_question(path: list) -> list:
    f = open(path[0], 'r')
    question = f.readline().strip() + "\n" + f.readline().strip()
    f.close()

    f = open(path[1], 'r')
    answer = list(map(str.strip, f.readline().split('|')))
    f.close()

    return [question, answer]


def give_task_by_id(message):
    if message.text in unique_id:
        q_a = give_question(unique_id[message.text])
        sent_message = bot.send_message(message.chat.id, q_a[0])
        question_to_user[sent_message.id] = [message.chat.id, q_a[1]]
        query_from_user.pop(message.reply_to_message.id)
    else:
        bot.send_message(message.chat.id, 'Задания не найдено, введите новое')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, пиши /help')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Чекай про меня тут ')


@bot.message_handler(commands=["give_task"])
def button_message(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    for i in range(19, 29 + 1):
        item = types.InlineKeyboardButton("Задание " + str(i), callback_data="task" + str(i))
        markup.row(item)

    bot.send_message(message.chat.id, 'Выбирите номер задания',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.message:
        if "task" in call.data:
            q_a = give_question(random.choice(dict_of_paths[call.data]))

            sent_message = bot.send_message(call.message.chat.id, q_a[0])
            question_to_user[sent_message.id] = [call.message.chat.id, q_a[1]]


@bot.message_handler(commands=["find_task"])
def button_message(message):
    sent_message = bot.send_message(message.chat.id, 'В ответном сообщение введите id задания')
    query_from_user[sent_message.id] = message.chat.id


@bot.message_handler(content_types=["text"])
def filter_of_answers(message):
    if message.reply_to_message != None:
        if message.reply_to_message.id in question_to_user and \
                question_to_user[message.reply_to_message.id][0] == message.chat.id:
            answer_to_question(message)
        if message.reply_to_message.id in query_from_user and \
                query_from_user[message.reply_to_message.id] == message.chat.id:
            give_task_by_id(message)


bot.polling(none_stop=True, interval=0)
