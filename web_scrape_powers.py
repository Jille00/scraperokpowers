import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import gspread
import oauth2client
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
data = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])


kingdoms = [1002, 1027]#, 1030, 1046, 1052, 1059, 1071, 1075, 1093, 1103, 1148, 1157, 1163, 1177, 1185, 1189, 1196, 1210, 1239, 1254, 1278, 1279, 1307, 1331, 1337, 1341, 1377, 1379, 1392, 1411, 1556, 1561]
for kingdom in kingdoms:
	url = 'https://rokinf.com/rank/player_power'


	driver = webdriver.Chrome()
	driver.get(url)
	driver.implicitly_wait(150)

	for i in range(1,9):
		nxt = driver.find_element_by_xpath("/html/body/div/section/section/main/div/div[2]/div/div/div/div[1]/form/div/div[2]/div/div/div/span/div/div/div/ul/li[1]/span")
		nxt.click()
		time.sleep(0.5)
	driver.find_element_by_class_name('ant-select-search__field').send_keys(kingdom)

	nxt = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/ul/li")
	nxt.click()

	nxt = driver.find_element_by_xpath("/html/body/div[1]/section/section/main/div/div[2]/div/div/div/div[1]/form/div/div[3]/span/button")
	nxt.click()

	time.sleep(1.5)

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
data.columns = ['Rank', 'Power', 'Nickname', 'Level', 'server', "avatar"]
scope = ['https://spreadsheets.google.com/feeds',
	 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('jsonFileFromGoogle.json', scope)
gc = gspread.authorize(credentials)

#Add a sheet in google and get the url key form it, make sure you share it with your service account first!
#my sheet url is https://docs.google.com/spreadsheets/d/1Ih04MGx2dhJV2RHxVFU2HNa5D1UkGZJjLj_S6DG4c9k/edit#gid=0
# https://docs.google.com/spreadsheets/d/1DNcDymRBnRSU-Qncg8uE9zdEM3-sorsJTSRrzaKseX8/edit#gid=0
spreadsheet_key = '1nTqwbFuWsV6SRV8nQy8bTcbRaqqf8FuqoWro7ytHCWM'
#Change to the worksheet name
#Todo: Add new worksheets for each day??
wks_name = 'All'
#this will overwrite the existing sheet
d2g.upload(data, spreadsheet_key, wks_name, credentials=credentials, row_names=True)

