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

SumTable = pd.DataFrame(data=[], columns=['TotalPower'])

#List of kingdoms to pull data from
kingdoms = range(1001,1002)
for kingdom in tqdm(kingdoms):
    kingdom = str(kingdom)
    Totals = pd.DataFrame()
    for page in range(1,21):
        again = True

        while again == True:
            try:
                page = str(page)
                url = "https://api.rokinf.com/api/player_power?kingdom[]="+kingdom+"&pageNo="+page+"&pageSize=15"
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

    SumTable.loc[kingdom] = Totals.score.sum()

    
print(SumTable)

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
wks_name = 'Kd1-600'
#this will overwrite the existing sheet
d2g.upload(SumTable, spreadsheet_key, wks_name, credentials=credentials, row_names=True)