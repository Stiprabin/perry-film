import random
import undetected_chromedriver as uc

from for_request import user_agent_list


# контекстный менеджер
class UnChromedriverManager:

    def __init__(self) -> None:
        # опции браузера
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.page_load_strategy = "eager"
        self.chrome_options.arguments.extend([
            '--headless',
            '--start-maximized',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-infobars',
            '--disable-extensions',
            '--user-agent=' + random.choice(user_agent_list)
        ])


    def __enter__(self) -> uc.Chrome:
        self.driver = uc.Chrome(
            version_main=114,
            options=self.chrome_options
        )
        return self.driver


    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.driver.close()
        self.driver.quit()
