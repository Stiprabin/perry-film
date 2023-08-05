import os
import random
import undetected_chromedriver as uc

from for_request import user_agent_list


# контекстный менеджер
class UnChromedriverManager:

    def __init__(self) -> None:
        # опции браузера
        self.chrome_options = uc.ChromeOptions()

        self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.chrome_options.page_load_strategy = "eager"

        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--user-agent=" + random.choice(user_agent_list))


    def __enter__(self) -> uc.Chrome:
        self.driver = uc.Chrome(
            options=self.chrome_options,
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            version_main=114
        )
        return self.driver


    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.close()
        self.driver.quit()
