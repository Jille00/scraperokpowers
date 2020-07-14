from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter
import numpy as np
import gspread_dataframe as gd

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
	 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonFileFromGoogle.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("ROK data").sheet1

existing = gd.get_as_dataframe(sheet)

kds = []
# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
for i in list_of_hashes:
	kds.append(i['server'])

total_kd_list = np.arange(1000, 1700)

cou = set(kds)
total_set = np.arange(1,10)
missing = set(total_set) - cou
missing = list(missing)[:1]

kingdoms = []
for i in missing:
	kingdoms.append(total_kd_list[i])

print(kingdoms)

existing.to_excel('test.xlsx')

DRIVER_PATH = '/home/jille/Desktop/Scrape/geckodriver'
profile = webdriver.FirefoxProfile()
profile.set_preference('dom.webdriver.enabled', False)

driver = webdriver.Firefox(firefox_profile=profile, executable_path=DRIVER_PATH)

url = 'https://rokinf.com/rank/player_power'
driver.get(url)

wait = WebDriverWait(driver,20)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-pagination-item")))

driver.implicitly_wait(150)
for i in range(1, 8):
    nxt = driver.find_element_by_xpath(
            "/html/body/div/section/section/main/div/div[2]/div/div/div/div[1]/form/div/div[2]/div/div/div/span/div/div/div/ul/li[1]/span")
    nxt.click()
    time.sleep(0.1)

VersionDate = datetime.datetime.now().date()
VersionFile = str(VersionDate).replace("-","")

data = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])

for kingdom in kingdoms:
    kingdom = int(kingdom)
    nxt = driver.find_element_by_xpath(
            "/html/body/div/section/section/main/div/div[2]/div/div/div/div[1]/form/div/div[2]/div/div/div/span/div/div/div/ul/li[1]/span")
    nxt.click()
    driver.find_element_by_class_name('ant-select-search__field').send_keys(kingdom)
    time.sleep(0.5)
    driver.find_element_by_class_name('ant-select-dropdown-menu-item').click()
    time.sleep(0.5)
    x = driver.find_element_by_css_selector('.ant-btn-primary')
    x.click()

    time.sleep(2.5)
 
    for i in range(1):
        _powers = driver.find_element_by_css_selector('table').text
        while len(list(_powers)) == 0:
            _powers = driver.find_element_by_css_selector('table').text
        x = _powers.split('\n')
        x = x[5:]
        Temp = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5]) 
        rows = []
        for index, i in enumerate(x):
            if index % 3 == 0:
                row = []
                #add rank
                row.append(int(i))

                a = x[index+2].split(' ')
                #add power
                row.append(int(a[1]))
                #add nickname
                row.append(x[index+1])
                #add level
                row.append(int(a[0]))
                #add kingdom
                row.append(int(a[2]))
                rows.append(row)

        for i in range(1, 16):
            _link = driver.find_element_by_xpath(f'/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[2]/div/span[1]//*')
            _name = driver.find_element_by_xpath(f'/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[2]/div/span[2]')
            for i in rows:
                if i[2] == _name.text:
                    i.append(_link.get_attribute('src'))

        Temp = pd.DataFrame(rows)
        data = data.append(Temp, ignore_index=True)
        
        nxt = driver.find_element_by_xpath("/html/body/div/section/section/main/div/div[2]/div/div/div/div[2]/div/div/ul/li[contains(@title, 'Next Page')]")
        nxt.click()
        time.sleep(2.5)
        driver.implicitly_wait(150)
        
data.columns = ['Rank', 'Power', 'Nickname', 'Level', 'server', "avatar"]
data = data.drop_duplicates()
# add a check for rank sum = 45150
filename = "good" + f"_" + str(VersionFile) +f".xlsx"
# data.to_excel(filename) 

updated = pd.concat([existing, data], axis=0, join='outer', ignore_index=True, keys=None,
          levels=None, names=None, verify_integrity=False, copy=True, sort=True)

# updated.to_excel(filename)
gd.set_with_dataframe(sheet, updated)