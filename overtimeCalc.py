#!/usr/bin/env python3
import datetime
import tabulate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("time_to_date", help="Time reported by timecard to date for this month")
parser.add_argument("-t","--time_now", help="Time worked today so far (in hours)")
args = parser.parse_args()

standard_working_day = 8.0
todays_date = datetime.date.today()
month_start = datetime.date(todays_date.year, todays_date.month, 1)

checkDay = month_start
n_wkdays = 0
while checkDay != todays_date:
    if checkDay.isoweekday() not in [6,7]:
        n_wkdays += 1
    checkDay += datetime.timedelta(days=1)

time_expected = n_wkdays*standard_working_day
time_this_month = float(args.time_to_date)


if args.time_now:
    print('If work stops right now: ')
    to_now = time_this_month+float(args.time_now)
    to_COB = time_expected + 8
    overtime = to_now - to_COB
    table_data = [to_now, to_COB, overtime]
else:
    print('As of COB yesterday: ')
    overtime = time_this_month-time_expected
    table_data = [time_this_month, time_expected, overtime]


outtable = tabulate.tabulate([table_data],headers=['Reported Hours', 'Standard Hours', 'Overtime'])
print(outtable)