import hashlib
import json
import os.path
import re
import urllib.parse

import flet as ft


class PassGenius:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'PassGenius'
        self.page.window_width = 400
        self.page.window_height = 500
        self.page.window_resizable = False
        self.page.window_maximizable = False
        self.page.theme_mode = ft.ThemeMode.DARK
        self.color = '#531683'
        self.text_color = '#ffffff'

        self.domain = ft.TextField(label="URL адрес сайта:")
        self.master_key = ft.TextField(label="Мастер пароль:")
        self.length = ft.TextField(label="Длина пароля:", value='25')
        self.old_password = ft.TextField(label="Старый пароль")

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            tabs=[
                ft.Tab(
                    text='Генерация',
                    icon=ft.icons.PASSWORD,
                    content=ft.Container(
                        content=self.generation_tab()
                    ),
                ),
                ft.Tab(
                    text='Замена',
                    icon=ft.icons.CHANGE_CIRCLE_OUTLINED,
                    content=self.replace_tab()
                ),
                ft.Tab(
                    text="Настройки",
                    icon=ft.icons.SETTINGS,
                    content=self.settings_tab()
                ),
            ],
        )

        page.add(self.tabs)

    def generation_tab(self):
        tab = ft.Column(controls=[
            ft.Text("PassGenius", text_align=ft.TextAlign.CENTER, color=self.color,
                    style=ft.TextThemeStyle.DISPLAY_LARGE),
            ft.Divider(opacity=0),
            self.domain,
            self.master_key,
            self.length,
            ft.OutlinedButton(text="Сгенерировать", width=400, on_click=self.generate),
            ft.Text('                 © 2023 TE1ch0st. All rights reserved.', text_align=ft.TextAlign.CENTER)
        ])
        return tab

    def replace_tab(self):
        tab = ft.Column(controls=[
            ft.Text("PassGenius", text_align=ft.TextAlign.CENTER, color=self.color,
                    style=ft.TextThemeStyle.DISPLAY_LARGE),
            ft.Divider(opacity=0),
            self.old_password,
            ft.OutlinedButton(text="Заменить", width=400, on_click=self.replaced),
            ft.Divider(opacity=0, height=140),
            ft.Text('                 © 2023 TE1ch0st. All rights reserved.', text_align=ft.TextAlign.CENTER)
        ])
        return tab

    def settings_tab(self):
        file_picker = ft.FilePicker()
        file_picker.allowed_extensions = [".json"]
        self.page.overlay.append(file_picker)
        self.page.update()
        tab = ft.Column(controls=[
            ft.Column(controls=[
                ft.Text('Выбор темы: ', size=24),
                ft.Switch(label='Темная тема', value=True, on_change=self.change_theme)
            ]),
            ft.Divider(opacity=0),
            ft.Text('Иморт/Экспорт конфигурации: ', size=24),
            ft.Row(controls=[
                ft.OutlinedButton(text="Импорт", width=150,
                                  on_click=lambda _: file_picker.pick_files(allowed_extensions=["json"])),
                ft.OutlinedButton(text="Экспорт", width=150, on_click=self.data_export)
            ]),
            ft.Divider(opacity=0, height=150),
            ft.Text('                 © 2023 TE1ch0st. All rights reserved.', text_align=ft.TextAlign.CENTER)
        ])
        return tab

    def data_import(self):
        home_path = os.path.expanduser('~').replace('\\', '/')
        home_path = f'{home_path}/.PassGenius/replace.json'

        def path(e: ft.FilePickerResultEvent):
            with open(e.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                with open(home_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Данные импортированы",
                            color=self.text_color),
                    bgcolor=self.color)
                self.page.snack_bar.open = True
                self.page.update()

        file_picker = ft.FilePicker(on_result=path)
        file_picker.allowed_extensions = [".json"]
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(dialog_title='Import', allowed_extensions=['json'], allow_multiple=False)

    def data_export(self, e):
        def path(e: ft.FilePickerResultEvent):
            data = PassGenius.get_replaced_password()
            with open(e.path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Данные экспортированы",
                        color=self.text_color),
                bgcolor=self.color)
            self.page.snack_bar.open = True
            self.page.update()

        file_picker = ft.FilePicker(on_result=path)
        file_picker.allowed_extensions = [".json"]
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.save_file(dialog_title='Export', file_name='replace.json', allowed_extensions=['json'])

    def change_theme(self, e):
        match self.page.theme_mode:
            case ft.ThemeMode.DARK:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                self.color = '#2584ff'
                self.text_color = '#000000'
            case ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
                self.color = '#531683'
                self.text_color = '#ffffff'
        self.page.update()

    def generate(self, e):

        if self.domain.value == '':
            self.domain.error_text = 'Некорректное значение'
            self.page.update()
        elif self.master_key.value == '':
            self.master_key.error_text = 'Некорректное значение'
            self.page.update()
        else:
            self.domain.error_text = None
            self.master_key.error_text = None

            try:
                password = PassGenius.get_hash(f'{self.master_key.value}-{PassGenius.get_domain(self.domain.value)}',
                                               length=int(self.length.value))
                if int(self.length.value) < 8 or self.domain.value == '' or self.master_key.value == '':
                    raise ValueError
            except ValueError:
                self.length.error_text = 'Некорректное значение'
                self.page.update(self.length)
            else:
                self.length.error_text = None
                password = PassGenius.password_format(password)
                data = PassGenius.get_replaced_password()
                if password in data.keys():
                    password = data[password]
                self.page.set_clipboard(password)
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Пароль скопирован в буфер обмена ({PassGenius.get_domain(self.domain.value)})",
                            color=self.text_color),
                    bgcolor=self.color)
                self.page.snack_bar.open = True
                self.page.update()

    def replaced(self, e):
        self.old_password.error_text = None
        password = self.old_password.value
        pattern = re.compile(r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}")
        if bool(pattern.findall(password)):
            PassGenius.password_replace(password)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Пароль обновлен", color=self.text_color), bgcolor=self.color)
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.old_password.error_text = 'Необходим пароль сгенерированный программой'
            self.page.update()

    @staticmethod
    def run():
        ft.app(PassGenius)

    @staticmethod
    def get_hash(string: str, length=-1):
        foo = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return foo[:int(length)]

    @staticmethod
    def get_domain(url: str):
        if not bool(re.findall(r'^(https://|http://)', url)):
            url = 'https://' + url
        foo = urllib.parse.urlsplit(url).netloc.replace('www.', '')
        return foo

    @staticmethod
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
    @staticmethod
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
                if len(set(re.findall('[A-Z]',
                                      password))) > 1:  # Если есть буквы в верхнем регистре которые можно заменить
                    char = str(re.findall('[A-Z]', password)[0])
                    password = password.replace(char, char.lower())
                else:  # Если нет букв
                    password = 'Tt' + password[2:]

            # Нет букв в верхнем регистре
            elif not len(re.findall('[A-Z]', password)):
                if len(set(
                        re.findall('[a-z]', password))) > 1:  # Если есть буквы в нижнем регистре которые можно заменить
                    char = str(re.findall('[a-z]', password)[0])
                    password = password.replace(char, char.upper())
                else:  # Если нет букв
                    password = 'Tt' + password[2:]

        return password

    @staticmethod
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
                data[i[0]] = PassGenius.password_format(PassGenius.get_hash(password, length=len(password)))
                break
        else:
            data[password] = PassGenius.password_format(PassGenius.get_hash(password, length=len(password)))

        with open(path, 'w') as file:
            file.write(json.dumps(data, indent=4))
        print('Пароль обновлен')


if __name__ == '__main__':
    PassGenius.run()
