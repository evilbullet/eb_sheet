import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# test doc --->
# https://docs.google.com/spreadsheets/d/1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA/edit#gid=716963912

summary_header = ['feature','test', 'author', 'comments', 'date']
cols_count = len(summary_header)

def today_check(date):
    DATE_RANGE_START = datetime(day=1, month=1, year=2016)
    DATE_RANGE_END = datetime(day=27, month=1, year=2099)
    DATE_TEST_FINISH = datetime.strptime(date, "%d/%m/%Y")
    today_check = DATE_RANGE_START <= DATE_TEST_FINISH <= DATE_RANGE_END

    return today_check

def insert_week_headers(test_date):
    test_date = datetime.strptime(test_date, '%d/%m/%Y')

    week_number = test_date.strftime("%W %Y")
    date_obj = datetime.strptime\
        (test_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    arr = (['Week - ' + week_number,
                        'Week start - end: ' + start_of_week.strftime('%Y/%m/%d') +
                        ' - ' + end_of_week.strftime('%Y/%m/%d'), '', '' , ''])
    return arr

def make_datetime(lst):
    if lst[6] == '' or lst[6] == 'Started On':
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

g_docs =    {# 'tset 1': '1MvLGkcfl5msJEb8DwQXjYaq8HVTi6cJk_JbzIKQAjrA',
            'Feature 0': '1kViBTBc90DPMnWHZ_WZghcalHcJmkASnA975zmmLPsM',
            # 'Feature 2': '1Ht9LsUvqLiwy1IV-bgM9A7F2dnYschja8XX3EnKTMJE',
            # 'Feature 3': '1kViBTBc90DPMnWHZ_WZghcalHcJmkASnA975zmmLPsM',
            # 'Feature 4': '1A9TzAkFXSoT_CAQe6twAn2wYL_1nDTiNyjhh8faZ4r8',
            # 'Feature 5': '10BMNqsqAkRLZwXZRdxKXVVWBnjG_i2_HZxrSpTtn5x0',
            # 'Feature 6': '1RwtIusKuKtJJBnjFKt_zbSmpB2XPtNhF1SdZU7pyQxU',
            # 'Feature 7': '1FVuedc19h17SSWpO4tHZaekBnqnu8Lr-IynZ1YLyXgI',
            # 'Feature 8': '1sABAOwlE4QpK5MEn6NFLkXqb4Tns3ApFN6l24Y4YF2g',
            # 'Feature 9': '1Uy-g5HQ2RCQFKNH3lbXKljJTvRRXw_ly7XU-1yps6l8',
            # 'Feature 10': '1lO5lnsfbl9htgLXfKwa5rmQeGs6cKbe34W367pm8uns',
            # 'Feature 11': '1ATYskL9uByTr7EP09P77DnTeErS4mz8aNPf3e-dFVT8',
            'Feature 12': '1JXcsUm9OzluzYNsaRSaA_lEz_xhJFH_UNrma6unNIyc'}

summary_sheet = client.open('new_table test').worksheet('calendar - finished')

summary_list = []
stat_line = []
sheet_lines = []

for feature_name, gd_key in g_docs.items():
    sheet_lines = client.open_by_key(gd_key).worksheet('Automation progress').get_all_values()
    print('operating: ', feature_name)
    stat_lines = sheet_lines
    for list in stat_lines:
        list.extend([feature_name])
    summary_list = summary_list + stat_lines
summary_list = sorted(summary_list, key=make_datetime)
print('total lines in doc: ', str(len(summary_list)))

final_array = []
week_header_array = []
for list in summary_list: # [1:] to skip table header
    if list[2] == 'Ready for review' and today_check(list[6]) and list[6] is not ''\
            and list[6] is not 'Started On':
        #  ['feature','test', 'author', 'comments',  # 'date']
        single_list = [list[9]] + [list[3]] + [list[4]] + [list[8]]  + [list[6]]
        if not final_array.count(insert_week_headers(list[6])):
            final_array.append(insert_week_headers(list[6]))

        final_array.append(single_list)

final_array.insert(0, summary_header)

print(len(final_array), type(final_array) )

rows_count = len(final_array)
cell_list = summary_sheet.range(1,1, rows_count, cols_count )

sum_st = []
for list in final_array:
    for st in list:
        sum_st.append(st)

print('update cells:', len(sum_st), sum_st)

for cell, st in zip(cell_list, sum_st):
    cell.value = st
summary_sheet.update_cells(cell_list)
# summary_sheet.insert_row(a)
