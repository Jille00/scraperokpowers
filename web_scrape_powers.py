import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np

url = 'https://rokinf.com/rank/player_power'

data = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])

driver = webdriver.Chrome()

driver.get(url)
driver.implicitly_wait(150)
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
	_links = driver.find_elements_by_css_selector('img')
	links = []
	for i in _links[2:]:
		links.append([i.get_attribute("src")])
	con = np.concatenate((np.array(rows), np.array(links)), axis=1)
	Temp = pd.DataFrame(con)
	data = data.append(Temp, ignore_index=True)
	
	nxt = driver.find_element_by_xpath("/html/body/div/section/section/main/div/div[2]/div/div/div/div[2]/div/div/ul/li[contains(@title, 'Next Page')]")
	nxt.click()
	time.sleep(2)
data.columns = ['Rank', 'Power', 'Nickname', 'Level', 'Server', "Avatar"]
data.to_excel('data.xlsx')
