import csv
import uuid
from datetime import date, datetime, timedelta


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