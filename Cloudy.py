import csv
import uuid
from datetime import date, datetime, timedelta
import pandas as pd


def filter_by_date():
    """Display the Weather information for sepesific date."""

    # Validate the observation date
    while True:
        selected_date = input("Enter the date in (MM-DD-YYYY) format, or press Enter for today date: ")
        if not selected_date.strip():  # Use today's date
            selected_date = date.today().strftime("%m-%d-%Y")
            break
        try:
            datetime.strptime(selected_date, "%m-%d-%Y")
            break
        except ValueError:
            print("The entered date format is invalid. Please use (MM-DD-YYYY) format.")


    # Try to open and filter the CSV file
    try:
        with open('Cloudy.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)

            matches = [row for row in reader if row['date'] == selected_date]

            if matches:
                print(f"Found {len(matches)} record(s) for {selected_date}:")
                for row in matches:
                    print(row)
            else:
                print(f"No data found for {selected_date}")

    except FileNotFoundError:
        print("File 'Cloudy.csv' not found! ;( Please make sure the file exists.")

filter_by_date()




# Function for Temperature Statistics
def display_weather_stats(new_observation):
    temperatures = [i['temperature'] for i in new_observation]
    weather_conditions = [i['weather_condition'] for i in new_observation]


    # Get Maximum, Minimum, Average, and Mode (Most Frequent) in Variables
    mode_weather = pd.Series(weather_conditions).mode()[0]
    highest_degree = max(temperatures)
    lowest_degree = min(temperatures)
    average_degree = round(sum(temperatures) / len(temperatures), 2)

    # Display to the user
    while True:
        choice = input("Choose what to display: Minimum, Maximum, Average, Most Common Weather or Exit: ")
        try:
            if choice.lower() == 'minimum':
                print(f"The lowest degree is {lowest_degree}")
            elif choice.lower() == 'maximum':
                print(f"The highest degree is {highest_degree}")
            elif choice.lower() == 'average':
                print(f"The Average degree is {average_degree}")
            elif choice.lower() == 'most common weather':
                print(f"The most common weather is {mode_weather}")
            elif choice.lower() == 'exit':
                break
            else:
                raise ValueError
        except ValueError:
            print("Please choose Minimum, Maximum, Average, Most Common Weather, or Exit.")


        
    
# Create variable the the data called cloudy
cloudy = Open_csv()


# Make list contains the data within each year 
data_2022 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%d-%m-%Y').year == 2022
]

data_2023 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%d-%m-%Y').year == 2023
]

data_2024 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%d-%m-%Y').year == 2024
]

data_2025 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%d-%m-%Y').year == 2025
]

# Filter the data in the current year, aggregate them together
current_year = datetime.now().year
data_current_year = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%d-%m-%Y').year == current_year
]


# Function contains the statistics (average of temp, humidity, and wind speed) of year 2023
def stats_23(data_2023):
    temperatures_23 = []
    for i in data_2023:
        try:
            temp = float(i['temperature'])
            temperatures_23.append(temp)
        except ValueError:
            continue  # Skip NA
    
    avg_temp_23 = round(sum(temperatures_23) / len(temperatures_23), 2)
    print(f'The average of temperatures in 2023 is {avg_temp_23}')
    
    # Humidity Stats
    humidity_23 = []
    for i in data_2023:
        try:
            hum = float(i['humidity'])
            humidity_23.append(hum)
        except ValueError:
            continue  # Skip NA
    
    avg_humidity_23 = round(sum(humidity_23) / len(humidity_23), 2)
    print(f'The average of humidity in 2023 is {avg_humidity_23}')
    
    # Wind Speed Stats
    wind_speed_23 = []
    for i in data_2023:
        try:
            wind = float(i['wind_speed'])
            wind_speed_23.append(wind)
        except ValueError:
            continue  # Skip NA
    
    avg_wind_23 = round(sum(wind_speed_23) / len(wind_speed_23), 2)
    print(f'The average of wind in 2023 is {avg_wind_23}')


