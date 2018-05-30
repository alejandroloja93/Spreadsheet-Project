#!/usr/local/bin/python

# TODO: export for multiple worksheets
# TODO: options for title of spreadsheet, maybe first worksheet on import?
# - Worksheet problem: GID seems to be deprecated. Ignore for now.
# TODO: function to receive JSON data including ML user name
# TODO: pass id of spreadsheet to javascript
# Using Ubuntu 14.04
# To customize:
# 1. Change global variables
# 2.


__author__ = "Alejandro Loja & Oscar Su8jiopk"

import json
import base64
import gspread
import pprint
import sys
from datetime import datetime
import csv
from oauth2client.service_account import ServiceAccountCredentials
import urllib3.contrib.pyopenssl

urllib3.contrib.pyopenssl.inject_into_urllib3()

# Globals
SPREADSHEET_NAME_1 = "JSON INPUTS"
#SPREADSHEET_NAME_1 = "Where are the data? Location and Spread"
#SPREADSHEET_NAME_2 = "Where are the data? Mean"
#SPREADSHEET_NAME_3 = "Where are the data? Median"
#SPREADSHEET_NAME_4 = "Where are the data? Mode"
#CSV_TO_IMPORT_1 = "/Users/aloja93/Desktop/GoogleSheets/where_data_location_text.csv"
#"/home/gnakkas/where_data_location_text.csv"
#CSV_TO_IMPORT_2 = "/Users/aloja93/Desktop/GoogleSheets/where_data_mean_text.csv"
#"/home/gnakkas/where_data_mean_text.csv"
#CSV_TO_IMPORT_3 = "/Users/aloja93/Desktop/GoogleSheets/where_data_median_text.csv"
#"/home/gnakkas/where_data_median_text.csv"
#CSV_TO_IMPORT_4 = "/Users/aloja93/Desktop/GoogleSheets/where_data_mode_text.csv"

# XLSX_FOR_EXPORT_1 = "exporttest.xlsx"
# XLSX_FOR_EXPORT_2 = "exporttest.xlsx"
# XLSX_FOR_EXPORT_3 = "exporttest.xlsx"

SERVICE_ACCOUNT = ("toplevelserviceaccount@mlspshtgenerator" +
                   ".iam.gserviceaccount.com")
ADDITIONAL_ACCOUNT = "matematikolinko@gmail.com"
CREDS_JSON = "/Users/aloja93/Desktop/GoogleSheets/credentials.json"
#/home/gnakkas/credentials.json"
STUDENT_NAME = "george_nakkas"
URL_PREFIX = "https://docs.google.com/spreadsheets/d/"


# second api scope is necessary for gspread create()
SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


# **********************************************
#               AUTHENTICATION
# **********************************************
# get email and key from creds
json_key = json.load(open(CREDS_JSON))
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_JSON,
                                                               SCOPE)
# authenticate with Google
file = gspread.authorize(credentials)
if len(sys.argv)==1:
    spreadsheet = file.open_by_key("1VWXi3Z-YyVYEU0WyDpflrtpVIPBMjQMiG3908jwnCik")
else:
    spreadsheet = file.open_by_key(json.loads(base64.b64decode(sys.argv[1])))
#varis['A1'] = file.getCell('A1')

worksheet = spreadsheet.get_worksheet(0)

#print json.dumps(worksheet.get_all_values()
#print worksheet.cell(1,1)
temp = worksheet.get_all_values()
rArr = []
for x in range(0,len(temp)):
    rArr.append(list())
    for y in range(0,len(temp[x])):
        rArr[x].append(temp[x][y])



print json.dumps(rArr)



#Make data, stick values into database, i am going to need two fields, New_Id primary key auto- increment
#
