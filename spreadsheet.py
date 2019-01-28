import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import datetime

summary_header = ['feature','test', 'author', 'comments']
summary = summary_header

def today_check(date):
    DATE_RANGE_START = datetime.datetime(day=1, month=1, year=2019)
    DATE_RANGE_END = datetime.datetime(day=27, month=1, year=2019)
    DATE_TEST_FINISH = datetime.datetime.strptime(date, "%d/%m/%Y")
    today_check = DATE_RANGE_START <= DATE_TEST_FINISH <= DATE_RANGE_END
    return today_check

def unique_autors(summary_lists):
    # order preserving
    print(summary_lists)
    all_autors = [row[4] for row in summary_lists]
    authors = []
    for e in all_autors:
        if e not in authors and e is not '':
            authors.append(e)
    return authors
#
# def sort_list_by_date(list):
#     # sorted_list = sorted(list, key=itemgetter(6))
#     list.sort(key=lambda x: datetime.datetime.strptime(x.split(None, 1)[-1], '%d/%m/%y'))
#     return list

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

g_docs = {'Feature 1': '1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA',
         'Feature 2': '1Ht9LsUvqLiwy1IV-bgM9A7F2dnYschja8XX3EnKTMJE'}

summary_sheet = client.open('new_table test').worksheet('summary')

summary_list = []
stat_line = []
sheet_lines = []
# unwanted = [0,1,2,4,5]

for feature_name, gd_key in g_docs.items():
    sheet_lines = client.open_by_key(gd_key).worksheet('Automation progress').get_all_values()
    stat_lines = sheet_lines
    for list in stat_lines:
        list.extend([feature_name])
    summary_list = summary_list + stat_lines

print(len(summary_list))
    #     # for delete_index in unwanted:
    #     #     del list[delete_index]
    # summary_list.append(sheet_lines)

# print(summary_list)

print( unique_autors(summary_list))

# print(u_autors)
#
# for autor in u_autors:
#     for line in sheet_lines:
#         if line[4] == autor \
#                 and line[2] == 'Finished' and today_check(line[6]):
#             line.remove(line[0])
#
#
#             # del stat_line[0,1]
#             # stat_line.append(feature_name)
#             # stat_line.append(line[3])
#             # stat_line.append(line[4])
#             # stat_line.append(line[8])
#             # stat_line = line[3] + line[4] + line[8]
#             stat_line.insert(0, feature_name)
#             summary.append(stat_line)

# summary_sheet.insert_row(line)


# print(type(summary_list), summary)
# print(len(summary))

