from datetime import datetime
import csv
import sys

def extract_first_two_columns_as_string(csv_file_path):
    # Initialize an empty list to store the concatenated first two columns
    combined_column_data = []

    # Open the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)

        # Skip the first row (usually the header)
        next(csv_reader, None)  # Advance the reader by one row

        # Iterate through rows in the CSV file
        for row in csv_reader:
            if len(row) < 2:
                # If the row has fewer than 2 columns, concatenate what's available
                combined_column_data.append(','.join(row))
            else:
                # Extract the first two columns, concatenate them with a comma, and add to the list
                combined_column_data.append(','.join(row[:2]))

    return combined_column_data

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

# Example usage
# date_time_str = "04/11/24, 08:30 PM"
# crontab_format = convert_to_crontab(date_time_str)
# print(crontab_format)

# my usage
game_times = extract_first_two_columns_as_string(sys.argv[1])
cron_times = []
for game_time in game_times:
    cron = convert_to_crontab(game_time)
    cron_times.append(cron)

print(cron_times)
