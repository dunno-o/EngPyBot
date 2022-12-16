import random
from telebot import types
import os
import sqlite3
from use import bot, query_handler_back, answer_to_question, give_task_by_id, \
    question_to_user, query_from_user, words


@bot.message_handler(commands=['start'])
def start_message(message):
    connect = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute("""drop table if exists data;""")
    connect.commit()
    cursor.execute("""create table data(
        id integer primary key autoincrement,
        chat_id int DEFAULT 0,
        success_cnt text DEFAULT "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
        all_cnt text DEFAULT "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        );""")
    connect.commit()
    cursor.execute('INSERT INTO data (chat_id) VALUES (?);', [message.chat.id])
    connect.commit()

    bot.send_message(message.chat.id, 'Привет, пиши /help')


@bot.message_handler(commands=["help"])
def send_help_info(message):
    help_info = '\- Для выдачи задания тестовой части отправьте команду \/give\_task \n' \
                '\- Для выдачи конкретного задания отправьте команду \/find\_task, а затем на отправленное вам сообщение ответьте id нужного задания \(его можно посмотреть на сайте РЕШУ ЕГЭ\) \n' \
                '\- Для выдачи слова отправьте команду \/give\_word \n' \
                'Подробнее читайте в [README](https://github.com/dunno-o/EngPyBot)'

    bot.send_message(message.chat.id, help_info, parse_mode='MarkdownV2')


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


@bot.message_handler(commands=["stats"])
def button_message(message):
    stats = 'Статистика по решённым задачам: \n'
    connect = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute(f"select success_cnt from data where chat_id = {message.chat.id}")
    success_tasks = list(cursor.fetchall()[0])[0]
    success_tasks = success_tasks.split(' ')
    cursor.execute(f"select all_cnt from data where chat_id = {message.chat.id}")
    all_tasks = list(cursor.fetchall()[0])[0]
    all_tasks = all_tasks.split(' ')
    for i in range(0, 29):
        try:
            stats += f'{str(i)}: {success_tasks[i]}/{all_tasks[i]} ({round(int(success_tasks[i]) / int(all_tasks[i]), 2) * 100}%)\n'
        except ZeroDivisionError:
            stats += f'{str(i)}: {success_tasks[i]}/{all_tasks[i]} (0%)\n'
    stats += f'30-36: {success_tasks[-1]}/{all_tasks[-1]}'
    bot.send_message(message.chat.id, stats)


@bot.message_handler(content_types=["text"])
def filter_of_answers(message):
    if message.reply_to_message is not None:
        if message.reply_to_message.id in question_to_user and \
                question_to_user[message.reply_to_message.id][0] == message.chat.id:
            answer_to_question(message)
        if message.reply_to_message.id in query_from_user and \
                query_from_user[message.reply_to_message.id] == message.chat.id:
            give_task_by_id(message)
    else:
        bot.send_message(message.chat.id, "Read /help")


bot.polling(none_stop=True, interval=0)
