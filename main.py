import telebot
import random
from telebot import types
import task_dict_path_script as ps

TOKEN = "5533652270:AAFHW6d2ZjjqWneMxv7H9CgKtOltmptDrzw"
bot = telebot.TeleBot(TOKEN)

question_to_user = dict()
query_from_user = dict()
dict_of_paths = ps.dict_of_files([i for i in range(19, 29 + 1)] + [36], "Tasks/task")
unique_id = ps.dict_of_unique_id([i for i in range(19, 29 + 1)] + [36], "Tasks/task")


def answer_to_question(message):
    if message.text.replace(' ', '').upper() == "ANS":
        bot.reply_to(message, '|'.join(question_to_user[message.reply_to_message.id][1]))
        question_to_user.pop(message.reply_to_message.id)
    elif question_to_user[message.reply_to_message.id][2] != "task36" and message.text.replace(' ', '').upper() in question_to_user[message.reply_to_message.id][1]:
        bot.send_message(message.chat.id, 'OK')
        question_to_user.pop(message.reply_to_message.id)
    elif question_to_user[message.reply_to_message.id][2] == "task36":
        wa = "wrong tasks: "
        ok = "right task: "
        c = 0
        for i in range(0, 7):
            if len(message.text) >= 7 and message.text[i] == question_to_user[message.reply_to_message.id][1][i]:
                ok += str(30 + i) + " "
                c += 1
                continue
            wa += str(30 + i) + " "
        ans = wa + "\n" + ok
        if c == 7:
            bot.send_message(message.chat.id, 'OK')
            question_to_user.pop(message.reply_to_message.id)
        else:
            bot.send_message(message.chat.id, ans)
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


def give_question36(path: list) -> list:
    f = open(path[0], 'r')
    question = ''
    for line in f:
        question += line.strip() + '\n'
    f.close()

    f = open(path[1], 'r')
    answer = ""
    for i in range(0, 7):
        answer += f.readline().strip()
    f.close()

    return [question, answer]


def give_task_by_id(message):
    if message.text.isnumeric():
        for i in range(0, 6):
            if int(message.text) - i in unique_id:
                if unique_id[int(message.text) - i][2] != "36":
                    q_a = give_question(unique_id[int(message.text) - i])
                else:
                    q_a = give_question36(unique_id[int(message.text) - i])
                sent_message = bot.send_message(message.chat.id, q_a[0])
                question_to_user[sent_message.id] = [message.chat.id, q_a[1], "task" + unique_id[int(message.text) - i][2]]
                query_from_user.pop(message.reply_to_message.id)
                break
    else:
        bot.send_message(message.chat.id, 'Задание не найдено, введите новое')


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

    item = types.InlineKeyboardButton("Задание 30-36", callback_data="task" + str(36))
    markup.row(item)

    bot.send_message(message.chat.id, 'Выберите номер задания',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.message:
        if "task" in call.data and int(call.data[4::]) != 36:
            q_a = give_question(random.choice(dict_of_paths[call.data]))

            sent_message = bot.send_message(call.message.chat.id, q_a[0])
            question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]
        elif "task" in call.data and int(call.data[4::]) == 36:
            q_a = give_question36(random.choice(dict_of_paths[call.data]))

            sent_message = bot.send_message(call.message.chat.id, q_a[0])
            question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]


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
