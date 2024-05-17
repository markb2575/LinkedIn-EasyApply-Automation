#"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\markb\AppData\Local\Google\Chrome\User Data\Default"
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
import time
import subprocess
import json

env_variables = dotenv_values('.env')
command = "\"" + env_variables['chromelocation'] + '\" --remote-debugging-port=9222 --user-data-dir=\"' + env_variables['userlocation'] + "\"" 

subprocess.Popen(command, shell=True)
print(command)
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
driver = webdriver.Chrome(options=options)

page = 0
jobs = {}

# change end range to search more pages
for page in range(0,5):
    try:
        driver.get(f"https://www.linkedin.com/jobs/collections/recommended/?discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII&start={page*24}")
        time.sleep(2)
        job_results_list = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
        # Scroll to load all elements
        scroll_height = driver.execute_script("return arguments[0].scrollHeight", job_results_list)
        for i in range(0, scroll_height, 800):
            driver.execute_script(f"arguments[0].scrollTop = {i}", job_results_list)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", job_results_list)
        # Get the list of jobs
        job_list = driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
        # Finding all elements that are Easy Apply
        easy_apply_elements = job_list.find_elements(By.XPATH, "//*[@class='job-card-container__apply-method job-card-container__footer-item inline-flex align-items-center']")
        for element in easy_apply_elements:
            parent = element.find_element(By.XPATH, "../../..")
            job_id = parent.get_attribute("data-job-id")
            job_name = parent.find_element(By.XPATH, "div[1]/div[1]/div[2]/div[1]/a").get_attribute("aria-label")
            if jobs.get(job_id) is not None and jobs.get(job_id) == job_name:
                continue
            job_details = {"job_name": job_name, "applied": False}
            jobs[job_id] = job_details
    except Exception as error:
        print(error)
        break
with open("jobs.json", "w") as f: 
    json.dump(jobs, f)
driver.quit()



        






















  
