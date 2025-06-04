from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def init_driver():
    options = Options()
    options.add_argument('--headless')  # Optional: Run in headless mode
    service = Service()  # Adjust path if needed
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_possible_locators(element):
    locators = {}
    try:
        if element.get_attribute("id"):
            locators['id'] = element.get_attribute("id")
        if element.get_attribute("name"):
            locators['name'] = element.get_attribute("name")
        if element.get_attribute("class"):
            locators['class'] = element.get_attribute("class")
        if element.get_attribute("type"):
            locators['type'] = element.get_attribute("type")
        locators['tag'] = element.tag_name
        # Simple CSS path
        if element.get_attribute("class"):
            locators['css'] = f"{element.tag_name}.{element.get_attribute('class').replace(' ', '.')}"
        else:
            locators['css'] = element.tag_name
        # XPath (basic relative XPath based on tag and id or class)
        if element.get_attribute("id"):
            locators['xpath'] = f"//*[@id='{element.get_attribute('id')}']"
        elif element.get_attribute("class"):
            cls = element.get_attribute("class").split()[0]
            locators['xpath'] = f"//{element.tag_name}[contains(@class, '{cls}')]"
        else:
            locators['xpath'] = f"//{element.tag_name}"
    except Exception as e:
        print(f"Error collecting locator: {e}")
    return locators

def collect_dom_elements(url):
    driver = init_driver()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    all_elements = driver.find_elements(By.XPATH, "//*")

    result = []
    for el in all_elements:
        locators = get_possible_locators(el)
        result.append(locators)

    driver.quit()
    return result

# Example usage
if __name__ == "__main__":
    url = "https://example.com"  # Replace with your target URL
    elements_with_locators = collect_dom_elements(url)
    for el in elements_with_locators:
        print(el)
