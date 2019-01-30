
def number_of_week():
    today = datetime.today()
    week_number = today.strftime("%W %Y")

    date_obj = datetime.strptime\
        (datetime.today().strftime('%d/%m/%Y'), '%d/%m/%Y')

    start_of_week = date_obj - timedelta(days=date_obj.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    return [week_number, start_of_week, end_of_week]

def add_week_header(arr):
    arr.append(['Week - ' + number_of_week()[0],
                        'Week start - end: ' + number_of_week()[1].strftime('%Y/%m/%d') +
                        ' - ' + number_of_week()[2].strftime('%Y/%m/%d'), '', '' , ''])
    return arr


def unique_autors(summary_lists):
    # order preserving
    all_autors = [row[4] for row in summary_lists]
    authors = []
    for e in all_autors:
        if e not in authors and e is not '':
            authors.append(e)
    return authors