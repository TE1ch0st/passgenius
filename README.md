# PassGenius
PassGenius - это инструмент командной строки для генерации и сохранения надежных паролей. Этот инструмент создан на Python3 и использует библиотеки hashlib, os, re, sys, urllib.parse, json.


## Установка
Склонируйте репозиторий на свою локальную машину:

```shell
git clone https://github.com/TE1ch0st/passgenius.git
```
## Использование
PassGenius может быть использован для генерации безопасных паролей, а также для их замены на более надежные хеши.

## Вызов справки
```shell
python3 PassGenius.py --help

Список команд
        -h --help : Вызов справки
        gen : Инструмент генерации пароля
         rep (replace) : Инструмент для смены пароля

    -----------------------------
    gen (generate) [flags] - Генерация пароля
         -d --Domain [url] :  URL адрес сайта
         -s --Secret [password] : Мастер пароль для генерации
         -l --Len [number] : Длина пароля (По умолчанию: 25)

    -----------------------------
    rep (replace) [flag] - Замена пароля
         -p --Password [you_password] : Пароль требующий замены
```

## Лицензия
Licensed under the Apache License, Version 2.0

---
Copyright © 2023 TE1ch0st. All rights reserved.