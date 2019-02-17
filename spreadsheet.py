import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from operator import itemgetter

# test doc --->
# https://docs.google.com/spreadsheets/d/1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA/edit#gid=716963912

summary_header = ['feature','test', 'author', 'comments']
cols_count = len(summary_header)

def today_check(date):
    DATE_RANGE_START = datetime(day=1, month=1, year=2016)
    DATE_RANGE_END = datetime(day=27, month=1, year=2099)
    try:
        DATE_TEST_FINISH = datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        return 0
    today_check = DATE_RANGE_START <= DATE_TEST_FINISH <= DATE_RANGE_END
    return today_check

def insert_week_headers(test_date):
    try:
        test_date = datetime.strptime(test_date, '%d/%m/%Y')
    except:
        return False
    week_number = test_date.strftime("%W %Y")
    date_obj = datetime.strptime\
        (test_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    arr = ['Week - ' + week_number,
            'Week start - end: ' + start_of_week.strftime('%Y/%m/%d') +
            ' - ' + end_of_week.strftime('%Y/%m/%d'), '' , '']
    return ('Week - ' + week_number,['Week - ' + week_number,
            'Week start - end: ' + start_of_week.strftime('%Y/%m/%d') +
            ' - ' + end_of_week.strftime('%Y/%m/%d'), '' , ''])

def make_datetime(lst):
    if lst[6] == '' or lst[6] == 'Started On'or lst[6]=='Finished On':
        date_str = '11/11/2000'
    else:
        date_str = lst[6]
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except:
        # datetime.strptime(date_str, '%m/%d/%Y')
        print(date_str)
        return  datetime.strptime(date_str, '%d/%m/%Y')# IndexError

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

g_docs_finished = {
'feature 1':'1DGdnyxgjKgZ1mN3DFqeFxcOQ9nOp_FQFg-6pR8xbWqs',
'feature 2':'192huiwOlSMtzi-nBftwdCwPvzhZTdhznqbK46g-jKQk',
'feature 3':'1Hnzfjur1rqse7gecHMj9s_VQw8-hct6gl-VqgdQj5XE',
'feature 4':'1PJkKI9zvjBT8etEmrQjqkn9GEBlvUTC--gl-MPX1o64',
'feature 5':'1aq_gcD2vrtIClhhZVteMT62sRHjE_UXX95Hl6LnQSz8',
'feature 6':'1XDCESv6trwAgoul1X3IE7l-fCh3dc43eFrcX3Qfo1_g'
}
g_docs =    {
    # 'tset 1': '1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA',
'feature 1':'1cvQpiRr4sWqD_dOmnPvGsRVeVHC_GCylJq_bBzvVlk0',
# 'feature 2':'1kViBTBc90DPMnWHZ_WZghcalHcJmkASnA975zmmLPsM',
# 'feature 3':'1A9TzAkFXSoT_CAQe6twAn2wYL_1nDTiNyjhh8faZ4r8',
# 'feature 4':'10BMNqsqAkRLZwXZRdxKXVVWBnjG_i2_HZxrSpTtn5x0',
# 'feature 5':'1RwtIusKuKtJJBnjFKt_zbSmpB2XPtNhF1SdZU7pyQxU',
# 'feature 6':'1FVuedc19h17SSWpO4tHZaekBnqnu8Lr-IynZ1YLyXgI',
# 'feature 7':'1sABAOwlE4QpK5MEn6NFLkXqb4Tns3ApFN6l24Y4YF2g',
# 'feature 8':'1Uy-g5HQ2RCQFKNH3lbXKljJTvRRXw_ly7XU-1yps6l8',
# 'feature 9':'1lO5lnsfbl9htgLXfKwa5rmQeGs6cKbe34W367pm8uns',
# 'feature 10':'1ATYskL9uByTr7EP09P77DnTeErS4mz8aNPf3e-dFVT8',
# 'feature 11':'1JXcsUm9OzluzYNsaRSaA_lEz_xhJFH_UNrma6unNIyc',
'feature 12':'1esuRzV-u6bjDf2dF7E0J_PFdvvirBhkcvsskyIbr-iM'
            }

summary_sheet = client.open('new_summary test').worksheet('all_new')

def collect_all_docs():
    summary_list = []
    stat_line = []
    sheet_lines = []

    for feature_name, gd_key in g_docs.items():
        sheet_lines = client.open_by_key(gd_key).worksheet('Automation progress').get_all_values()
        print('operating: ', feature_name, client.open_by_key(gd_key).title)
        stat_lines = sheet_lines
        for list in stat_lines:
            list.extend([feature_name])
        summary_list = summary_list + stat_lines
    summary_list = sorted(summary_list, key=make_datetime)
    print('total lines in doc: ', str(len(summary_list)))

worksheet = client.open_by_key(
    '1cvQpiRr4sWqD_dOmnPvGsRVeVHC_GCylJq_bBzvVlk0').worksheet(
    'Automation progress')
all_rows = worksheet.get_all_records()

performances = []
processed_rows = []
keys = ['Title', 'Assignee', 'PR', 'Finished On' ]
header = ['Title', 'Assignee', 'PR', 'Finished On']
for idx, row in enumerate(all_rows):
    if row['Status'] is not '' :
        keys = ('Title', 'Assignee', 'PR', 'Finished On' )
        # Create new Dict with only keys from list (Drop extra)
        new_row = {key: row[key] for key in keys}
        performances.append(new_row)

data = sorted(performances, key=itemgetter('Finished On'))

def add_weeks(data):
    out = []
    x = 'Week - 05 2019'
    x1 = ['Week - 05 2019']
    for idx, row in enumerate(data):
        if row['Finished On'] is not '':
            keys = ('Title', 'Assignee', 'PR', 'Finished On')
            # Create new Dict with only keys from list (Drop extra)
            new_row = {key: row[key] for key in keys}
            # if not out.count(insert_week_headers(new_row.get('Finished On'))[0]):
            if not out.count(insert_week_headers(new_row.get('Finished On'))[0]):
                out.extend(insert_week_headers(new_row.get('Finished On'))[1])
            # print(insert_week_headers(new_row.get('Finished On'))[0])
            # print(out.count(x))
            # print(out.count(x1))
            # print(insert_week_headers(new_row.get('Finished On'))[0])
            for key in new_row:
                out.append(new_row[key])
            # out.append(new_row)
            # TODO: avg time
            # TODO: longest test
            # TODO: shortest test
            # TODO: test per autor
            # TODO:
    return out

header = dict(zip(keys, header))

print(performances)
data = add_weeks(data)
print(data)

def output_to_spreadsheet(final_array):
    sum_st = final_array

    cols_count = len(summary_header)
    rows_count = len(sum_st) / len(summary_header)
    cell_list = summary_sheet.range(1,1, rows_count, cols_count )

    print('update cells:', len(sum_st), sum_st)

    for cell, st in zip(cell_list, sum_st):
        cell.value = st
    summary_sheet.update_cells(cell_list)
    # summary_sheet.insert_row(a)

output_to_spreadsheet(data)

# print(header)
# print(data[5].get('Title'))
# for x in data:
#     print(x)

# for dic in data:
#     print((dic.get('Title')))
