import time
import random

from soup import get_soup
from unchromedriver_manager import UnChromedriverManager
from selenium.webdriver.common.by import By


def parser(
    url: str,
    query: str
) -> list:

    films = []
    print("Поиск произведений киноискусства на", url, "...")
    soup = get_soup(url + "?s=" + query)

    # ссылки на страницы с фильмами
    link_page_list = soup.find_all("div", {'class': 'post_content'})[:10]
    print(f"Найдено: {len(link_page_list)}\nПоиск ссылок на скачивание ...")

    for link_page in link_page_list:
        try:
            link_page = link_page.find('a').get("href")
            soup = get_soup(link_page)

            # название
            name = soup.find("h1", {'class': 'insidepost'})
            assert name is not None, "Название отсутствует!"
            name = ' '.join(name.text.split())

            # ссылки на фреймы с фильмами
            link_frame_seasons = soup.find("div", {'class': 'episode_nav'})
            links = []

            # если сезонов нет
            if link_frame_seasons is None:
                link_frame = soup.find("div", {'class': 'player'}).find("iframe", {'src': True}).get("src")
                if (link_frame is not None) and ("vio.to" not in link_frame): links.append(link_frame)
            
            # если сезоны есть
            else:
                link_frame_list = link_frame_seasons.find_all('a', {'href': True})
                for link_frame in link_frame_list:
                    soup = get_soup(link_frame.get("href"))
                    link_frame = soup.find("div", {'class': 'player'}).find("iframe", {'src': True}).get("src")
                    if (link_frame is not None) and ("vio.to" not in link_frame): links.append(link_frame)

            # извлечение ссылок на mp4
            for index, link in enumerate(links, start=0):
                with UnChromedriverManager() as driver:
                    driver.get(link)
                    time.sleep(random.randint(3, 5))
                    links[index] = driver.find_element(By.TAG_NAME, "video").get_attribute("src")

            links.append(link_page)

            # добавить фильм в список
            films.append([
                name,
                "Описание отсутствует",
                links
            ])

        except Exception as ex:
            print("[JELANG] Фатальная ошибка:", ex)

        finally:
            continue

    print("Поиск завершен!")
    return films
