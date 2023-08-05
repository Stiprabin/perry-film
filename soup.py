import time
import random
import requests

from typing import Union
from bs4 import BeautifulSoup
from for_request import user_agent_list, referer_list


def get_soup(url: str) -> Union[BeautifulSoup, None]:
    """
    200 - запрос выполнен успешно
    429 - отправлено слишком много запросов
    403 - доступ запрещен
    503 - сервер недоступен
    """
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Referer': random.choice(referer_list)
    }
    response = requests.get(url=url, headers=headers)

    if response.status_code == 429:
        print("[REQUESTS] Отправлено слишком много запросов. Пойду посплю...")
        time.sleep(3)
        return get_soup(url)

    elif response.status_code != 200:
        print("[REQUESTS] Фатальная ошибка:", response.status_code)
        time.sleep(10)
        return

    soup = BeautifulSoup(response.text, "lxml")
    return soup
