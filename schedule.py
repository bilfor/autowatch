from datetime import datetime
import csv
import sys
import requests
from bs4 import BeautifulSoup

def extract_date_time_teams(csv_file_path):
    # Initialize an empty list to store the concatenated first two columns
    times = []
    teams = []
    crons = []

    # Open the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)

        # Skip the first row (usually the header)
        next(csv_reader, None)  # Advance the reader by one row

        # Iterate through rows in the CSV file
        for row in csv_reader:
            times.append(','.join(row[:2]))
            teams.append(row[3]) 

    return times, teams

def make_urls(teams):

    teams = lc_space_to_dash(teams)
    teams = decide_home_away(teams)

    urls = ['https://volokit2.com/lives/' + game for game in teams]

    return urls

def make_open_commands(urls, mode):
    if mode == 'fullscreen':
        return ['/home/billy/working/autowatch/selenium_mode.py ' + url + ' >> /home/billy/cronlog.txt 2>&1' for url in urls]

    elif mode == 'no-fullscreen':
        return ['export DISPLAY=:0 && firefox --new-window ' + url for url in urls]

def make_crontimes(times):
    crons = []

    for time in times:
        cron_game = convert_to_crontab(time)
        crons.append(cron_game)

    return crons

def make_cronjobs(crontimes, commands):
    if commands == 'close':
        return [crontime + ' ' + 'pkill -f firefox' for crontime in crontimes]
    else:
        return [crontime + ' ' + command for crontime, command in zip(crontimes, commands)]

def lc_space_to_dash(strings):
    processed_strings = []
    for string in strings:
        processed_string = string.lower().replace(' ', '-')
        processed_strings.append(processed_string)
    return processed_strings

def decide_home_away(strings):
    processed_strings = []
    for string in strings:
        if "at-orioles" in string:
            processed_strings.append(string + "-home")
        elif "orioles-at" in string:
            processed_strings.append(string + "-away")
        else:
            processed_strings.append(string)
    return processed_strings

def convert_to_crontab(date_time_str):
    # Parse the date and time string
    dt = datetime.strptime(date_time_str, "%m/%d/%y,%I:%M %p")
    
    # Extract components
    minute = dt.minute
    hour = dt.hour
    day = dt.day
    month = dt.month
    
    # Day of the week is not specified, so we use "*" to denote every day of the week
    crontab_format = f"{minute} {hour} {day} {month} *"
    
    return crontab_format

def write_list_to_file(file_path, input_list):
    with open(file_path, 'w') as file:
        for item in input_list:
            file.write("%s\n" % item)

def modify_hour(input_list, operation, number):
    if operation not in ('add', 'subtract'):
        raise ValueError("Invalid operation. Choose 'add' or 'subtract'.")

    modified_list = []
    for element in input_list:
        numbers = element.split()
        modified_element = ''
        count = 0
        for number_str in numbers:
            if number_str.isdigit():
                count += 1
                if count == 2:  # Second number encountered
                    if operation == 'add':
                        modified_element += str(int(number_str) + number) + ' '
                    elif operation == 'subtract':
                        modified_element += str(int(number_str) - number) + ' '
                else:
                    modified_element += number_str + ' '
            else:
                modified_element += number_str + ' '
        modified_list.append(modified_element.strip())  # Remove trailing space
    return modified_list

def fix_day_rollover(cron_times):
    adjusted_cron_times = []
    for cron_time in cron_times:
        minute, hour, day, month, _ = cron_time.split()
        hour = int(hour)
        if hour >= 24:
            hour %= 24
            day = str(int(day) + 1)  # Increment day by 1
        adjusted_cron_times.append(f"{minute} {hour} {day} {month} *")
    return adjusted_cron_times

def make_crontab(all_cronjobs):
    display = 'DISPLAY=:0'
    shell = 'SHELL=/bin/bash'
    path = 'PATH=:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin'

    env = [display, shell, path, ' ']

    crontab = env + all_cronjobs
    
    return crontab

times, teams = extract_date_time_teams(sys.argv[1])
urls = make_urls(teams)
#onestream_urls = find_streams_in_urls(volo_urls)
open_commands = make_open_commands(urls, 'fullscreen')
et_start_times = make_crontimes(times)
ct_start_times = modify_hour(et_start_times, 'subtract', 1)
ct_end_times = modify_hour(ct_start_times, 'add', 4)
fixed_ct_end_times = fix_day_rollover(ct_end_times)
open_cronjobs = make_cronjobs(ct_start_times, open_commands)
close_cronjobs = make_cronjobs(fixed_ct_end_times, 'close')
all_cronjobs = [value for pair in zip(open_cronjobs, close_cronjobs) for value in pair]
full_crontab = make_crontab(all_cronjobs)
write_list_to_file(sys.argv[2], full_crontab)

