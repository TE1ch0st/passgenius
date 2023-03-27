#!/bin/python3
import hashlib
import os
import re
import sys
import urllib.parse
import json


logo = """
$$$$$$$$\ $$$$$$$$\   $$\             $$\        $$$$$$\              $$\     
\__$$  __|$$  _____|$$$$ |            $$ |      $$$ __$$\             $$ |    
   $$ |   $$ |      \_$$ |   $$$$$$$\ $$$$$$$\  $$$$\ $$ | $$$$$$$\ $$$$$$\   
   $$ |   $$$$$\      $$ |  $$  _____|$$  __$$\ $$\$$\$$ |$$  _____|\_$$  _|  
   $$ |   $$  __|     $$ |  $$ /      $$ |  $$ |$$ \$$$$ |\$$$$$$\    $$ |    
   $$ |   $$ |        $$ |  $$ |      $$ |  $$ |$$ |\$$$ | \____$$\   $$ |$$\ 
   $$ |   $$$$$$$$\ $$$$$$\ \$$$$$$$\ $$ |  $$ |\$$$$$$  /$$$$$$$  |  \$$$$  |
   \__|   \________|\______| \_______|\__|  \__| \______/ \_______/    \____/ 
   """


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


def main():
    args = sys.argv
    length = 25
    domain = ''
    master_key = ''

    help_string = f"""
    {logo}
    
    Список команд
    \t-h --help : Вызов справки
    \tgen : Инструмент генерации пароля
    \t rep (replace) : Инструмент для смены пароля
    
    -----------------------------
    gen (generate) [flags] - Генерация пароля
    \t -d --Domain [url] :  URL адрес сайта
    \t -s --Secret [password] : Мастер пароль для генерации
    \t -l --Len [number] : Длина пароля (По умолчанию: 25)
    
    -----------------------------
    rep (replace) [flag] - Замена пароля
    \t -p --Password [you_password] : Пароль требующий замены
    """

    try:
        match args[1]:
            case "-h" | "--help":
                print(help_string)
            case 'gen' | 'generate':
                try:
                    # Собираем флаги
                    for i in range(1, int((len(args)-2)/2+1)):
                        match args[2*i]:
                            case '-d' | '--Domain':
                                domain = get_domain(args[2*i+1])
                            case '-s' | '--Secret':
                                master_key = args[2*i+1]
                            case '-l' | '--Len':
                                length = args[2*i+1]
                    # Если все необходимое собрали
                    if domain and master_key:
                        password = get_hash(f'{master_key}-{domain}', length=length)
                        password = password_format(password)

                        data = get_replaced_password()
                        if password in data.keys():
                            print(f'Пароль ({domain}): {data[password]}')
                        else:
                            print(f'Пароль ({domain}): {password}')
                    else:
                        print(help_string)
                except IndexError:
                    print(help_string)
            case 'rep' | 'replace':
                if args[2] == '-p' or args[2] == '--Password':
                    password = args[3]
                    pattern = re.compile(r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}")
                    if bool(pattern.findall(password)):
                        password_replace(password)
                    else:
                        print('Необходим пароль сгенерированный программой')
                else:
                    print(help_string)
            case _:
                print(help_string)
    except IndexError:
        print(help_string)


if __name__ == '__main__':
    main()
