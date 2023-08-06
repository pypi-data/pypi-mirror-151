from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from random import choice

os.environ['WDM_LOG'] = '1'
os.environ['WDM_LOG_LEVEL'] = '1'


class Browser:
    user_agents = []

    @classmethod
    def __use_proxy(cls):
        API_KEY = '030bc9e214b3a2eae6bc1fe05e50e4b6'
        return {
            'proxy': {
                'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    @classmethod
    def get_agent(cls):
        if len(Browser.user_agents) > 0:
            return choice(Browser.user_agents)
        exit(1)

    @staticmethod
    def interceptor(request):
        del request.headers['Referer']  # Remember to delete the header first
        request.headers['Referer'] = 'https://google.com.br'  # Spoof the referer

    def __init__(self, use_proxy=False, in_terminal=False, profile_path=None, active_sleep=False):
        self.__active_sleep = active_sleep

        # if use_proxy:
        #     from seleniumwire import webdriver
        # else:
        #     from selenium import webdriver
        options = webdriver.ChromeOptions()
        if in_terminal:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--mute-audio")

        if profile_path is not None:
            if not os.path.exists(profile_path):
                os.makedirs(profile_path)
            options.add_argument("--profile-directory=Default")
            options.add_argument('--user-data-dir=' + profile_path)

        Browser.user_agents = list(map(str.strip, open('resources/user-agents.txt').readlines()))

        options.add_argument("start-maximized")
        options.add_argument("--window-size=1280,800")
        options.add_argument(f'user-agent={Browser.get_agent()}')
        options.add_argument('--disable-dev-sh-usage')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        serv_driver = Service(ChromeDriverManager().install())
        if use_proxy:
            self.driver = webdriver.Chrome(service=serv_driver, options=options,
                                           seleniumwire_options=Browser.__use_proxy())
        else:
            self.driver = webdriver.Chrome(service=serv_driver, options=options)

    def set_headers(self):
        raise NotImplementedError("Please implement this method")

    def test_proxy(self):
        self.driver.get('http://httpbin.org/ip')
        print(self.driver.page_source)

    def delay(self, waiting_time=5):
        self.driver.implicitly_wait(waiting_time)

    def close_driver(self):
        self.driver.close()

    def click(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).click()

    def wait_to_click(self, xpath, time=10):
        return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def wait_frame_switch_to(self, xpath, time=10):
        WebDriverWait(self.driver, time).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))

    def switch_to_frame_default(self):
        self.driver.switch_to.default_content()

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)

    def get_href(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).get_attribute('href')

    def get_src(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).get_attribute('src')

    def get(self, url):
        if self.__active_sleep:
            Utils.time_to_sleep()

        self.driver.request_interceptor = Browser.interceptor
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.get_agent()})
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                  const newProto = navigator.__proto__
                  delete newProto.webdriver
                  navigator.__proto__ = newProto
                  """
        })
        self.driver.get(url)

    def input(self, xpath, send):
        self.driver.find_element(By.XPATH, xpath).send_keys(send)

    def get_text(self, xpath):
        return self.driver.find_element(By.XPATH, xpath).text

    def get_elements(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)


class Utils:
    @staticmethod
    def time_to_sleep(start=2, end=10):
        from time import sleep
        from random import randint
        sleep(randint(start, end))


if __name__ == '__main__':
    bw = Browser()
    print(bw.get_agent())
