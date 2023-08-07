import json
import time
import random

from soup import get_soup
from for_request import data_list
from unchromedriver_manager import UnChromedriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parser(
    url: str,
    query: str,
    search_id: str
) -> list:

    with UnChromedriverManager() as driver:

        films = []
        driver.get(url)

        # поиск фильмов
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, search_id))).send_keys(query + Keys.ENTER)

        time.sleep(random.randint(5, 7))

        current_url = driver.current_url
        print("Поиск произведений киноискусства на", current_url, "...")

        # ссылки на страницы с фильмами и названия фильмов
        link_page_list = driver.find_elements(By.XPATH, "//a[@class='th-in with-mask']")
        names = driver.find_elements(By.XPATH, "//div[@class='th-title']")

        link_page_list = [link.get_attribute("href") for link in link_page_list][:10]
        names = [name.text for name in names][:10]

        print(f"Найдено: {len(link_page_list)}\nПоиск ссылок на скачивание ...")

    for link_page, name in zip(link_page_list, names):
        try:
            soup = get_soup(link_page)

            # описание
            description = soup.find("div", {'class': 'fdesc clearfix slice-this'})
            if description is None:
                description = "Описание отсутствует"
            else:
                description = ' '.join(description.text.split())

            # фреймы с фильмами
            if url == data_list[0][1]:
                link_frame_list = soup.find_all("iframe", {'src': True, 'id': False, 'class': False})
                links = [link_frame.get("src") for link_frame in link_frame_list]
                for link in links:
                    if "trailer" in link: links.remove(link)
                    elif "api.ebder.ws" in link: links[links.index(link)] = "https:" + link

            elif url == data_list[1][1]:
                link_frame_list = soup.find_all("iframe", {'class': 'lazyFrame'})
                links = [link_frame.get("data-frame") for link_frame in link_frame_list]
                for link in links:
                    if "youtube" in link: links.remove(link)
                    elif "getvideo" in link: links[links.index(link)] = current_url + link

            for index, link in enumerate(links, start=0):

                # если найденное чудо является сериалом
                if ("multserial" in link_page) or \
                        ("serial" in link_page) or \
                        ("anime" in link_page):
                    if "https://vid" in link: del links[index]

                # если является фильмом
                else:
                    if "https://vid" in link:
                        with UnChromedriverManager() as driver:
                            
                            driver.get(link)
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "body"))).click()
                            time.sleep(random.randint(5, 7))

                            # сетевые ресурсы
                            har = driver.execute_script("""
                            const har = window.performance.getEntries();
                            return JSON.stringify(har);
                            """)

                            # ссылка на m3u8
                            for entry in json.loads(har):
                                if entry['name'][-4:] == "m3u8":
                                    links[index] = entry['name']
                                    break

                            if "https://vid" in links[index]: del links[index]

            # добавить фильм в список
            links.append(link_page)
            films.append([
                name,
                description,
                links
            ])

        except Exception as ex:
            print("[LORDFILM] Фатальная ошибка:", ex)

        finally:
            continue

    print("Поиск завершен!")
    return films
