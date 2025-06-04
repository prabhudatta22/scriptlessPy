import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def get_locator(locator_str):
    """Parses locator string like 'XPATH://...' or 'ID:...'"""
    if not locator_str:
        return None, None
    if locator_str.startswith("XPATH:"):
        return By.XPATH, locator_str.split("XPATH:")[1]
    elif locator_str.startswith("ID:"):
        return By.ID, locator_str.split("ID:")[1]
    else:
        raise ValueError(f"Unsupported locator: {locator_str}")

def read_test_steps(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    steps = []
    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        testcase = row[0]
        page = row[1]
        step_no = row[2]
        step_name = row[3]
        action_type = row[4]
        element_locator = row[5]
        on_fail = row[6]
        data = row[7]
        if any([testcase, step_no, step_name]):
            steps.append({
                "TestCase": testcase,
                "Page": page,
                "StepNo": step_no,
                "StepName": step_name,
                "ActionType": action_type,
                "Locator": element_locator,
                "OnFail": on_fail,
                "Data": data
            })
    return steps

def execute_test_steps(steps):
    options = Options()
    # options.add_argument("--headless")  # Optional: uncomment for headless
    driver = webdriver.Chrome(options=options)

    results = []
    base_url = None

    for step in steps:
        try:
            action = step["ActionType"]
            locator_type, locator_value = get_locator(step["Locator"])
            data = step["Data"]
            step_desc = f'{step["StepNo"]} - {step["StepName"]}'

            # Navigate to URL
            if action == "navigateToURL":
                base_url = step["Page"]
                driver.get(base_url)
                status = "PASS"

            # Click an element
            elif action == "click":
                driver.find_element(locator_type, locator_value).click()
                status = "PASS"

            # Enter text using JS
            elif action == "jsEnterText":
                element = driver.find_element(locator_type, locator_value)
                driver.execute_script("arguments[0].value = arguments[1];", element, data)
                status = "PASS"

            # Verify text
            elif action == "verifyText":
                element = driver.find_element(locator_type, locator_value)
                if data.strip().lower() in element.text.strip().lower():
                    status = "PASS"
                else:
                    status = f'FAIL - Text "{data}" not found'

            else:
                status = f"SKIPPED - Unknown action: {action}"

        except NoSuchElementException as e:
            status = f"FAIL - Element not found: {str(e)}"
        except Exception as e:
            status = f"FAIL - Exception: {str(e)}"

        print(f'{step_desc}: {status}')
        results.append((step["StepNo"], step["StepName"], action, status))
        time.sleep(1)

    driver.quit()
    return results

def generate_html_report(results, output_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<html><head><title>Test Report</title></head><body>
    <h2>Automated Test Execution Report</h2>
    <p>Generated on: {timestamp}</p>
    <table border='1' cellpadding='5'>
    <tr><th>Step No</th><th>Step Name</th><th>Action</th><th>Status</th></tr>"""
    for step_no, name, action, status in results:
        color = "green" if "PASS" in status else "red" if "FAIL" in status else "orange"
        html += f"<tr><td>{step_no}</td><td>{name}</td><td>{action}</td><td style='color:{color}'>{status}</td></tr>"
    html += "</table></body></html>"

    with open(output_file, "w") as f:
        f.write(html)
    print(f"\nReport saved to: {output_file}")

# === Main ===
if __name__ == "__main__":
    excel_file = "steps.xlsx"       # Your Excel filename
    report_file = "report.html"     # Output HTML report

    print(" Reading test steps...")
    steps = read_test_steps(excel_file)

    print(" Executing test steps...")
    results = execute_test_steps(steps)

    print(" Generating report...")
    generate_html_report(results, report_file)
