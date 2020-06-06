import requests
import json
import pandas as pd
import numpy as np
import gspread 
from datetime import date
from tqdm import tqdm
import gspread
import oauth2client
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
Totals = pd.DataFrame()

#List of kingdoms to pull data from
kingdoms = [1002, 1027, 1030, 1046, 1052, 1059, 1071, 1075, 1093, 1103, 1148, 1157, 1163, 1177, 1185, 1189, 1196, 1210, 1239, 1254, 1278, 1279, 1307, 1331, 1337, 1341, 1377, 1379, 1392, 1411, 1556, 1561]
for kingdom in tqdm(kingdoms):
	kingdom = str(kingdom)
	for page in tqdm(range(1,21)):
		again = True

		while again == True:
			try:
				url = "https://api.rokinf.com/api/player_power?kingdom[]="+kingdom+"&pageNo="+str(page)+"&pageSize=15"
				response = requests.get(url)
				data=response.json()
				json.dumps(data)
				val = data["result"]
				val2 = val["records"]
				Temp = pd.DataFrame(val2)  
				Totals = Totals.append(Temp, ignore_index=True)
				again=False
			except:
				pass
Totals.columns = ['Rank, "Power', 'Nickname', 'Level', 'Server', "Avatar"]
scope = ['https://spreadsheets.google.com/feeds',
	 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('jsonFileFromGoogle.json', scope)
gc = gspread.authorize(credentials)

#Add a sheet in google and get the url key form it, make sure you share it with your service account first!
#my sheet url is https://docs.google.com/spreadsheets/d/1Ih04MGx2dhJV2RHxVFU2HNa5D1UkGZJjLj_S6DG4c9k/edit#gid=0
# https://docs.google.com/spreadsheets/d/1DNcDymRBnRSU-Qncg8uE9zdEM3-sorsJTSRrzaKseX8/edit#gid=0
spreadsheet_key = '1DNcDymRBnRSU-Qncg8uE9zdEM3-sorsJTSRrzaKseX8'
#Change to the worksheet name
#Todo: Add new worksheets for each day??
wks_name = 'All'
#this will overwrite the existing sheet
d2g.upload(Totals, spreadsheet_key, wks_name, credentials=credentials, row_names=True)