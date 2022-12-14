import os


def get_list_of_words(path: str) -> list:
    res = []
    for smth in os.scandir(path):
        if not smth.is_file():
            res.append(smth.name)

    return res


def list_of_files_in_dir(path: str) -> list:
    res = list()
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            file_path = os.path.join(dir_path, file)
            file_ans = os.path.join(dir_path.replace('Tasks', 'TasksAnswers'), (file.split('.'))[0] + '_ans.txt')
            res.append([file_path, file_ans])

    return res


def dict_of_files(tasks: list, path: str) -> dict:
    res = dict()
    for i in tasks:
        res['task' + str(i)] = list_of_files_in_dir(os.path.join(os.getcwd(), path + str(i)))

    return res


def find_unique_id(path: str, d: dict):
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            task_n = file.split('_')[0]
            unique_id = file.split('_')[1].split('.')[0]
            file_path = os.path.join(dir_path, file)
            file_ans = os.path.join(dir_path.replace('Tasks', 'TasksAnswers'), (file.split('.'))[0] + '_ans.txt')
            d[int(unique_id)] = [file_path, file_ans, task_n]


def dict_of_unique_id(tasks: list, path: str) -> dict:
    res = dict()
    for i in tasks:
        find_unique_id(os.path.join(os.getcwd(), path + str(i)), res)

    return res


def rename(path: str):
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            ans = file.split('_')
            os.rename(os.path.join(dir_path, file), os.path.join(dir_path, ans[1] + '_' + (ans[2].split('.'))[0] + '_' + 'ans.txt'))


def rename_for(tasks: list, path: str):
    for i in tasks:
        rename(os.path.join(os.getcwd(), path + str(i))) #для переименовки файлов использовалось


def delete_DS_Store(path: str):
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            if file == ".DS_Store":
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)
