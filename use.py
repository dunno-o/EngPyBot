import telebot
import random
from telebot import types
import os
import task_dict_path_script as ps

TOKEN = "5533652270:AAFHW6d2ZjjqWneMxv7H9CgKtOltmptDrzw"
bot = telebot.TeleBot(TOKEN)


question_to_user = dict()
query_from_user = dict()
dict_of_paths = ps.dict_of_files([i for i in range(1,  29 + 1)] + [36], "Tasks/task")
unique_id = ps.dict_of_unique_id([i for i in range(1,  29 + 1)] + [36], "Tasks/task")
words = ps.get_list_of_words(os.path.join(os.getcwd(), 'words'))


def answer_to_question(message):
    if message.text.replace(' ', '').upper() == "ANSWER":
        bot.reply_to(message, '|'.join(question_to_user[message.reply_to_message.id][1]))
        question_to_user.pop(message.reply_to_message.id)
    elif question_to_user[message.reply_to_message.id][2] != "task36" and message.text.replace(' ', '').upper() in \
            question_to_user[message.reply_to_message.id][1]:
        bot.send_message(message.chat.id2, 'OK')
        question_to_user.pop(message.reply_to_message.id)
    elif question_to_user[message.reply_to_message.id][2] == "task36":
        wa = "wrong tasks: "
        ok = "right tasks: "
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
    task_id = path[0].split('_')[-1].split('.')[0]
    path_to_audio = os.getcwd() + '/Audio/' + task_id + '.mp3'
    f = open(path[0], 'r')
    question = ''
    for line in f:
        question += line.strip() + '\n'
    f.close()

    f = open(path[1], 'r')
    answer = list(map(str.strip, f.readline().split('|')))
    f.close()

    return [question, answer, path_to_audio]


def give_question1(path: list) -> list:
    task_id = path[0].split('_')[-1].split('.')[0]
    path_to_audio = os.getcwd() + '/Audio/' + task_id + '.mp3'
    f = open(path[0], 'r')
    question = ''
    for i in range(5):
        question += f.readline().strip() + "\n"
    for i in range(7):
        question += f.readline().strip() + " " + f.readline().strip() + "\n"
    f.close()

    f = open(path[1], 'r')
    answer = list(map(str.strip, f.readline().split('|')))
    f.close()

    return [question, answer, path_to_audio]


def give_question3(path: list) -> list:
    task_id = path[0].split('_')[-1].split('.')[0]
    path_to_audio = os.getcwd() + '/Audio/' + task_id + '.mp3'

    question = []
    for i in range(0, 6 + 1):
        cur_path = path[0].split('/')
        if int(cur_path[6][-1]) + i > 9:
            break
        cur_path[6] = cur_path[6][:4] + str(int(cur_path[6][-1]) + i)
        cur_path[7] = str(int(cur_path[7][0]) + i) + cur_path[7][1:]
        new_task_id = str(int(cur_path[7].split('_')[1].split('.')[0]) + i)
        cur_path_7 = cur_path[7].split('_')
        cur_path[7] = cur_path_7[0] + '_' + str(new_task_id) + '.txt'
        cur_path = '/'.join(cur_path)
        cur_question = ''
        f = open(cur_path)
        for line in f:
            cur_question += line.strip() + '\n'
        f.close()
        question.append(cur_question)

    answer = []
    for i in range(0, 6 + 1):
        cur_path = path[1].split('/')
        if int(cur_path[6][-1]) + i > 9:
            break
        cur_path[6] = cur_path[6][:4] + str(int(cur_path[6][-1]) + i)
        cur_path[7] = str(int(cur_path[7][0]) + i) + cur_path[7][1:]
        new_task_id = str(int(cur_path[7].split('_')[1].split('.')[0]) + i)
        cur_path_7 = cur_path[7].split('_')
        cur_path[7] = cur_path_7[0] + '_' + str(new_task_id) + '_ans.txt'
        cur_path = '/'.join(cur_path)
        cur_answer = ''
        f = open(cur_path)
        for line in f:
            cur_answer += line.strip()
        f.close()
        answer.append(cur_answer)

    return [question, answer, path_to_audio]



