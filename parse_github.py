import requests
import re

page = requests.get("https://github.com/mozilla/iris/issues")

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

all_issues = soup.find('div', class_='d-table table-fixed width-full Box-row--drag-hide position-relative')
# relative_time = all_issues.select('relative-time')
# print(all_issues)#
issue_title = all_issues.find('a', id=re.compile('issue_*')).text
print(issue_title)
opened_by_author = all_issues.find('a', class_='muted-link').text

relative_time = all_issues.find('relative-time')
relative_time_date = relative_time['datetime']

issue_link = all_issues.find('a')
issue_link_href  = issue_link['href']
# print(issue_link_href  )[title^="para"]
issue_links = [il.select('[data-hovercard-url]') for il in all_issues.select('a[id^="issue"]')]
print(issue_links)

[item['data-bin'] for item in all_issues.find_all('ul', attrs={'data-bin' : True})]
# issue_number_text = all_issues.find('span')
# print(issue_number)

# short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
# temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
# descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
