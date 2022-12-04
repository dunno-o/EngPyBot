from bs4 import BeautifulSoup
import requests
from os import path, remove
import re


class GiaParser:
    def __init__(self):
        self._BASE_DOMAIN = 'sdamgia.ru'
        self._SUBJECT_BASE_URL = {
            'math': f'https://math-ege.{self._BASE_DOMAIN}',
            'mathb': f'https://mathb-ege.{self._BASE_DOMAIN}',
            'en': f'https://en-ege.{self._BASE_DOMAIN}'}

    def get_problem_by_id(self, subject, id):
        page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}')
        soup = BeautifulSoup(page.content, 'html.parser')

        probBlock = soup.find('div', {'class': 'prob_maindiv'})
        if probBlock is None:
            return None

        CONDITION, CONDITION_TITLE, CONDITION_TEXT, SOLUTION, ANSWER = ' ', ' ', ' ', ' ', ' '
        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'

        try:
            TOPIC_ID = ' '.join(probBlock.find('span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        except:
            return None

        try:
            CONDITION = probBlock.find_all('p', {'class': 'left_margin'})[0].text.split('.')[0]
        except:
            pass

        try:
            CONDITION_TITLE = probBlock.find_all('center')[0].text
        except:
            pass

        try:
            CONDITION_TEXT = probBlock.find_all('p', {'class': 'left_margin'})[1].text
            if CONDITION_TEXT == ' ':
                CONDITION_TEXT = probBlock.find_all('p', {'class': 'left_margin'})[2].text
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
            'condition': CONDITION,
            'condition_title': CONDITION_TITLE,
            'condition_text': CONDITION_TEXT,
            'solution': SOLUTION,
            'answer': ANSWER,
            'url': URL
        }


parser = GiaParser()
subject = 'en'
# workfile = open('workfile', 'w', encoding="utf-8")

for id in range(3716, 99999):
    print(id)
    problem = parser.get_problem_by_id(subject, str(id))
    if problem is not None and len(problem['topic']) < 3 and 18 < int(problem['topic']) < 30:
        print('----------', id)
        # workfile.write(problem['id'] + '\n')
        # workfile.write(problem['topic'] + '\n')
        # workfile.write(problem['condition']['text'] + '\n')
        # workfile.write(problem['answer'] + '\n')
        # workfile.write('\n\n')

        task_file = open(f'Test_tasks/{problem["topic"]}/{problem["topic"]}_{problem["id"]}.txt', 'w', encoding="utf-8")
        task_file.write(problem['condition'])
        task_file.write('\n')
        # if problem['condition_title'] != ' ':
        #     task_file.write(problem['condition_title'])
        #     task_file.write('\n')
        task_file.write(problem['condition_text'])
        task_file.close()

        ans_file = open(f'Test_answers/{problem["topic"]}/answer_{problem["topic"]}_{problem["id"]}.txt', 'w', encoding="utf-8")
        ans_file.write(problem['answer'].upper().replace(' ', ''))
        ans_file.close()

# workfile.close()
