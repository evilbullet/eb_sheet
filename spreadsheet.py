import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

summary_header = ['feature','test', 'author', 'comments']
summary = summary_header
cells_count = len(summary_header)

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

for feature_name, gd_key in g_docs.items():
    sheet_lines = client.open_by_key(gd_key).worksheet('Automation progress').get_all_values()
    stat_lines = sheet_lines
    for list in stat_lines:
        list.extend([feature_name])
    summary_list = summary_list + stat_lines

print('total lines in doc: ', len(summary_list))

final_array = []
for list in summary_list:
    if list[2] == 'Finished' and today_check(list[6]):
        single_list = [list[9]] + [list[3]] + [list[4]] + [list[8]]
        final_array.append(single_list)

print(len(final_array), final_array)
rows_count = len(final_array)

cell_list = summary_sheet.range(1,1, cells_count, rows_count)
# worksheet.range(1, 1, 7, 2) a1:b7

# a = ['1','2','3','4']
# for cell, aa in zip(cell_list, a):
#     cell.value = aa

# summary_sheet.insert_row(a)
sum_st = []
for list in final_array:
    for st in list:
        sum_st.append(st)

print(len(sum_st), sum_st)

for cell, st in zip(cell_list, sum_st):
    cell.value = st

summary_sheet.update_cells(cell_list)

# print(len(summary))

