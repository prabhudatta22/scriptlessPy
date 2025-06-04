import os
import time
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict

# Mocked imports for missing dependencies in Java version
# You'll need to implement or translate ElementDetails, GenerateLocator, ExcelAction, ExcelWriter, ReadConfigProperty, etc.
from your_project.models import ElementDetails
from your_project.utils import GenerateLocator, ExcelAction, ExcelWriter, ReadConfigProperty


class GeneratePageObject:
    def __init__(self):
        self.config = ReadConfigProperty()

    def generate_page_object(self):
        print("********Started Generating XPATH*********************")
        urls = set()
        test_suite = ExcelAction().get_test_execution_status("RegressionSuite")
        test_cases = ExcelAction().read_test_case_excel()

        for tc in test_cases.values():
            if tc.test_case_name in test_suite:
                urls.update([u for u in tc.urls if u])

        file_path = os.path.join(os.getcwd(), self.config.get_config_value("TestSuiteName"))

        for url in urls:
            element_details_list = []
            all_locator_map = defaultdict(list)

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            driver.get(url)
            time.sleep(3)

            elements = self.get_all_elements(url)

            for el in elements:
                ed = ElementDetails()
                ed = GenerateLocator().get_locator(el, ed)
                ed.text = el.get_text()
                element_details_list.append(ed)

            all_locator_map[url] = element_details_list

            workbook = load_workbook(file_path)
            sheet = workbook["CapturedObjectProperties"]
            ExcelWriter().prepare_workbook(all_locator_map, sheet)

            try:
                workbook.save(file_path)
                print("File written successfully")
            except Exception as e:
                print(f"Error writing Excel: {e}")

            driver.quit()

        print("********Finished Generating XPATH*********************")

    def get_locator_val(self, ed: ElementDetails) -> str:
        if not ed:
            return ""
        return {
            "ID": ed.id,
            "VALUE": ed.value,
            "TITLE": ed.title,
            "NAME": ed.name,
            "CLASSNAME": ed.class_name,
            "HREF": ed.href,
            "CSS": ed.csspath,
        }.get(ed.locator_type.upper(), "")

    def get_all_elements(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        return body.find_all(True) if body else []

    def generate_xpath(self, el):
        if el.get("id"):
            return el["id"]
        elif el.name.lower() == "html":
            return "/html[1]"
        elif el.name.lower() == "body":
            return "/html[1]/body[1]"
        else:
            parent = el.find_parent()
            if not parent:
                return f"/{el.name.lower()}"
            siblings = parent.find_all(el.name, recursive=False)
            index = siblings.index(el) + 1 if el in siblings else 1
            return f"{self.generate_xpath(parent)}/{el.name.lower()}[{index}]"

# Entry point
if __name__ == "__main__":
    GeneratePageObject().generate_page_object()
