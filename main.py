from icalendar import Calendar
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('wage', help='時給')
parser.add_argument('--name', default='shift', help='iCSファイル名。拡張子は不要')
parser.add_argument('--other', help='勤務日に固定で入る残業手当・交通費などの雑費')

wage = int(parser.parse_args().wage)

if parser.parse_args().name != None:
    name = parser.parse_args().name
else:
    name = 0

if parser.parse_args().other != None:
    other = int(parser.parse_args().other)
else:
    other = 0

f = open(name+'.ics', 'r', encoding='utf-8')
cal = Calendar.from_ical(f.read())

sum = 0  # total salary
hours = 0
day = 0

for event in cal.walk():
    if event.name == 'VEVENT':
        summary = event['summary'].split(' ')
        st = datetime.strptime(summary[1], '%H:%M')
        ed = datetime.strptime(summary[3], '%H:%M')
        td = ed-st
        hours = hours+int(td.total_seconds()/3600)
        day += 1

print('勤務日：', str(day), '日\t勤務時間：', str(hours), '時間')
print('時給合計', str(hours*wage), '円')
print('その他経費：', str(day*other), '円')
print('給与合計：', str(hours*wage+day*other), '円')
