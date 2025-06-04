import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os

# 1. Read instructions from Excel
def read_steps_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    steps = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[1]:  # assuming 2nd column has the instruction
            steps.append(row[1])
    return steps

# 2. Extract locators and actions using basic NLP-like rules
def parse_instruction(instruction):
    instruction = instruction.lower()
    if "go to" in instruction:
        url = instruction.split("go to")[-1].strip()
        return ("navigate", url, None)
    elif "enter" in instruction and "into the input with id" in instruction:
        value = instruction.split('enter')[1].split('into')[0].strip().strip('"')
        element_id = instruction.split('id')[-1].replace('"', '').strip()
        return ("enter", value, ("id", element_id))
    elif "click" in instruction and "id" in instruction:
        element_id = instruction.split('id')[-1].replace('"', '').strip()
        return ("click", None, ("id", element_id))
    else:
        return ("unknown", instruction, None)

# 3. Run Selenium automation
def execute_steps(step_list):
    driver = webdriver.Chrome()
    results = []

    for i, instruction in enumerate(step_list, 1):
        action, value, locator = parse_instruction(instruction)
        try:
            if action == "navigate":
                driver.get(value)
                results.append((i, instruction, "PASS"))
            elif action == "enter" and locator:
                by, val = locator
                driver.find_element(By.ID, val).send_keys(value)
                results.append((i, instruction, "PASS"))
            elif action == "click" and locator:
                by, val = locator
                driver.find_element(By.ID, val).click()
                results.append((i, instruction, "PASS"))
            else:
                results.append((i, instruction, "SKIPPED - Unknown instruction"))
        except NoSuchElementException as e:
            results.append((i, instruction, f"FAIL - Element not found: {str(e)}"))
        except Exception as e:
            results.append((i, instruction, f"FAIL - {str(e)}"))

        time.sleep(1)

    driver.quit()
    return results

# 4. Generate HTML report
def generate_report(results, report_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<html><head><title>Test Report</title></head><body>
    <h1>Test Execution Report</h1>
    <p>Generated on: {timestamp}</p>
    <table border='1' cellpadding='5'>
    <tr><th>Step #</th><th>Instruction</th><th>Status</th></tr>"""

    for step_no, instruction, status in results:
        color = "green" if "PASS" in status else "red" if "FAIL" in status else "orange"
        html += f"<tr><td>{step_no}</td><td>{instruction}</td><td style='color:{color}'>{status}</td></tr>"

    html += "</table></body></html>"

    with open(report_path, "w") as f:
        f.write(html)

    print(f"Report saved to {report_path}")

# Main execution
if __name__ == "__main__":
    excel_path = "steps.xlsx"
    report_path = "report.html"

    print("Reading Excel...")
    steps = read_steps_from_excel(excel_path)

    print("Executing Selenium steps...")
    results = execute_steps(steps)

    print("Generating report...")
    generate_report(results, report_path)
