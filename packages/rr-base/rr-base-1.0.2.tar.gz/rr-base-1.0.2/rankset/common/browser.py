from seleniumwire import webdriver as webdriver_wire
from selenium import webdriver as selenium_driver
from browsermobproxy import Server
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumConfig:
    """Default parameters for initiate driver"""

    def __init__(self, chrome_driver_location=None, url='chrome://settings/cookies',
                 headless: bool = False, network: bool = False,
                 page_load_timeout=20, implicitly_wait=10,
                 proxy: bool = False, bob_proxy_path=None, using_wire_package: bool = True):
        self._url = url
        self._headless = headless
        self._network = network
        self.__proxy = proxy
        self.__bob_proxy_path = bob_proxy_path
        self.__using_wire_package = using_wire_package
        self._page_load_timeout = page_load_timeout
        self._implicitly_wait = implicitly_wait
        self.__driver = self.__initiate_driver(chrome_driver_location=chrome_driver_location)
        self.__actions = SeleniumActions(self.__driver)

    @property
    def __get_driver_type(self):
        if self.__using_wire_package:
            return webdriver_wire
        else:
            return selenium_driver

    @property
    def driver(self):
        return self.__driver

    @property
    def actions(self):
        return self.__actions

    @property
    def proxy(self):
        return self.__proxy

    @property
    def session_requests(self):
        if self.__using_wire_package:
            return self.__driver.requests

    @property
    def proxy_server(self):
        server = Server(self.__bob_proxy_path)
        server.start()
        return server.create_proxy()

    def __initiate_driver(self, chrome_driver_location=None):
        """Creates a new instance of the chrome driver.
           Starts the service and then creates new instance of chrome driver.
        :Args
        - url - set end point
        - headless - gives the option to run the tests in the background
        - proxy - gives the option to record the traffic
        :Returns:
             - the driver object"""
        chrome_options = Options()
        capabilities = DesiredCapabilities.CHROME.copy()
        webdriver = self.__get_driver_type

        if self.__proxy:
            self.__proxy = self.proxy_server
            chrome_options.add_argument("--proxy-server={0}".format(self.__proxy.proxy))
            chrome_options.add_argument('--ignore-ssl-errors=yes')
            chrome_options.add_argument('--ignore-certificate-errors')

        if self._headless:
            chrome_options.add_argument("--headless")

        if self._network:
            capabilities = webdriver.DesiredCapabilities.CHROME
            capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        if chrome_driver_location is None:
            driver = webdriver.Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                                      chrome_options=chrome_options,
                                      desired_capabilities=capabilities)
        else:
            driver = webdriver.Chrome(executable_path=chrome_driver_location,
                                      chrome_options=chrome_options,
                                      desired_capabilities=capabilities)

        driver.set_page_load_timeout(self._page_load_timeout)
        driver.get(self._url)
        driver.implicitly_wait(self._implicitly_wait)
        if not self._headless:
            driver.maximize_window()

        print(f"Started a new session: {driver.session_id}")
        return driver

    @property
    def get_network_performance(self):
        """return the log entry"""
        return self.__driver.get_log('performance')

    def get_url(self, url):
        """Loads a web page in the current browser session.
        :Args:
       - url - needs end point url for start session"""
        try:
            self.__driver.get(url)
        except Exception as e:
            print(f'Failed to get url : {url}, reason : {e}')

    def get_data_from_url(self, url):
        """this function return the html body from specific url."""
        self.get_url(url)
        return self.__get_body()

    def __get_body(self):
        """this function return the html body."""
        try:
            return self.__driver.find_element_by_tag_name("body").text
        except Exception as e:
            print(f"get body method exception:\n{e}")
            return

    def tear_down(self):
        """close the driver session."""
        self.__driver.close()
        print("driver close")


