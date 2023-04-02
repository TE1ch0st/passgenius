import hashlib
import json
import os
import re
import urllib.parse

from flask import Flask
from flask import render_template, request


def get_hash(string: str, length=-1):
    foo = hashlib.sha256(string.encode('utf-8')).hexdigest()
    return foo[:int(length)]


def get_domain(url: str):
    if not bool(re.findall(r'^(https://|http://)', url)):
        url = 'https://' + url
    foo = urllib.parse.urlsplit(url).netloc.replace('www.', '')
    return foo


def get_replaced_password() -> json:
    home_path = os.path.expanduser('~').replace('\\', '/')
    path = f'{home_path}/.PassGenius/replace.json'
    data = {}
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        ...
    return data


# Изменяет хеш пароля изменяя регистр и добавляя спец символы
def password_format(string: str):
    """
    ba3555216e0aa22eea1d3b6ed -> BA3555216E0A%22ee%1d3b6ed
    4a438cc886eb5c7445ef209c2 -> 4A438CC886EB@c744@ef209c2
    """
    l_1 = l_2 = len(string) // 2
    l_1 = string[:l_1].upper()
    l_2 = string[l_2:]

    char_list = ['!', '#', '@', '%']

    # мудреная система выбора символа на замену
    char = l_2[0]
    l_2 = l_2.replace(char, char_list[l_2.count(l_2[3]) % 4])

    password = f'{l_1}{l_2}'

    """ Проверка пароля на безопасность """
    pattern = re.compile(r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}")

    # Фикс пароля
    if not bool(pattern.findall(password)):
        # Нет букв в нижнем регистре
        if not len((re.findall('[a-z]', password))):
            if len(set(re.findall('[A-Z]', password))) > 1:  # Если есть буквы в верхнем регистре которые можно заменить
                char = str(re.findall('[A-Z]', password)[0])
                password = password.replace(char, char.lower())
            else:  # Если нет букв
                password = 'Tt' + password[2:]

        # Нет букв в верхнем регистре
        elif not len(re.findall('[A-Z]', password)):
            if len(set(re.findall('[a-z]', password))) > 1:  # Если есть буквы в нижнем регистре которые можно заменить
                char = str(re.findall('[a-z]', password)[0])
                password = password.replace(char, char.upper())
            else:  # Если нет букв
                password = 'Tt' + password[2:]

    return password


def password_replace(password: str):
    home_path = os.path.expanduser('~').replace('\\', '/')
    if not os.path.exists(f'{home_path}/.PassGenius'):
        os.mkdir(f'{home_path}/.PassGenius')

    path = f'{home_path}/.PassGenius/replace.json'
    data = {}
    try:
        with open(path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f'Создана таблица хешей: {path}')

    for i in data.items():
        if password == i[1]:  # Повторная замена пароля
            data[i[0]] = password_format(get_hash(password, 25))
            break
    else:
        data[password] = password_format(get_hash(password, 25))

    with open(path, 'w') as file:
        file.write(json.dumps(data, indent=4))
    print('Пароль обновлен')


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('app.html')


@app.route("/generate", methods=["POST"])
def generate():
    domain = get_domain(request.form.get('domain'))
    master_key = request.form.get('secret')
    length = int(request.form.get('len'))
    password = get_hash(f'{master_key}-{domain}', length=length)
    password = password_format(password)
    data = get_replaced_password()
    if password in data.keys():
        return render_template('app.html', answer=True, _pass=data[password])
    else:
        return render_template('app.html', answer=True, _pass=password)


@app.route("/replace", methods=["POST"])
def replace():
    password = request.form.get('oldPass')
    pattern = re.compile(r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}")
    if bool(pattern.findall(password)):
        password_replace(password)
        result = 'Пароль успешно изменен!'
    else:
        result = 'Необходим пароль сгенерированный программой.'
    return render_template('app.html', ranswer=True, _result=result)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
