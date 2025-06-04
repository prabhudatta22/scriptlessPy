import threading
from selenium.webdriver.remote.webdriver import WebDriver

class DriverManager:
    _driver = threading.local()

    @staticmethod
    def get_driver() -> WebDriver:
        """Returns the WebDriver instance for the current thread."""
        return getattr(DriverManager._driver, 'instance', None)

    @staticmethod
    def set_driver(driver: WebDriver):
        """Sets the WebDriver instance for the current thread."""
        DriverManager._driver.instance = driver

    @staticmethod
    def maximize_browser(driver: WebDriver):
        """Maximizes the browser window."""
        driver.maximize_window()

    @staticmethod
    def set_implicit_wait(driver: WebDriver, seconds: int = 30):
        """Sets implicit wait time."""
        driver.implicitly_wait(seconds)

    @staticmethod
    def page_load_timeout(driver: WebDriver, seconds: int = 30):
        """Sets the page load timeout."""
        driver.set_page_load_timeout(seconds)