# Function contains the statistics (average of temp, humidity, and wind speed) of year 2024
def stats_24(data_2024):
    temperatures_24 = []
    for i in data_2024:
        try:
            temp = float(i['temperature'])
            temperatures_24.append(temp)
        except ValueError:
            continue  # Skip NA

    avg_temp_24 = round(sum(temperatures_24) / len(temperatures_24), 2)
    print(f'The average of temperatures in 2024 is {avg_temp_24}')

    # Humidity
    humidity_24 = []
    for i in data_2024:
        try:
            hum = float(i['humidity'])
            humidity_24.append(hum)
        except ValueError:
            continue  # Skip NA

    avg_humidity_24 = round(sum(humidity_24) / len(humidity_24), 2)
    print(f'The average of humidity in 2024 is {avg_humidity_24}')

    # Wind Speed
    wind_speed_24 = []
    for i in data_2024:
        try:
            wind = float(i['wind_speed'])
            wind_speed_24.append(wind)
        except ValueError:
            continue  # Skip NA

    avg_wind_24 = round(sum(wind_speed_24) / len(wind_speed_24), 2)
    print(f'The average of wind speed in 2024 is {avg_wind_24}')


# Function contains the statistics (average of temp, humidity, and wind speed) of year 2025
def stats_25(data_2025):
    temperatures_25 = []
    for i in data_2025:
        try:
            temp = float(i['temperature'])
            temperatures_25.append(temp)
        except ValueError:
            continue  # Skip NA

    avg_temp_25 = round(sum(temperatures_25) / len(temperatures_25), 2)
    print(f'The average of temperatures in 2025 is {avg_temp_25}')

    # Humidity
    humidity_25 = []
    for i in data_2025:
        try:
            hum = float(i['humidity'])
            humidity_25.append(hum)
        except ValueError:
            continue  # Skip NA

    avg_humidity_25 = round(sum(humidity_25) / len(humidity_25), 2)
    print(f'The average of humidity in 2025 is {avg_humidity_25}')

    # Wind Speed
    wind_speed_25 = []
    for i in data_2025:
        try:
            wind = float(i['wind_speed'])
            wind_speed_25.append(wind)
        except ValueError:
            continue  # Skip NA

    avg_wind_25 = round(sum(wind_speed_25) / len(wind_speed_25), 2)
    print(f'The average of wind in 2025 is {avg_wind_25}')


# Function contains the statistics (average of temp, humidity, and wind speed) of the current year of the user
def stats_current(data_current_year):
    current_year = datetime.now().year
    
    temperatures_current = []
    for i in data_current_year:
        try:
            temp = float(i['temperature'])
            temperatures_current.append(temp)
        except ValueError:
            continue  # Skip NA

    avg_temp_current = round(sum(temperatures_current) / len(temperatures_current), 2)
    print(f'The average of temperatures in {current_year} is {avg_temp_current}')

    # Humidity
    humidity_current = []
    for i in data_current_year:
        try:
            hum = float(i['humidity'])
            humidity_current.append(hum)
        except ValueError:
            continue  # Skip NA

    avg_humidity_current = round(sum(humidity_current) / len(humidity_current), 2)
    print(f'The average of humidity in {current_year} is {avg_humidity_current}')

    # Wind Speed
    wind_speed_current = []
    for i in data_current_year:
        try:
            wind = float(i['wind_speed'])
            wind_speed_current.append(wind)
        except ValueError:
            continue  # Skip NA

    avg_wind_current = round(sum(wind_speed_current) / len(wind_speed_current), 2)
    print(f'The average of wind in {current_year} is {avg_wind_current}')



#Asking the user which year they want to display their stats?
while True:
        year_choice = input("Choose a year to view stats (2024, 2023, 2022) or type 'exit' to quit: ")


        if year_choice == '2025':
            stats_25(data_2025)
            
        elif year_choice == '2024':
            stats_current(data_current_year)
            stats_24(data_2024)

        elif year_choice == '2023':
            stats_current(data_current_year) 
            stats_23(data_2023)

        elif year_choice.lower() == 'exit':
            print("Exit")
            break

        else:
            print("Invalid input. Please enter 2024, 2023, 2022 or 'exit'.")