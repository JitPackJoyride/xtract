import parameters

import csv
import time
# import web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def append_to_csv(items, file):
    with open(file, 'a', newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)

def save_to_csv(items, file):
    with open(file, "w+", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        for item in items:
            writer.writerow(item)

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(10)

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_css_selector('.input:nth-child(1) .input__field--with-label')

# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)

time.sleep(1)

# locate password form by_class_name
password = driver.find_element_by_css_selector('.input+ .input .input__field--with-label')

# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)

time.sleep(1)

# locate submit button by_class_name
log_in_button = driver.find_element_by_css_selector('.sign-in-form__submit-btn')

# .click() to mimic button click
log_in_button.click()



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import parameters
from lxml import html

data = [['Name', 'URL', 'Industry', 'Description']]
save_to_csv(data, parameters.file_name)

for query in parameters.search_query:
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.google.com')

    # locate search form by_name
    search_query = driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')

    # send_keys() to simulate the search text key strokes
    search_query.send_keys(query)

    time.sleep(0.5)

    # .send_keys() to simulate the return key
    search_query.send_keys(Keys.RETURN)
    time.sleep(2)



    all_linkedin_urls = []

    for i in range(5):
        if i != 0:
            driver.get(next_page)
        linkedin_urls = driver.find_elements_by_xpath('//div[@class="g"]//div[@class="r"]/a')
        linkedin_urls = [url.get_attribute("href") for url in linkedin_urls]
        time.sleep(0.5)

        for url in linkedin_urls:
            all_linkedin_urls.append(url)

        tree = html.fromstring(driver.page_source)
        
        if tree.xpath('//div[@role="navigation"]//a[@class="pn"]'):
            next_page = driver.find_elements_by_xpath('//div[@role="navigation"]//a[@class="pn"]')
            next_page = [page.get_attribute("href") for page in next_page]
            next_page = next_page[-1]
        else:
            break

    for url in all_linkedin_urls:
        print(url)
    #driver.quit()
    time.sleep(0.5)



    new_data = []
    for i in range(len(all_linkedin_urls)):
        datum = []
        driver.get(all_linkedin_urls[i] + "/about/")
        time.sleep(1)
    
        tree = html.fromstring(driver.page_source)

        if tree.xpath('//h1[@class="org-top-card-summary__title t-24 t-black truncate"]'):
            Name = driver.find_element_by_xpath('//h1[@class="org-top-card-summary__title t-24 t-black truncate"]').get_attribute("title")
        else:
            Name = "N/A"
        datum.append(Name)

        if tree.xpath('//dd[@class="org-page-details__definition-text t-14 t-black--light t-normal"]/a'):
            URL = driver.find_element_by_xpath('//dd[@class="org-page-details__definition-text t-14 t-black--light t-normal"]/a').get_attribute("href")
        elif tree.xpath('//div[@class="org-top-card-primary-actions__inner"]/a'):
            URL = driver.find_element_by_xpath('//div[@class="org-top-card-primary-actions__inner"]/a').get_attribute("href")
        else:
            URL = "N/A"
        datum.append(URL)
    
        if tree.xpath('//div[@class="org-top-card-summary__info-item org-top-card-summary__industry"]'):
            Industry = driver.find_element_by_xpath('//div[@class="org-top-card-summary__info-item org-top-card-summary__industry"]').text
        else:
            Industry = "N/A"
        datum.append(Industry)

        if tree.xpath('//p[@class="break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal"]'):
            Description = driver.find_element_by_xpath('//p[@class="break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal"]').text
        else:
            Description = "N/A"
        datum.append(Description)
    
        new_data.append(datum)

    append_to_csv(new_data, parameters.file_name)



driver.quit()
