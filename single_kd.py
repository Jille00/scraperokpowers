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
kingdom = '1623'
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

Totals.to_excel(f'{str(kingdom)}.xlsx')

