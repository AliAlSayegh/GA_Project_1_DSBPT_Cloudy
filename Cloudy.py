import pandas as pd
import numpy as np
import random, math, uuid, pytz, csv
from datetime import date, datetime, timedelta

# # Weather conditions list
# conditions = ["sunny", "cloudy", "rainy", "stormy", "foggy", "snowy", "windy"]

# # Open CSV file
# with open("Cloudy.csv", "w", newline="") as file:
#     writer = csv.writer(file)
    
#     # Write header
#     writer.writerow(["id", "date", "temperature", "condition", "humidity", "wind_speed"])
    
#     # Date range: from today back 2 years
#     today = datetime.now()
#     start_date = today - timedelta(days=730)  # approx 2 years
    
#     # Generate 20 records
#     for _ in range(730):
#         record_id = uuid.uuid4().hex[:8]  # 8-char unique id
#         # Random date in the last 2 years
#         date = (start_date + timedelta(days=random.randint(0, 730))).strftime("%d-%m-%Y")
        
#         # Weather values
#         temperature = round(random.uniform(-5, 45), 1)   # realistic temp range
#         condition = random.choice(conditions)
#         humidity = random.randint(20, 100)              # %
#         wind_speed = round(random.uniform(0, 50), 1)    # km/h
        
#         # Write row
#         writer.writerow([record_id, date, temperature, condition, humidity, wind_speed])
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def generate_weather_csv(out_path="cloudy.csv",
                         start_date="2020-01-01",
                         end_date="2025-01-01",
                         hour=9,
                         tz_name="Asia/Bahrain",
                         seed=73):
    random.seed(seed)
    np.random.seed(seed)
    tz = pytz.timezone(tz_name)
    start_dt = tz.localize(datetime.strptime(start_date, "%Y-%m-%d").replace(hour=hour))
    end_dt   = tz.localize(datetime.strptime(end_date, "%Y-%m-%d").replace(hour=hour))
    dates = pd.date_range(start=start_dt, end=end_dt, freq="D", tz=tz)
    conditions = ["sunny", "cloudy", "rainy", "dusty", "humid"]
    condition_weights = {
        1: [0.65, 0.20, 0.05, 0.05, 0.05],
        2: [0.62, 0.22, 0.06, 0.05, 0.05],
        3: [0.58, 0.24, 0.08, 0.05, 0.05],
        4: [0.60, 0.23, 0.07, 0.05, 0.05],
        5: [0.68, 0.18, 0.04, 0.05, 0.05],
        6: [0.72, 0.15, 0.03, 0.06, 0.04],
        7: [0.75, 0.12, 0.02, 0.07, 0.04],
        8: [0.72, 0.13, 0.03, 0.07, 0.05],
        9: [0.65, 0.18, 0.05, 0.05, 0.07],
        10:[0.62, 0.22, 0.07, 0.04, 0.05],
        11:[0.60, 0.25, 0.08, 0.03, 0.04],
        12:[0.62, 0.23, 0.08, 0.03, 0.04],
    }
    def seasonal_temp(day):
        month_mean = {
            1: 18, 2: 19, 3: 22, 4: 27, 5: 32, 6: 35,
            7: 38, 8: 38, 9: 35, 10: 31, 11: 25, 12: 20
        }
        base = month_mean[day.month]
        daily_noise = np.random.normal(0, 2)
        weekly = 1.5 * math.sin(2 * math.pi * (day.timetuple().tm_yday % 7) / 7)
        return round(base + daily_noise + weekly, 1)
    def seasonal_humidity(day, condition):
        base = {
            1: 60, 2: 58, 3: 55, 4: 55, 5: 55, 6: 60,
            7: 65, 8: 68, 9: 70, 10: 60, 11: 58, 12: 60
        }[day.month]
        adj = 0
        if condition in ("rainy", "humid"):
            adj += 10
        if condition == "dusty":
            adj -= 8
        val = base + adj + np.random.normal(0, 6)
        return int(np.clip(round(val), 25, 100))
    def seasonal_wind(day, condition):
        base = {
            1: 12, 2: 13, 3: 15, 4: 18, 5: 20, 6: 22,
            7: 22, 8: 20, 9: 18, 10: 16, 11: 14, 12: 12
        }[day.month]
        adj = 0
        if condition == "dusty":
            adj += 8
        if condition == "rainy":
            adj += 4
        val = base + adj + np.random.normal(0, 4)
        return float(np.clip(round(val, 1), 0, 60))
    def uuid8(existing):
        while True:
            s = uuid.uuid4().hex[:8]
            if s not in existing:
                return s
    rows, used = [], set()
    for dt in dates:
        cond = random.choices(conditions, weights=condition_weights[dt.month], k=1)[0]
        rows.append({
            "id": uuid8(used),
            "date": dt.strftime("%m-%d-%Y"),
            "temperature": seasonal_temp(dt),
            "weather_condition": cond,
            "humidity_percentage": seasonal_humidity(dt, cond),
            "wind_speed": seasonal_wind(dt, cond),
        })
        used.add(rows[-1]["id"])
    df = pd.DataFrame(rows, columns=[
        "id","date","temperature","weather_condition",
        "humidity_percentage","wind_speed"
    ])
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")
    return df
