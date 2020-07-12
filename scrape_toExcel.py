from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
import datetime

DRIVER_PATH = 'C:\\Python\\Python38\\geckodriver.exe'
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

#data = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])

kingdoms = [1002,1030,1046,1052,1059,1075,1093,1103,1126,1148,1157,1166,1177,1185,1189,1196,1210,1239,1254,1279,1307,
           1331,1341,1349,1359,1377,1392,1397,1411,1422,1430,1597,1623,1636,1071,1077,1142,1234,1255,1270,1278,1337,1349,1401,1156]

for kingdom in kingdoms:
    data = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])
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
 
    for i in range(20):
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
        
    data.columns = ['KingdomRank', 'Power', 'Player', 'CityHallLevel', 'Kingdom', "avatar"]
    data.insert(6, 'VersionDate', VersionDate)
    data.insert(7, 'playerID', '')
    data = data.drop_duplicates()
    # add a check for rank sum = 45150
    filename = str(kingdom) + f"_" + str(VersionFile) +f".xlsx"
    data.to_excel(filename) 
