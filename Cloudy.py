import csv
import uuid
from datetime import date, datetime, timedelta

def add_observation():
    """To add new weather observation to cloudy csv file"""

    # Create a file if not exist
    try:
        with open('cloudy.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)

    #Confirmation message if the file exist
        print('\ncloudy.csv exist.')

    except :
        with open('cloudy.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'date', 'temperature', 'weather_condition', 'humidity_percentage', 'wind_speed'])
            print(f'\n New csv {file} has been created 1')
    print("\n=== Record a New Weather Observation ===")


    # To create unique id everytime a observation is added     
    observation_id = str(uuid.uuid4())[:8] 



    # Validate The observation date
    while True:
        observation_date = input("Enter the date in (MM-DD-YYYY) format, or press Enter for today date: ")
        if not observation_date.strip():  # Use today's date
            observation_date = date.today().strftime("%m-%d-%Y")
            break
        try:
            datetime.strptime(observation_date, "%m-%d-%Y")
            break
        except ValueError:
            print("The entered date format is invalid. Please use (MM-DD-YYYY) format.")


    # Validate temperature
    while True:
        try:
            temperature = float(input("Enter temperature (Celsius): "))
            break
        except ValueError:
            print("Please enter a valid number for temperature.")


    # Validate weather condition
    weather_condition = ["sunny", "cloudy", "rainy", "snowy", 'other']
    print("\nWeather condition options: Sunny, Cloudy, Rainy, Snowy, other")
    while True:
        try:
            print("Please enter valid weather condition [Sunny, Cloudy, Rainy, Snowy, other]")
            condition = input("Enter weather condition: ").lower()
            if condition == 'other':
                condition = input('Please enter the weather condition')    
            if condition in weather_condition:
                break
            else:
                print("Invalid condition. Please choose from these options: Sunny, Cloudy, Rainy, Snowy, other")
            if len(condition) == 0:
                print("Condition cannot be empty.")
            elif len(condition) > 20:
                print("Condition cannot exceed  20 characters).")
        except ValueError:
            print("Please enter a valid Weather condition")

            
    # Validate humidity percentage
    while True:
        try:
            humidity = int(input("Enter the humidity percentage in the range of (0–100): "))
            if humidity >= 0 and humidity <= 100:
                break
            else:
                 print("Humidity cannot be under 0 or over 100.")
        except ValueError:
            print("Please enter a valid number.")      


    # Validate wind speed
    while True:
        try:
            wind_speed = float(input("Please enter the observed wind speed in km/h: "))
            if wind_speed >= 0:
                break
            else:
                print("Wind speed cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")



            
    # To Create new observation
    new_observation = {
        'id': observation_id,
        'date': observation_date,
        'temperature': temperature,
        'weather_condition': condition,
        'humidity_percentage': humidity,
        'wind_speed': wind_speed,
    }


    # Write the new observation into the cloudy.csv
    try:
        with open('cloudy.csv', 'a', newline='') as file:
            fields = ['id', 'date', 'temperature', 'weather_condition', 'humidity_percentage', 'wind_speed']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow(new_observation)
            print(f"\nWeather observation for {observation_date} added successfully!")
    except Exception as exp:
        print(f"Error saving observation: {exp}")

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

