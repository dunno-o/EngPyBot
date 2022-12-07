from bs4 import BeautifulSoup
import requests
from os import path, remove
import re


def save_audio(link, id):
    filename = link.split('/')[-1]
    r = requests.get(link, allow_redirects=True)
    open(f'Audio/{id}_{filename}', 'wb').write(r.content)


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

        TASK, AUDIO_LINK, SOLUTION, ANSWER = ' ', ' ', ' ', ' '
        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'

        try:
            TOPIC_ID = ' '.join(probBlock.find('span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        except:
            return None

        try:
            TASK = probBlock.find_all('p', {'class': 'left_margin'})[0].text
            TASK = TASK.replace('1)', '\n1)')
            TASK = TASK.replace('1.\n', '1)')
            TASK = TASK.replace('ГоворящийABCDEFУтверждение', '')
            TASK = TASK.replace('Воспользуйтесь плеером, чтобы прослушать запись.', '')
            split_dot = TASK.split('.')
            TASK = ''
            for el in split_dot:
                if el.count(' ') != len(el):
                    TASK += el.strip() + '.\n'
        except:
            pass

        try:
            AUDIO_LINK = 'https://en-ege.sdamgia.ru'
            AUDIO_LINK += probBlock.find('audio').get('src')
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
            'solution': SOLUTION,
            'answer': ANSWER,
            'url': URL,
            'audio': AUDIO_LINK
        }


parser = GiaParser()
subject = 'en'
# workfile = open('workfile', 'w', encoding="utf-8")

for id in range(1, 99999):
    print(id)
    problem = parser.get_problem_by_id(subject, str(id))
    if problem is not None and len(problem['topic']) < 3 and 1 <= int(problem['topic']) < 10:
        print('----------', id)
        task_num = int(problem['topic'])
        task_file = open(f'Test_tasks/{task_num}/{task_num}_{id}.txt', 'w', encoding="utf-8")
        task = problem['task']
        task_file.write(task)
        task_file.close()
        ans_file = open(f'Test_answers/{task_num}/{task_num}_{id}_ans.txt', 'w', encoding="utf-8")
        answers = problem['answer'].upper().replace(' ', '').replace('.', '')
        ans_file.write(answers)
        ans_file.close()

        save_audio(problem['audio'], id)
