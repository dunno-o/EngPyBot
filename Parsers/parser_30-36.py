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

        TEXT, CONDITION_TITLE, CONDITION_TEXT, SOLUTION, ANSWER = ' ', ' ', ' ', ' ', ' '
        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'

        try:
            TOPIC_ID = ' '.join(probBlock.find('span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        except:
            return None

        try:
            TEXT = probBlock.find_all('p', {'class': 'left_margin'})[5].text
            if len(TEXT) < 70:
                TEXT = probBlock.find_all('p', {'class': 'left_margin'})[6].text
            if len(TEXT) < 70:
                TEXT = probBlock.find_all('p', {'class': 'left_margin'})[7].text
            if len(TEXT) < 70:
                TEXT = probBlock.find_all('p', {'class': 'left_margin'})[8].text
        except:
            pass

        try:
            CONDITION_TITLE = probBlock.find_all('center')[0].text
        except:
            pass

        try:
            CONDITION_TEXT = probBlock.find_all('p', {'class': 'left_margin'})[1].text
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
            'condition': TEXT,
            'condition_title': CONDITION_TITLE,
            'condition_text': CONDITION_TEXT,
            'solution': SOLUTION,
            'answer': ANSWER,
            'text': TEXT,
            'url': URL
        }


parser = GiaParser()
subject = 'en'
# workfile = open('workfile', 'w', encoding="utf-8")

for id in range(8654, 99999):
    print(id)
    problem = parser.get_problem_by_id(subject, str(id))
    if problem is not None and len(problem['topic']) < 3 and int(problem['topic']) == 30:
        print('----------', id)

        task_file = open(f'Test_tasks/30-36/30-36_{id}.txt', 'w', encoding="utf-8")

        answers = ''
        task = ''
        for i in range(7):
            problem = parser.get_problem_by_id(subject, str(id + i))
            cur_task = problem['condition_text']
            cur_task = re.sub(r'(  )', ' ', cur_task)
            cur_task = re.sub(r'([0-9])', r'   \1', cur_task)
            cur_task = str(30 + i) + ": " + cur_task
            task += cur_task + '\n'
            answers += problem['answer'].upper().replace(' ', '').replace('.', '') + '\n'

        task += '\n' + problem['text']
        task_file.write(task)
        task_file.close()
        ans_file = open(f'Test_answers/30-36/answer_30-36_{id}.txt', 'w', encoding="utf-8")
        ans_file.write(answers)
        ans_file.close()
