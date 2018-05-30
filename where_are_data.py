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


__author__ = "Alejandro Loja & Oscar Su"

import json
import base64
import gspread
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
STUDENT_NAME = "Alejandro Loja"
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

# print "After auth"

# *****************************************************************************
# *****************************************************************************
#                               FUNCTIONS
# *****************************************************************************
# *****************************************************************************
# **********************************************
#        CREATE A NEW SPREADSHEET
# - Calls log_spsh()
# **********************************************
def create_spsh(spsh_name):
    #  create new spreadsheet and share it with service account
    sheet_object = file.create(spsh_name)

    #  shares to service and additional accounts
    sheet_object.share(SERVICE_ACCOUNT, perm_type='user', role='writer')
    # sheet_object.share(ADDITIONAL_ACCOUNT, perm_type='user', role='writer')

    #  sets permission of new spreadsheet to publicly writable
    file.insert_permission(
        sheet_object.id,
        None,
        perm_type='anyone',
        role='writer',
        notify=False
    )

    # log the spreadsheet created in a local text file
    # log_spsh(sheet_object, STUDENT_NAME)

    return sheet_object

    #  creates json file with id
    # with open('spshid.json', 'w') as outfile:
    #     json.dump(({"id": shid}, outfile)


# **********************************************
#        DELETE SPREADSHEET
# TODO: Only log if delete successful
# **********************************************
def delete_spsh(s_obj):
    # Delete spreadsheet
    file.del_spreadsheet(s_obj.id)
    # Log the deletion
    log_spsh(s_obj, STUDENT_NAME, True)


# **********************************************
#       FILL SPREADSHEET WITH CSV
# Input: s_obj
# **********************************************

#def csv_to_spsh(s_obj, csv_location terminal_test_mode=False):
def csv_to_spsh(s_obj, terminal_test_mode=False):
     json_string = ""

     if len(sys.argv)==1:
         data = (["Input 1", "data", "more data", "12"], ["Input 2", "data", 15, "16", "=RANDBETWEEN(0,10)"])
     else:
        data = json.loads(base64.b64decode(sys.argv[1]))

     for x in range(0, len(data)):
        json_string += str(data[x]) + "\n"

        var_to_save_to_db = json.dumps(json_string)
	#  READ THE SPSH FROM CSV FILE
#    with open(csv_location, 'rb') as csv_file:
#        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='\"')
#        for row in csv_reader:
#            if terminal_test_mode:
#                print row
#            csv_string += str(row)
#            csv_string += '\n'

    #with open('test_list.json') as data1:

	#bring in data from db.
	#data1 = json.parse(data)

    #data1= (["Input 1", "data", "more data", "12"], ["Input 2", "data", 15, "16", "=RANDBETWEEN(0,10)"])
    #if len(sys.argv)== 1:
    #    data = (["Input 1", "data", "more data", "12"], ["Input 2", "data", 15, "16", "=RANDBETWEEN(0,10)"])
    #else:
    #    data = json.loads(base64.b64decode(sys.argv[1]))
#Saves each input into json_string

    #for x in range(0, len(data)):
    #    json_string += str(data[x]) + "\n"

    #    var_to_save_to_db = json.dumps(json_string)

#  MODIFY OUTPUT TO MATCH GSPREAD FORMAT
#  replace single quotes with double quotes
        json_string = json_string.replace("\'", "\"")
        #  replace starting brackets
        json_string = json_string.replace("[", "")
        #  replace ending brackets
        json_string = json_string.replace("\"]", "\"")
        #	replace starting curly brackets
        json_string = json_string.replace("{\"","\"")
        #	replace ending curly brackets
        json_string = json_string.replace("\"}", "\"")
        #	replace u's when input json array
        json_string = json_string.replace("u\"","\"")

        if terminal_test_mode:
            print "\ncsv_string:"
            print json_string

        file.import_csv(s_obj.id, json_string)



# **********************************************
#       WRITE SPSH TO XLSX
# NOTE: Can only handle first worksheet
# Sent to XLSX to preserve formatting and functions
# because CSV formatting would lose functions
#
# Input: s_obj is spreadsheet object
# csv_location is the absolute path
# terminal_mode when true enables output values to terminal
# **********************************************
def spsh_to_xlsx(s_obj, export_location, terminal_test_mode=False):
    #  get first worksheet
    wksht_obj = s_obj.sheet1
    #  export to xlsx format via gspread
    export_file = wksht_obj.export(format='xlsx')
    #  write to file
    with open(export_location, 'wb') as f:
        f.write(export_file)
    if terminal_test_mode:
        print f.closed


