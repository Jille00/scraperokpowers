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
	for page in tqdm(range(1,2)):
		again = True

		while again == True:
			try:
				url = "https://api.rokinf.com/api/player_kills?kingdom[]="+kingdom+"&pageNo="+str(page)+"&pageSize=15"
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
scope = ['https://spreadsheets.google.com/feeds',
	 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('jsonFileFromGoogle.json', scope)
gc = gspread.authorize(credentials)

#Add a sheet in google and get the url key form it, make sure you share it with your service account first!
spreadsheet_key = 'yourkey'
#Change to the worksheet name
wks_name = 'Kills'
d2g.upload(Totals, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
