#"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\markb\AppData\Local\Google\Chrome\User Data\Default"
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
import time
import subprocess
import json
import re

env_variables = dotenv_values('.env')
command = "\"" + env_variables['chromelocation'] + '\" --remote-debugging-port=9222 --user-data-dir=\"' + env_variables['userlocation'] + "\"" 

subprocess.Popen(command, shell=True)
print(command)
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
driver = webdriver.Chrome(options=options)

end_page = 5
jobs = {}

# change end range to search more pages
for page in range(0,end_page):
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
        job_list = job_list.find_elements(By.XPATH, "./*")
        for job in job_list:
            job.click()
            time.sleep(1)
            try:
                text = driver.find_element(By.XPATH, "//*[@id='how-you-match-card-container']/section[1]/div/h2").text
            except:
                continue
            if (text.find("you may be a good fit") == -1): continue
            numbers = re.findall(r'\d+', text)
            if (int(numbers[0])/int(numbers[1]) > 0.8):
                id = job.get_attribute("data-occludable-job-id")
                jobs[id] = f"https://www.linkedin.com/jobs/collections/recommended/?currentJobId={id}"     
    except Exception as error:
        print(error)
        break
with open("perfect-jobs.json", "w") as f: 
    json.dump(jobs, f)
driver.quit()
