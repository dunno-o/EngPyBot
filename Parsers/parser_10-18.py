from bs4 import BeautifulSoup
import requests
from os import path, remove
import re


class GiaParser:
    def __init__(self):
        self._BASE_DOMAIN = 'sdamgia.ru'
        self._SUBJECT_BASE_URL = {
            'en': f'https://en-ege.{self._BASE_DOMAIN}'}

    def get_problem_by_id(self, subject, id):
        page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}')
        soup = BeautifulSoup(page.content, 'html.parser')

        probBlock = soup.find('div', {'class': 'prob_maindiv'})
        if probBlock is None:
            return None

        TASK, TEXT, SOLUTION, ANSWER = ' ', ' ', ' ', ' '
        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'

        try:
            TOPIC_ID = ' '.join(probBlock.find('span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        except:
            return None

        try:
            TASK = probBlock.find_all('p', {'class': 'left_margin'})[0].text
            TASK = TASK.replace('1)', '\n\n1)')
            TASK = TASK.replace('2)', '\n2)')
            TASK = TASK.replace('3)', '\n3)')
            TASK = TASK.replace('4)', '\n4)')

            TASK = TASK.replace('1.', '\n\n1.')
            TASK = TASK.replace('2.', '\n2.')
            TASK = TASK.replace('3.', '\n3.')
            TASK = TASK.replace('4.', '\n4.')
            TASK = TASK.replace('5.', '\n5.')
            TASK = TASK.replace('6.', '\n6.')
            TASK = TASK.replace('7.', '\n7.')
            TASK = TASK.replace('8.', '\n8.')

            TASK = TASK.replace('A.', '\n\nA.')
            TASK = TASK.replace('B.', '\n\nB.')
            TASK = TASK.replace('C.', '\n\nC.')
            TASK = TASK.replace('D.', '\n\nD.')
            TASK = TASK.replace('E.', '\n\nE.')
            TASK = TASK.replace('F.', '\n\nF.')
            TASK = TASK.replace('G.', '\n\nG.')

            TASK = TASK.replace('ГоворящийABCDEFУтверждение', '')
            TASK = TASK.replace('Говорящий', '')
            TASK = TASK.replace('Утверждение', '')
            TASK = TASK.replace('ТекстABCDEFGЗаголовок', '')
            TASK = TASK.replace('ABCDEFG', '')
            TASK = TASK.replace('A–\n\nG', 'A-G')
            TASK = TASK.replace('1–\n7', '1-7')
            TASK = TASK.replace('1–\n8', '1-8')

            TASK = TASK.replace('ПропускABCDEFЧасть предложения', '')
            TASK = TASK.replace('Пропуск', '')
            TASK = TASK.replace('Часть предложения', '')
            TASK = TASK.replace('ABCDEF', '')

            TASK = TASK.replace('в таблицу.', 'в таблицу.\n')
        except:
            pass

        try:
            TEXT = probBlock.find_all('div', {'class': 'probtext'})[0].text
            title = probBlock.find('center').string
            print(title)
            TEXT = TEXT.replace(title, '\n' + title.strip() + '\n\n', 1)
        except:
            pass

        try:
            SOLUTION = probBlock.find_all('div', {'class': 'pbody'})[1].text
        except:
            pass

        try:
            ANSWER = probBlock.find_all('div', {'class': 'answer'})[-1].text.replace('Ответ: ', '')
        except:
            pass

        return {
            'id': id,
            'topic': TOPIC_ID,
            'task': TASK,
            'text': TEXT,
            'solution': SOLUTION,
            'answer': ANSWER,
            'url': URL
        }


parser = GiaParser()
subject = 'en'

for id in range(1, 13000):
    print(id)
    problem = parser.get_problem_by_id(subject, str(id))
    if problem is not None and len(problem['topic']) < 3 and 10 <= int(problem['topic']) <= 18:
        print('----------', id)
        task_num = int(problem['topic'])
        task_file = open(f'Test_tasks/{task_num}/{task_num}_{id}.txt', 'w', encoding="utf-8")
        task = problem['task'] + '\n'
        task += problem['text']
        task_file.write(task)
        task_file.close()
        ans_file = open(f'Test_answers/{task_num}/{task_num}_{id}_ans.txt', 'w', encoding="utf-8")
        answers = problem['answer'].upper().replace(' ', '').replace('.', '')
        ans_file.write(answers)
        ans_file.close()
