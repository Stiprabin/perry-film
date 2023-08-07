# import os
# os.chdir('')

import random
import threading
import requests
import webbrowser

# from kivy.config import Config
# Config.set("graphics", "resizable", '0')
# Config.set("graphics", "width", "360")
# Config.set("graphics", "height", "780")

from kivy.core.text import LabelBase
from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET,
        Permission.ACCESS_NETWORK_STATE,
        Permission.ACCESS_WIFI_STATE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE
    ])


# сервер
url = ''

# доменные имена
data_list = [
    'tv1.lordfilm.lu',
    'tv1.lordfilm.black',
    'jelang'
]

# хранилище
storage = JsonStore("storage.json")
storage['data'] = {'url': data_list[-1], 'query': ''}
storage['response_films'] = {'films': [], 'index': 0}


# вернуть фильм из хранилища
def get_response_film(index: int) -> str:
    response_film = storage['response_films']['films'][index]

    text = f"[u]{response_film[0]}[/u]\n\n{response_film[1]}\n\n"
    for link in response_film[2]:
        text += f"[color=#308CE8][ref={link}]{link[:15]}...{link[-4:]}[/ref][/color]\n"

    return text


# основной макет
class MainLayout(MDBoxLayout):
    
    def __init__(self, **kwargs) -> None:
        super(MainLayout, self).__init__(**kwargs)


    def button_lu(self) -> None:
        self.ids.button_lu.md_bg_color = "#363636"
        self.ids.button_black.md_bg_color = "#262626"
        self.ids.button_jelang.md_bg_color = "#262626"
        self.ids.main_label.text = f"Поиск на {data_list[0]}"
        storage['data']['url'] = data_list[0]


    def button_black(self) -> None:
        self.ids.button_lu.md_bg_color = "#262626"
        self.ids.button_black.md_bg_color = "#363636"
        self.ids.button_jelang.md_bg_color = "#262626"
        self.ids.main_label.text = f"Поиск на {data_list[1]}"
        storage['data']['url'] = data_list[1]


    def button_jelang(self) -> None:
        self.ids.button_lu.md_bg_color = "#262626"
        self.ids.button_black.md_bg_color = "#262626"
        self.ids.button_jelang.md_bg_color = "#363636"
        self.ids.main_label.text = "Поиск на Jelang"
        storage['data']['url'] = data_list[-1]


    def button_backward(self) -> None:
        response_films = storage['response_films']
        if not response_films['films']:
            self.ids.response_label.text = "Не ломай приложение, олень!"
        else:
            storage['response_films']['index'] -= 1
            if response_films['index'] == -1: storage['response_films']['index'] = len(response_films['films']) - 1
            self.ids.response_label.text = get_response_film(response_films['index'])


    def button_forward(self) -> None:
        response_films = storage['response_films']
        if not response_films['films']:
            self.ids.response_label.text = "Не ломай приложение, олень!"
        else:
            storage['response_films']['index'] += 1
            if response_films['index'] == len(response_films['films']): storage['response_films']['index'] = 0
            self.ids.response_label.text = get_response_film(response_films['index'])


    """Поиск фильмов"""
    def search(self) -> None:
        if ("  " in self.ids.search_textinput.text) or \
                (self.ids.search_textinput.text == '') or \
                (self.ids.search_textinput.text == ' '):
            self.ids.response_label.text = "Пустой или некорректный запрос!"
        else:
            storage['response_films'] = {'films': [], 'index': 0}
            storage['data']['query'] = self.ids.search_textinput.text
            self.start_search_update_ui()
            threading.Thread(target=self.search_thread).start()


    """Отправка POST-запроса Flask-приложению"""
    def search_thread(self) -> None:
        try:
            response = requests.post(url, data=storage['data'])
            storage['response_films']['films'] = response.json()

            if not storage['response_films']['films']:
                self.ids.response_label.text = "Ничего не удалось найти!"
            else:
                self.ids.response_label.text = get_response_film(0)

        except requests.exceptions.ConnectionError:
            self.ids.response_label.text = "Не удалось подключиться к серверу!"

        except Exception as ex:
            self.ids.response_label.text = "Произошла фатальная ошибка!"

        finally:
            self.finish_search_update_ui()


    """Обновление UI в начале поиска"""
    @mainthread
    def start_search_update_ui(self) -> None:
        self.ids.search_textinput.disabled = True
        self.ids.search_button.disabled = True
        self.ids.del_button.disabled = True
        self.ids.response_label.text = "Поиск произведений киноискусства..."


    """Обновление UI в конце поиска"""
    @mainthread
    def finish_search_update_ui(self) -> None:
        self.ids.search_textinput.disabled = False
        self.ids.search_button.disabled = False
        self.ids.del_button.disabled = False


    """Нажатие на ссылку"""
    def ref_press(self, link: str) -> None:
        if link[-4:] == "m3u8":
            Clipboard.copy(link)
            Factory.BasePopup().open()
        else:
            webbrowser.open(link)


class MobileApp(MDApp):

    """Override"""
    def build(self) -> MDBoxLayout:
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "300"

        LabelBase.register(name="TNR", fn_regular="assets/timesnewromanpsmt.ttf")
        LabelBase.register(name="TNRB", fn_regular="assets/timesnewromanbold.ttf")

        return MainLayout()


if __name__ == '__main__':
    MobileApp().run()
