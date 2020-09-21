#!/usr/bin/env python3

# import texttable
import datetime
import tabulate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("start_time", help="Daily start time in 24 hour time")
parser.add_argument("-b","--breaks", help="Total break time in minutes")
parser.add_argument("-t","--target", help="Target hours for the day")

args = parser.parse_args()

# Check minutes are between 0 and 59. If not, throw error
mins = int(args.start_time[-2:])
if mins // 60 > 0:
    raise ValueError("Minutes must be between 0 and 59")

# Check hours are between 0 and 23. If not, throw error
hrs = int(args.start_time[0:-2])
if hrs // 24 > 0:
    raise ValueError("Hours must be between 0 and 23")

# Set the days start time from user input
day_start = datetime.datetime.today().replace(hour = hrs, minute = mins, second = 0,
    microsecond=0)

# Set amount of time spent on breaks
if args.breaks:
    coffee_breaks = datetime.timedelta(minutes=int(args.breaks))
else:
    coffee_breaks = datetime.timedelta(minutes=0)

# Determine when the user wants to quit for the day, if specified
if args.target:
    target = int(args.target)
    if target > 24:
        raise ValueError("You cannot work more than 24 hours in a day")
    day_end = day_start+datetime.timedelta(hours=int(args.target))+coffee_breaks

# Get the current time
current_time = datetime.datetime.now().replace(second=0, microsecond=0)

# Calculate how much time has been spent working
time_worked = round(((current_time - day_start)-coffee_breaks).seconds/3600,1)
# outtable = texttable.Texttable()

# Format table based on targeted stop time or simply adding up current work time
if args.target:
    outtable = tabulate.tabulate([[day_start.time(), current_time.time(), day_end.time(), time_worked]],headers=['Start Time', 'Current Time', 'Quitting Time', 'Hours Worked'])
else:
    outtable = tabulate.tabulate([[day_start.time(), current_time.time(), time_worked]],headers=['Start Time', 'Current Time', 'Hours Worked'])

print(outtable)