# /////////////////////////////////////////////////////////////////////////



def add_observation():
    """To add new weather observation to cloudy csv file"""
    # To check if the CSV file exists
    try:
        with open('cloudy.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
    # print confirmation message if CSV exist
        print('\ncloudy.csv exist.')
    # To Create a file if not exist with the header row
    except :
        with open('cloudy.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'date', 'temperature', 'weather_condition', 'humidity_percentage', 'wind_speed'])
            print(f'\n New CSV {file} has been created')
    print("\n=== Record a New Weather Observation ===")
    # To create unique id everytime a observation is added
    observation_id = str(uuid.uuid4())[:8]
    # Ask the user for the observation date, if the user pressed enter it will use today date
    while True:
        observation_date = input("Enter the date in (MM-DD-YYYY) format, or press Enter for today date: ")
        if not observation_date.strip():
            observation_date = date.today().strftime("%m-%d-%Y")
            break
        try:
            datetime.strptime(observation_date, "%m-%d-%Y")
            break
        except ValueError:
            print("The entered date format is invalid. Please use (MM-DD-YYYY) format.")
    # Ask the use to input the recorded temperature, it will track and display if a temperature record has been broken
    while True:
        try:
            temperature = float(input("Enter temperature (Celsius): "))
            temps = []
            with open('cloudy.csv', 'r') as file:
                reader = csv.DictReader(file)
                for i in reader:
                    temps.append(float(i['temperature']))
                if temps:
                    max_temp = max(temps)
                    min_temp = min(temps)
                    if temperature > max_temp:
                        print(f'Your weather observation broke a new record as the maximum recorded temperature!')
                    elif temperature < min_temp:
                        print(f'Your weather observation broke a new record as the minimum recorded temperature!')
                break
        except ValueError:
            print("Please enter a valid number for temperature.")
    # Ask the user for the observed weather condition, it will track and display if the weather condition never been recorded before
    # Condition cannot exceed 20 charecters and cannot be empty
   

    print("\nWeather condition options: Sunny, Cloudy, Rainy, Snowy, Other")

    while True:
        condition = input("Enter weather condition: ").lower()

        if condition in ["sunny", "cloudy", "rainy", "snowy"]:
            # Standard condition → proceed
            break

        elif condition == "other":
            custom_condition = input("Please enter the weather condition: ").lower()

            if len(custom_condition) == 0:
                print("Condition cannot be empty.")
                continue
            elif len(custom_condition) > 20:
                print("Condition cannot exceed 20 characters.")
                continue

            # Load existing conditions from CSV
            conditions_that_exist = []
            try:
                with open("cloudy.csv", "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        conditions_that_exist.append(row["weather_condition"].lower())
            except FileNotFoundError:
                conditions_that_exist = []  # if CSV doesn't exist yet

            if custom_condition not in conditions_that_exist:
                print(f"{custom_condition} is a new weather condition!")

            condition = custom_condition  # Save the custom condition
            break

        else:
            print("Invalid condition. Please choose from: Sunny, Cloudy, Rainy, Snowy, Other.")


    # Ask the user for the observed humidity percentage
    # Humidity percentage cannot be lower then 0 and more then 100
    while True:
        try:
            humidity = int(input("Enter the humidity percentage in the range of (0–100): "))
            if humidity >= 0 and humidity <= 100:
                break
            else:
                 print("Humidity cannot be under 0 or over 100.")
        except ValueError:
            print("Please enter a valid number.")
    # Ask the user for the observed wind speed
    # Wind speed cannot be negative
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
    """Display the Weather information for specific day, month, or season."""
    print("\n=== Filter Weather Observations ===")
    print("1. Filter by Day")
    print("2. Filter by Month")
    print("3. Filter by Season")

    choice = input("Choose an option (1/2/3): ").strip()

    # Try to open and filter the CSV file
    try:
        with open('Cloudy.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            matches = []

            # 1️ Filter by Day
            if choice == "1":
                while True:
                    selected_date = input("Enter the date in (MM-DD-YYYY) format, or press Enter for today: ")
                    if not selected_date.strip():  # Use today's date
                        selected_date = date.today().strftime("%m-%d-%Y")
                        break
                    try:
                        datetime.strptime(selected_date, "%m-%d-%Y")
                        break
                    except ValueError:
                        print("Invalid date format. Please use (MM-DD-YYYY).")

                matches = [row for row in reader if row['date'] == selected_date]

            # 2️ Filter by Month
            elif choice == "2":
                while True:
                    month = input("Enter the month (MM): ")
                    if len(month) == 2 and month.isdigit() and 1 <= int(month) <= 12:
                        break
                    else:
                        print("Invalid month. Please enter two digits (01–12).")

                matches = [row for row in reader if row['date'].split("-")[0] == month]

            # 3 Filter by Season
            elif choice == "3":
                season = input("Enter season (winter/spring/summer/autumn): ").strip().lower()
                season_months = {
                    "winter": ["11", "12", "01"],
                    "spring": ["02", "03", "04"],
                    "summer": ["05", "06", "07"],
                    "autumn": ["08", "09", "10"],
                }

                if season not in season_months:
                    print(" Invalid season. Choose from: winter, spring, summer, autumn.")
                    return

                matches = [row for row in reader if row['date'].split("-")[0] in season_months[season]]

            else:
                print(" Invalid choice. you are send to the main menu.")
                return

            # Show results
            if matches:
                print(f"\n Found {len(matches)} record(s):")
                for row in matches:
                    print(row)
            else:
                print("\n No data found for your selection.")

    except FileNotFoundError:
        print("File 'Cloudy.csv' not found! Please make sure the file exists.")

def  Open_csv():
    """To open and read the cloudy csv file""" 
    try:
        with open('Cloudy.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            matches = [row for row in reader]

            if matches:
                # print(matches)
                return matches
            else:
                print(f"No data found in the file")
    except FileNotFoundError:
        print("File 'Cloudy.csv' not found! ;( Please make sure the file exists.")



# Function for Temperature Statistics
def display_weather_stats(observation):
    temperatures = [float(i['temperature']) for i in observation]  # Convert to float
    weather_conditions = [i['weather_condition'] for i in observation]  # Use correct key

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
    if datetime.strptime(i['date'], '%m-%d-%Y').year == 2022
]

data_2023 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%m-%d-%Y').year == 2023
]

data_2024 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%m-%d-%Y').year == 2024
]

data_2025 = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%m-%d-%Y').year == 2025
]

# Filter the data in the current year, aggregate them together
current_year = datetime.now().year
data_current_year = [
    i for i in cloudy
    if datetime.strptime(i['date'], '%m-%d-%Y').year == current_year
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
            hum = float(i['humidity_percentage'])
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
            hum = float(i['humidity_percentage'])
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
            hum = float(i['humidity_percentage'])
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
def stats_current(data_current):
    current_year = datetime.now().year
    
    temperatures_current = []
    for i in data_current:
        try:
            temp = float(i['temperature'])
            temperatures_current.append(temp)
        except ValueError:
            continue  # Skip NA

    avg_temp_current = round(sum(temperatures_current) / len(temperatures_current), 2)
    print(f'The average of temperatures in {current_year} is {avg_temp_current}')

    # Humidity
    humidity_current = []
    for i in data_current:
        try:
            hum = float(i['humidity_percentage'])
            humidity_current.append(hum)
        except ValueError:
            continue  # Skip NA

    avg_humidity_current = round(sum(humidity_current) / len(humidity_current), 2)
    print(f'The average of humidity in {current_year} is {avg_humidity_current}')

    # Wind Speed
    wind_speed_current = []
    for i in data_current:
        try:
            wind = float(i['wind_speed'])
            wind_speed_current.append(wind)
        except ValueError:
            continue  # Skip NA

    avg_wind_current = round(sum(wind_speed_current) / len(wind_speed_current), 2)
    print(f'The average of wind in {current_year} is {avg_wind_current}')



#Asking the user which year they want to display their stats?
def ask_year():
    while True:
            year_choice = input("Choose a year to view stats (2025, 2024, 2023) or type 'exit' to quit: ")

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
                print("Invalid input. Please enter 2025, 2024, 2023 or 'exit'.")

def predict_weather_tomorrow():
    try:
        with open("cloudy.csv", "r") as file:
            reader = list(csv.DictReader(file))

        if len(reader) < 7:
            print("Not enough data to predict (need at least 7 days).")
            return

        # Get last 7 days
        last_week = reader[-7:]

        # Extract numeric values
        temps = [float(row["temperature"]) for row in last_week]
        hums = [float(row["humidity_percentage"]) for row in last_week]
        winds = [float(row["wind_speed"]) for row in last_week]
        conditions = [row["weather_condition"].lower() for row in last_week]

        # --- Temperature prediction ---
        diffs_temp = [temps[i+1] - temps[i] for i in range(len(temps)-1)]
        avg_temp = sum(temps) / len(temps)
        avg_temp_diff = sum(diffs_temp) / len(diffs_temp)
        predicted_temp = round(avg_temp + avg_temp_diff, 1)

        # --- Humidity prediction ---
        diffs_hum = [hums[i+1] - hums[i] for i in range(len(hums)-1)]
        avg_hum = sum(hums) / len(hums)
        avg_hum_diff = sum(diffs_hum) / len(diffs_hum)
        predicted_hum = int(avg_hum + avg_hum_diff)

        # --- Wind prediction ---
        diffs_wind = [winds[i+1] - winds[i] for i in range(len(winds)-1)]
        avg_wind = sum(winds) / len(winds)
        avg_wind_diff = sum(diffs_wind) / len(diffs_wind)
        predicted_wind = round(avg_wind + avg_wind_diff, 1)

        # --- Weather condition prediction ---
        from collections import Counter
        condition_counts = Counter(conditions)
        predicted_condition = condition_counts.most_common(1)[0][0]

        # Show prediction
        tomorrow_date = datetime.strptime(last_week[-1]["date"], "%m-%d-%Y")
        tomorrow_date = tomorrow_date.replace(day=tomorrow_date.day + 1)
        formatted_date = tomorrow_date.strftime("%m-%d-%Y")

        print("\n=== Weather Prediction for Tomorrow ===")
        print(f"Date: {formatted_date}")
        print(f"Temperature: {predicted_temp} °C")
        print(f"Condition: {predicted_condition}")
        print(f"Humidity: {predicted_hum} %")
        print(f"Wind Speed: {predicted_wind} km/h")

    except FileNotFoundError:
        print("File 'cloudy.csv' not found!")
    except Exception as e:
        print(f"Error: {e}")

# ------------------------------------------------------------------------------------------

predict_weather_tomorrow()
# add_observation()
# filter_by_date()
# ask_year()
# new_observation = Open_csv()
# display_weather_stats(new_observation)
# Open_csv()
# generate_weather_csv(out_path="cloudy.csv",
#                          start_date="2020-09-03",
#                          end_date="2025-09-05")