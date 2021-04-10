#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.


from pprint import pprint
import requests
import json

username = str(input('nickname of repository: '))
url = 'https://api.github.com'


def github_repos_name(username):
    response = json.loads((requests.get(url+f'/users/{username}/repos')).text)
    #response = requests.get(url+f'/users/{username}/repos')
    #response = json.loads(response.text)

    with open('answer_for_task_1.json', 'w') as f:
        for i in range(len(response)):
            f.write(dict(response[i]).get('name')+'\n')