class SeleniumActions:
    """
    This module wrapping basic web actions
    """

    def __init__(self, driver):
        self._list_of_elements = []
        self._web_element_type = "webelement"
        self._temp_element = None
        self._wait_seconds = 0
        self.__driver = driver

    def wait_for_text(self, location=None, text=None):
        try:
            if location:
                WebDriverWait(self.__driver, 10).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, location), text))
                print(f"Succes to find text: {text} in element: {location}")
            else:
                text = self.find_element_by_xpath(f"//*[text()='{text}']").text
                print(f"Succes to find text: {text}")
            return True
        except Exception:
            assert False, print(f"Failed to find text: {text}")

    def get_list_of_elements_by_type(self, element_type, element):
        """
        - args -
              element_type: 1 = id, 2 - xpath, 3 - name, 4 - css, 5 - link text"""
        try:
            if element_type == 1:
                self._list_of_elements = self.__driver.find_elements(By.ID, element)
            elif element_type == 2:
                self._list_of_elements = self.__driver.find_elements(By.XPATH, element)
            elif element_type == 3:
                self._list_of_elements = self.__driver.find_elements(By.NAME, element)
            elif element_type == 4:
                self._list_of_elements = self.__driver.find_elements(By.CSS_SELECTOR, element)
            elif element_type == 5:
                self._list_of_elements = self.__driver.find_elements(By.LINK_TEXT, element)

            return self._list_of_elements

        except Exception as e:
            print(f"Failed to find list of elements: {e}")
        return

    def click(self, element, wait=0):
        sleep(wait)
        self._temp_element = self.check_all_options(element)
        try:
            if self._temp_element is not None:
                self._temp_element.click()
                print(f"success to click on element: {element}")
                return True
        except Exception as e:
            assert False, print(f"Failed to click on element: {e}")

    def hover(self, element, wait=0):
        sleep(wait)
        self._temp_element = self.check_all_options(element)
        try:
            if self._temp_element is not None:
                hover = ActionChains(self.__driver).move_to_element(self._temp_element)
                hover.perform()
                print(f"success to hover on: {element}")
                return True
        except Exception as e:
            assert False, print(f"Failed to hover on element ,reason: {e}")

    def send_keys(self, element=None, text=None, wait=0):
        text = str(text)
        sleep(wait)
        if not element:
            ActionChains(self.__driver).send_keys(text).perform()
            print(f"Succeed to send text to screen")
            return True
        self._temp_element = self.check_all_options(element)
        try:
            if self._temp_element is not None:
                self._temp_element.send_keys(text)
                print(f"Succeed to send text to element: {element}")
                return True
        except Exception as e:
            assert False, print(f"Failed to send text to element: {e}")

    def get_text(self, element, wait=0, fail=True):
        sleep(wait)
        self._temp_element = element
        if self._web_element_type not in str(type(self._temp_element)):
            self._temp_element = self.check_all_options(element)
        try:
            if self._temp_element is not None:
                return self._temp_element.text
        except Exception as e:
            print(f"Failed to get text to element: {element}\nException:\n{e}")
            if fail:
                assert False

    def check_all_options(self, element):
        # check id option
        self._temp_element = self.find_element_by_id(element)
        if self._temp_element is not None:
            return self._temp_element

        self._temp_element = self.find_element_by_xpath(element)
        if self._temp_element is not None:
            return self._temp_element

        # check name option
        self._temp_element = self.find_element_by_css(element)
        if self._temp_element is not None:
            return self._temp_element

        # check name option
        self._temp_element = self.find_element_by_link_text(element)
        if self._temp_element is not None:
            return self._temp_element

        # check name option
        self._temp_element = self.find_element_by_name(element)
        if self._temp_element is not None:
            return self._temp_element

        return

    def find_element_by_id(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_id(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def find_element_by_class_name(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_class_name(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def find_element_by_xpath(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_xpath(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def find_element_by_name(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_name(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def find_element_by_css(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_css(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def find_element_by_link_text(self, element):
        try:
            self._temp_element = self.__driver.find_element_by_link_text(element)
            print(f"Found element: {element}")
            return self._temp_element
        except Exception:
            print(f"Failed to find element: {element}")
        return None

    def get_page_source(self):
        try:
            source = self.__driver.page_source
            return source
        except Exception:
            return False

    def get_body(self):
        try:
            return self.__driver.find_element_by_tag_name("body").text
        except Exception:
            return False

    def get_href(self, element):
        try:
            if element is not None:
                self._temp_element = element.get_attribute("href")
                return self._temp_element

        except Exception:
            print(f"Failed to find element: {element}")
        return False
