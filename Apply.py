from selenium import webdriver
from dotenv import dotenv_values
import selenium.common
import selenium.webdriver
import selenium.webdriver.common
from selenium.webdriver.common.by import By
import time
import subprocess
import json
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def jobLoop():
    while True:
        start = time.time()
        time.sleep(1)
        try:
            currentPage = []
            # specialInputs = driver.find_elements(By.XPATH, "//*['data-test-single-typeahead-entity-form-component']")
            # for specialInput in specialInputs:
            #     print("here")
            inputs = driver.find_elements(By.XPATH, "//*[@class='artdeco-text-input--container ember-view']")
            for input in inputs:
                required = True if driver.execute_script("return window.getComputedStyle(arguments[0], '::after').getPropertyValue('content');", input.find_element(By.XPATH, "label")) == '"*"' else False
                label = input.find_element(By.XPATH, "label").text
                value = input.find_element(By.XPATH, "input").get_attribute("value")
                currentPage.append({'type':'input', 'label': label, 'value': value, 'required': required, 'element': input})
            dropdowns = driver.find_elements(By.XPATH, "//*[@data-test-text-entity-list-form-component]")
            for dropdown in dropdowns:
                required = True if driver.execute_script("return window.getComputedStyle(arguments[0], '::after').getPropertyValue('content');", dropdown.find_element(By.XPATH, "label")) == '"*"' else False
                select = Select(dropdown.find_element(By.XPATH, "select"))
                label = dropdown.find_element(By.XPATH, "label/span").text
                selectedValue = select.first_selected_option.text
                allValues = select.options
                currentPage.append({'type':'dropdown', 'label': label, 'selectedValue': selectedValue, 'allValues': allValues, 'required': required, 'element': dropdown})
            radios = driver.find_elements(By.TAG_NAME, "fieldset")
            for radio in radios:
                required = True if driver.execute_script("return window.getComputedStyle(arguments[0], '::after').getPropertyValue('content');", radio.find_element(By.XPATH, "//*[@data-test-form-builder-radio-button-form-component__title]")) == '"*"' else False
                selectedValues = []
                allValues = []
                label = radio.find_element(By.XPATH, ".//*[@data-test-form-builder-radio-button-form-component__title]/span[1]").text
                options = radio.find_elements(By.XPATH, ".//*[@data-test-text-selectable-option__label]")
                for option in options:
                    option_text = option.get_attribute("data-test-text-selectable-option__label")
                    allValues.append(option_text)
                    color = driver.execute_script("return window.getComputedStyle(arguments[0], '::before').getPropertyValue('background-color');", option)
                    if color == 'rgb(1, 117, 79)':
                        selectedValues.append(option_text)
                currentPage.append({'type':'radio', 'label': label, 'selectedValues': selectedValues, 'allValues': allValues, 'required': required, 'element': radio})
            multiline_inputs = driver.find_elements(By.XPATH, "//*[@class='fb-multiline-text  artdeco-text-input--input artdeco-text-input__textarea artdeco-text-input__textarea--align-top']")
            for multiline_input in multiline_inputs:
                required = True if driver.execute_script("return window.getComputedStyle(arguments[0], '::after').getPropertyValue('content');", multiline_input.parent.find_element(By.TAG_NAME, "label")) == '"*"' else False
                label = multiline_input.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "label").text
                value = multiline_input.get_attribute("value")
                currentPage.append({'type':'multiline_input', 'label':label, 'value':value, 'required':required, 'element':multiline_input})            
            for item in currentPage:
                if time.time() > start + 10: return                
                with open("prompts.json", "r") as f:
                    prompts = json.load(f)                                
                if (item['type'] == 'input'):                                        
                    stored = prompts.get(item['label'])                    
                    if stored == None and item['value'] == "":                        
                        if item['required'] == False : continue                                              
                        print("stuck")
                        with open("jobs.json", "w") as f:
                            jobs[job]['applied'] = True
                            json.dump(jobs, f)
                        return
                    elif stored != None and item['value'] == "":                                                                        
                        driver.execute_script("arguments[0].scrollIntoView(true);", item['element']);
                        item['element'].find_element(By.XPATH, "input").send_keys(stored)
                    elif stored == None and item['value'] != "":                                              
                        prompts[item['label']] = item['value']
                elif (item['type'] == 'dropdown'):                                        
                    stored = prompts.get(item['label'])                                        
                    if stored == None and item['selectedValue'] == "Select an option":                       
                        if item['required'] == False : continue               
                        print("stuck")
                        with open("jobs.json", "w") as f:
                            jobs[job]['applied'] = True
                            json.dump(jobs, f)
                        return
                    elif stored != None and item['selectedValue'] == "Select an option":                                                
                        driver.execute_script("arguments[0].scrollIntoView(true);", item['element']);
                        Select(item['element'].find_element(By.XPATH, "select")).select_by_visible_text(stored)
                    elif stored == None and item['selectedValue'] != "Select an option":                                                
                        prompts[item['label']] = item['selectedValue']
                elif (item['type'] == 'radio'):                                        
                    stored = prompts.get(item['label'])
                    if stored == None and not item['selectedValues']:                        
                        if item['required'] == False : continue                                                
                        print("stuck")
                        with open("jobs.json", "w") as f:
                            jobs[job]['applied'] = True
                            json.dump(jobs, f)
                        return
                    elif stored != None and not item['selectedValues']:                                              
                        options = item['element'].find_elements(By.XPATH, ".//*[@data-test-text-selectable-option__label]")
                        driver.execute_script("arguments[0].scrollIntoView(true);", item['element']);
                        for i in stored:
                            for option in options:
                                if option.get_attribute("data-test-text-selectable-option__label") == i:
                                    option.click()
                                    return                    
                    elif stored == None and item['selectedValues']:                                                
                        prompts[item['label']] = item['selectedValues']
                elif (item['type'] == 'multiline_input'):                                        
                    stored = prompts.get(item['label'])
                    if stored == None and item['value'] == "":                       
                        if item['required'] == False : continue                                              
                        print("stuck")
                        with open("jobs.json", "w") as f:
                            jobs[job]['applied'] = True
                            json.dump(jobs, f)
                        return
                    elif stored != None and item['value'] == "":                                                
                        driver.execute_script("arguments[0].scrollIntoView(true);", item['element']);
                        item['element'].send_keys(stored)
                    elif stored == None and item['value'] != "":                                                
                        prompts[item['label']] = item['value']
                with open("prompts.json", "w") as f:
                    prompts = json.dump(prompts, f)
            try:
                next_button = driver.find_element(By.XPATH, "//*[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                next_button.click()
            except:
                print("cant find next button")
                with open("jobs.json", "w") as f:
                    jobs[job]['applied'] = True
                    json.dump(jobs, f)
                return
        except:
            print("could not apply")
            return

jobs = {}
with open("jobs.json", "r") as f:
    jobs = json.load(f)
prompts = {}
with open("prompts.json", "r") as f:
    prompts = json.load(f)

env_variables = dotenv_values('.env')
command = "\"" + env_variables['chromelocation'] + '\" --remote-debugging-port=9222 --user-data-dir=\"' + env_variables['userlocation'] + "\""

subprocess.Popen(command, shell=True)
env_variables = dotenv_values('.env')
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

for job in jobs:
    if jobs[job].get('applied') == True: continue
    driver.get(f"https://www.linkedin.com/jobs/collections/recommended/?currentJobId={job}")
    time.sleep(2)
    try:
        apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button--top-card")
        apply_button.click()
        with open("jobs.json", "w") as f:
            jobs[job]['applied'] = True
            json.dump(jobs, f)
    except:
        with open("jobs.json", "w") as f:
            jobs[job]['applied'] = True
            json.dump(jobs, f)
        continue
    jobLoop()
with open("jobs.json", "w") as f:
    jobs = json.dump(jobs, f)
with open("prompts.json", "w") as f:
    prompts = json.dump(prompts, f)