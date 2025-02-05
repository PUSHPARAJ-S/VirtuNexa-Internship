import time
import json
import requests
import sqlite3
from datetime import datetime
import logging
import threading

# Setup logging
logging.basicConfig(filename="assistant.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Database setup
conn = sqlite3.connect("assistant.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    response TEXT,
                    timestamp TEXT)''')
conn.commit()

# OpenWeather API (Replace 'YOUR_API_KEY' with an actual key)
API_KEY = "YOUR_API_KEY"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return "City not found!"
        weather = f"Weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C"
        return weather
    except Exception as e:
        return f"Error fetching weather: {e}"

def set_reminder(reminder_text, seconds):
    def reminder():
        time.sleep(seconds)
        print(f"\n[Reminder]: {reminder_text}")
        logging.info(f"Reminder triggered: {reminder_text}")
    threading.Thread(target=reminder).start()
    return f"Reminder set: {reminder_text} in {seconds} seconds"

def simple_calculator():
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                return "Error: Division by zero!"
            result = num1 / num2
        else:
            return "Invalid operator!"

        logging.info(f"Calculation performed: {num1} {op} {num2} = {result}")
        return f"Result: {result}"
    except ValueError:
        return "Invalid input! Please enter numbers only."

def save_to_db(command, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO history (command, response, timestamp) VALUES (?, ?, ?)", (command, response, timestamp))
    conn.commit()

def main():
    print("Welcome to Simple Virtual Assistant!")
    
    while True:
        command = input("\nEnter a command (weather, reminder, calculate, exit): ").lower()
        
        if command == "weather":
            city = input("Enter city name: ")
            response = get_weather(city)
        
        elif command == "reminder":
            text = input("Enter reminder text: ")
            seconds = int(input("Set reminder in how many seconds? "))
            response = set_reminder(text, seconds)
        
        elif command == "calculate":
            response = simple_calculator()
        
        elif command == "exit":
            print("Goodbye!")
            break
        
        else:
            response = "Unknown command!"
        
        print(response)
        save_to_db(command, response)

if __name__ == "__main__":
    main()
