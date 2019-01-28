import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import datetime
from operator import itemgetter

# DATE_RANGE_START = datetime.datetime(day=1,month=1,year=2019)
# DATE_RANGE_END = datetime.datetime(day=27,month=1,year=2019)
# DATE_TODAY = datetime.datetime.now()  #  datetime.datetime(day=27,month=1,year=2019)

summary_header = ['feature','test', 'author', 'comments']

def today_check(date):
    DATE_RANGE_START = datetime.datetime(day=1, month=1, year=2019)
    DATE_RANGE_END = datetime.datetime(day=27, month=1, year=2019)
    DATE_TEST_FINISH = datetime.datetime.strptime(date, "%d/%m/%Y")
    today_check = DATE_RANGE_START <= DATE_TEST_FINISH <= DATE_RANGE_END
    return today_check

def unique_autors(seq):
   # order preserving
   autors = []
   for e in seq:
       if e not in autors:
           autors.append(e)
   return autors
#
# def sort_list_by_date(list):
#     # sorted_list = sorted(list, key=itemgetter(6))
#     list.sort(key=lambda x: datetime.datetime.strptime(x.split(None, 1)[-1], '%d/%m/%y'))
#     return list

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
summary = summary_header

#
# g_sh_1 = client.open('new_table test').worksheet('Automation progress')
# g_sh_2 = client.open_by_key('')\
#     .worksheet('Automation progress')

g_docs = {'Feature 1': '1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA',
         'Feature 2': '1Ht9LsUvqLiwy1IV-bgM9A7F2dnYschja8XX3EnKTMJE'}

summary_sheet = client.open('new_table test').worksheet('summary')

# g_doc =  g_sh.get_all_values()
# g_sh_2.get_all_values()

for item in g_docs.items():
    g_sheet_lists = client.open_by_key(item).worksheet('Automation progress').get_all_values()
    # list_of_lists = sort_list_by_date(list_of_lists)
    list_of_autors = [row[4] for row in list_of_lists ]
    u_autors = unique_autors(list_of_autors)


for autor in u_autors:
    for list in list_of_lists:
        if list[4] == autor \
        and list[2] == 'Finished' and today_check(list[6]):
            summary_list = list[3] +
            summary.append(list)
            summary_sheet.insert_row(list)

print(len(summary))