def give_question10(path: list) -> list:
    f = open(path[0], 'r')
    question = ['']
    for i, line in enumerate(f):
        if i < 11:
            question[0] += line.strip() + '\n'
        elif line.strip():
            question.append(line.strip() + '\n')
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
        print('isnumeric')
        print(message.text)
        print(message.text in unique_id)
        if int(message.text) in unique_id and int(unique_id[int(message.text)][2]) == 1:
            q_a = give_question1(unique_id[int(message.text)])
            audio = open(q_a[2], 'rb')
            bot.send_audio(message.chat.id, audio)
            sent_message = bot.send_message(message.chat.id, q_a[0])
            question_to_user[sent_message.id] = [message.chat.id, q_a[1],
                                                 "task" + unique_id[int(message.text)][2]]

        elif int(message.text) in unique_id and int(unique_id[int(message.text)][2]) == 2:
            q_a = give_question(unique_id[int(message.text)])
            audio = open(q_a[2], 'rb')
            bot.send_audio(message.chat.id, audio)
            sent_message = bot.send_message(message.chat.id, q_a[0])
            question_to_user[sent_message.id] = [message.chat.id, q_a[1],
                                                 "task" + unique_id[int(message.text)][2]]

        elif int(message.text) in unique_id and int(unique_id[int(message.text)][2]) <= 9:
            q_a = give_question3(unique_id[int(message.text)])
            audio = open(q_a[2], 'rb')
            bot.send_audio(message.chat.id, audio)
            sent_message = bot.send_message(message.chat.id, q_a[0][0])
            question_to_user[sent_message.id] = [message.chat.id, q_a[1][0],
                                                 "task" + unique_id[int(message.text)][2]]

        elif int(message.text) in unique_id and int(unique_id[int(message.text)][2]) == 10:
            q_a = give_question10(unique_id[int(message.text)])

            sent_message = bot.send_message(message.chat.id, q_a[0][0])
            question_to_user[sent_message.id] = [message.chat.id, q_a[1], "task" + unique_id[int(message.text)][2]]
            for i in range(1, len(q_a[0])):
                bot.send_message(message.chat.id, q_a[0][i])

        else:
            for i in range(0, 6):
                if int(message.text) - i in unique_id:
                    if unique_id[int(message.text) - i][2] != "36":
                        q_a = give_question(unique_id[int(message.text) - i])
                    else:
                        q_a = give_question36(unique_id[int(message.text) - i])
                    sent_message = bot.send_message(message.chat.id, q_a[0])
                    question_to_user[sent_message.id] = [message.chat.id, q_a[1],
                                                         "task" + unique_id[int(message.text) - i][2]]
                    query_from_user.pop(message.reply_to_message.id)
                    break
    else:
        bot.send_message(message.chat.id, "Incorrect task id. Try again.")


def query_handler_back(call):
    if call.message:
        if "audio" in call.data:
            markup = types.InlineKeyboardMarkup(row_width=4)
            for i in range(1, 2 + 1):
                item = types.InlineKeyboardButton("Task " + str(i), callback_data="task" + str(i))
                markup.row(item)

            item = types.InlineKeyboardButton("Task " + "3-9", callback_data="task3")
            markup.row(item)

            bot.send_message(call.message.chat.id, 'Select task number',
                             reply_markup=markup)

        elif "reading" in call.data:
            markup = types.InlineKeyboardMarkup(row_width=4)
            for i in range(10, 18 + 1):
                item = types.InlineKeyboardButton("Task " + str(i), callback_data="task" + str(i))
                markup.row(item)

            bot.send_message(call.message.chat.id, 'Select task number',
                             reply_markup=markup)

        elif "grammar" in call.data:
            markup = types.InlineKeyboardMarkup(row_width=4)
            for i in range(19, 29 + 1):
                item = types.InlineKeyboardButton("Task " + str(i), callback_data="task" + str(i))
                markup.row(item)

            item = types.InlineKeyboardButton("Task 30-36", callback_data="task36")
            markup.row(item)

            bot.send_message(call.message.chat.id, 'Select task number',
                             reply_markup=markup)

        elif "task" in call.data:
            if int(call.data[4::]) <= 2:
                if int(call.data[4::]) == 1:
                    q_a = give_question1(random.choice(dict_of_paths[call.data]))

                elif int(call.data[4::]) == 2:
                    q_a = give_question(random.choice(dict_of_paths[call.data]))

                audio = open(q_a[2], 'rb')
                bot.send_voice(call.message.chat.id, audio)
                sent_message = bot.send_message(call.message.chat.id, q_a[0])
                question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]

            elif int(call.data[4::]) == 3:
                q_a = give_question3(random.choice(dict_of_paths[call.data]))

                audio = open(q_a[2], 'rb')
                bot.send_voice(call.message.chat.id, audio)
                for i in range(7):
                    sent_message = bot.send_message(call.message.chat.id, str(3 + i) + '. ' + q_a[0][i])
                    question_to_user[sent_message.id] = [call.message.chat.id, q_a[1][i], call.data]

            elif int(call.data[4::]) == 10:
                q_a = give_question10(random.choice(dict_of_paths[call.data]))

                sent_message = bot.send_message(call.message.chat.id, q_a[0][0])
                question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]
                for i in range(1, len(q_a[0])):
                    bot.send_message(call.message.chat.id, q_a[0][i])

            elif int(call.data[4::]) == 36:
                q_a = give_question36(random.choice(dict_of_paths[call.data]))

                sent_message = bot.send_message(call.message.chat.id, q_a[0])
                question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]

            elif int(call.data[4::]) != 36:
                q_a = give_question(random.choice(dict_of_paths[call.data]))

                sent_message = bot.send_message(call.message.chat.id, q_a[0])
                question_to_user[sent_message.id] = [call.message.chat.id, q_a[1], call.data]