# **********************************************
#       LOG THE SPREADSHEET DATA
# TODO: Add calling page parameter
# TODO: Add CSV file name parameter
# TODO: Add access URL composed with ID
# **********************************************
def log_spsh(s_obj, unique_id, deletion=False):
    #  object of type time
    now_obj = datetime.today()

    #  open the log in append mode
    with open("spsh_log.txt", "a") as text_file:
        if deletion:
            text_file.write("\n\n" + "DELETED")
        else:
            text_file.write("\n\n" + "CREATED")

        #  write the id to the text file
        text_file.write("\n" + unique_id)
        #  write the current time to the text file
        text_file.write("\n" + now_obj.strftime('%c'))
        #  write the unique_id to the text file (sugg: student name)
        text_file.write("\n" + s_obj.id)
        #  write a url for the spreadsheet using the unique_id
        text_file.write("\n" + URL_PREFIX +
                        s_obj.id)


# SHOULD I KEEP?
# **********************************************
#        PRINT TO COMMAND LINE
# TODO: Dynamic spreadsheet range
# **********************************************
def print_spsh(s_obj):
    sheet = s_obj.sheet1
    print_range = sheet.range(1, 1, 11, 3)
    for cell in print_range:
        print cell.value


# **********************************************
#        SEND SPREADSHEET DATA THROUGH JSON
# TODO: Improve amount of data sent
#       - Name of spsh, id of spsh, URL path of spsh,
# TODO: Ability to dynamically send names of all worksheets
# **********************************************
def send_to_ml_verbose(s_obj_1, s_obj_2, s_obj_3, s_obj_4):
    spsh_to_js = {"id_1": s_obj_1.id,
                  "spsh_name_1": s_obj_1.title,
                  "url_1": URL_PREFIX + s_obj_1.id,
                  "first_wksht_1": s_obj_1.get_worksheet(0).title,
                  s_obj_1.get_worksheet(0).title: s_obj_1.get_worksheet(0).id
                  }
    print json.dumps(spsh_to_js)


# **********************************************
#        SEND SPREADSHEET DATA THROUGH JSON
# TODO: Improve amount of data sent
#       - Name of spsh, id of spsh, URL path of spsh,
# TODO: Ability to dynamically send names of all worksheets
# **********************************************
def send_url_to_ml(s_obj_1, s_obj_2, s_obj_3, s_obj_4):
    spsh_to_js = {"url_1": URL_PREFIX + s_obj_1.id,
                  "url_2": URL_PREFIX + s_obj_2.id,
                  "url_3": URL_PREFIX + s_obj_3.id,
                  "url_4": URL_PREFIX + s_obj_4.id,
                  }
    print json.dumps(spsh_to_js)


# *****************************************************************************
# *****************************************************************************
#                               EXECUTION
# *****************************************************************************
# *****************************************************************************
# create a spreadsheet and assign its object to variable
# print "How about here"
spsh_obj_1 = create_spsh(SPREADSHEET_NAME_1)
# spsh_obj_2 = create_spsh(SPREADSHEET_NAME_2)
# spsh_obj_3 = create_spsh(SPREADSHEET_NAME_3)
# spsh_obj_4 = create_spsh(SPREADSHEET_NAME_4)

# fill new spreadsheet with contents of a csv

csv_to_spsh(spsh_obj_1)
# csv_to_spsh(spsh_obj_1, CSV_TO_IMPORT_1)
# csv_to_spsh(spsh_obj_2, CSV_TO_IMPORT_2)
# csv_to_spsh(spsh_obj_3, CSV_TO_IMPORT_3)
# csv_to_spsh(spsh_obj_4, CSV_TO_IMPORT_4)

# create json object and dump
# send_url_to_ml(spsh_obj_1, spsh_obj_2, spsh_obj_3, spsh_obj_4)

spread1 = URL_PREFIX + spsh_obj_1.id
#print spread1

varis = dict()
varis['full_url']=spread1
varis['id']=spsh_obj_1.id
print json.dumps(varis)

#file.open_by_key(sys.argv[1])
#varis['A1'] = file.getCell('A1')

# print str(spsh_obj.get_worksheet(0))

# delete_spsh(spsh_obj)

# print the spreadsheet to the command line in a small range
# print_spsh(spsh_obj)

# delete the spreadsheet
# delete_spsh(spsh_obj)
