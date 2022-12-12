# EngPyBot

## Описание

Бот создан для помощи в подготовке к ЕГЭ по английскому.

## Функционал

**В  боте существует 3 основных функции:**

1. `/give_task` - функция, выдающая задания формата ЕГЭ (все задания взяты с сайта https://ege.sdamgia.ru). 
Ответ вводится в ответном сообщении. Если вы хотите узнать решение задания, то введите "answer" в ответном сообщении. 
Бот не чувстителен к регистру ввода и пробельным символам (т.е. корректным вводом также является "A nsw ER", но рекомендуется вводить нормально, как на ЕГЭ). 
В случае неверного ответа, бот вам напишет: "WA, try again". 
В некоторых заданиях есть частичное решение (вам высвечивается задания, в которых ошибка).
В заданиях 3-9 (аудирование), высылается несколько сообщений, на каждое ответ вводится отдельно.

2. `/find_task` - функция, выдающая задание по уникальному id с сайта https://ege.sdamgia.ru, 
если задание не найдено, то бот напишет: "Incorrect task id. Try again.". 
После выдачи задания взаимодействие происходит аналогично функции /give_task.

3. `/give_word` - функция выдающая случайно слово, его значение, часть речи и аудио с произношением (от google-переводчика)

## Используемые данные

- Задания взяты с сайта https://ege.sdamgia.ru

- Слова взяты с сайта https://www.dictionary.com

- Произношение слов сгенерировано с помощью библиотеки gTTS (Google Text-to-Speech)

## Используемые библиотеки

- Данные парсились с помощью библиотеки "BeautifulSoup" (все парсеры лежат в папке "Parsers" с соответствующими названиями),
также использовались библиотеки: "requests", "os", "re".

- Бот создан с помощью библиотеки "pyTelegramBotAPI"

- В файле "task_dict_path_script.py" находятся функции для сборки путей до файлов с заданиями и ответами, переименования файлов и удаления ненужных.
Использовалась библиотека "os".
