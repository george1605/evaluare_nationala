from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from io import StringIO

driver = webdriver.Firefox()
driver.implicitly_wait(2)
driver.get("https://admitere.tuiasi.ro/licenta/")
group = driver.find_element(by=By.CLASS_NAME, value="form-group")
agree = group.find_elements(by=By.NAME, value="agree")[0]
agree.click()
submit = driver.find_elements(by=By.CLASS_NAME, value="btn-primary")[0]
submit.click()

driver.get("https://admitere.tuiasi.ro/licenta/rezultate_admitere.php?facultate=AC")
link = driver.find_elements(by=By.CLASS_NAME, value="localLink")[7]
link.click()
rows = driver.find_element(by=By.XPATH, value="/html/body/section[2]/div[12]/div[3]/div[1]/div[2]/div[4]/div[1]/span[2]/span/button")
rows.click()
link = driver.find_element(by=By.XPATH, value='/html/body/section[2]/div[12]/div[3]/div[1]/div[2]/div[4]/div[1]/span[2]/span/ul/li[5]/a')
link.click()
table = driver.find_element(by=By.ID, value="admisACCTITable")

html = table.get_attribute("outerHTML")
df = pd.read_html(StringIO(html))[0]
df.to_csv('ac.csv')
time.sleep(2.5)
driver.close()
