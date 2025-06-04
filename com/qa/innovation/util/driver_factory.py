import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.ie.options import Options as IEOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

from driver_manager import DriverManager  # Assumes a Python version of DriverManager exists


class DriverFactory:
    @staticmethod
    def create_driver_instance(browser_name: str):
        driver = None
        download_filepath = os.path.join(os.getcwd(), "Download")

        if browser_name.lower() == "firefox":
            profile = FirefoxProfile()
            profile.accept_untrusted_certs = True
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "jpeg")
            profile.set_preference("browser.download.dir", download_filepath)

            options = FirefoxOptions()
            driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(),
                firefox_profile=profile,
                options=options
            )

        elif browser_name.lower() == "chrome":
            chrome_prefs = {
                "profile.password_manager_enabled": False,
                "profile.default_content_settings.popups": 0,
                "download.default_directory": download_filepath,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
                "safebrowsing.enabled": True,
                "download.prompt_for_download": False
            }

            options = ChromeOptions()
            options.add_argument("--incognito")
            options.add_experimental_option("prefs", chrome_prefs)
            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=options
            )

        elif browser_name.lower() == "ie":
            options = IEOptions()
            options.ensure_clean_session = True
            options.enable_persistent_hover = True
            options.ignore_protected_mode_settings = True

            driver = webdriver.Ie(
                executable_path=IEDriverManager().install(),
                options=options
            )

        else:
            raise Exception(f"Unsupported browser: {browser_name}")

        DriverManager.set_driver(driver)
        DriverManager.maximize_browser(driver)
        DriverManager.page_load_timeout(driver)
        DriverManager.set_implicit_wait(driver)

        print(f"Driver created: {driver}")
        return DriverManager.get_driver()

    @staticmethod
    def destroy_driver():
        driver = DriverManager.get_driver()
        if driver:
            driver.quit()
