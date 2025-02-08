import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Constants
API_KEY = "your_openweathermap_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Database setup (optional)
def setup_database():
    conn = sqlite3.connect("weather_history.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT,
                        temperature REAL,
                        humidity REAL,
                        wind_speed REAL,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

def save_to_database(location, temperature, humidity, wind_speed):
    conn = sqlite3.connect("weather_history.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO history (location, temperature, humidity, wind_speed, timestamp)
                      VALUES (?, ?, ?, ?, ?)''', (location, temperature, humidity, wind_speed, datetime.now()))
    conn.commit()
    conn.close()

# Fetch weather data
def get_weather_data(location):
    try:
        params = {"q": location, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            return weather_info
        else:
            raise ValueError(data.get("message", "Failed to fetch weather data."))
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Console-based interface
def console_interface():
    location = input("Enter a location (city name): ")
    try:
        weather_data = get_weather_data(location)
        print(f"\nWeather in {location.capitalize()}:")
        print(f"Temperature: {weather_data['temperature']} °C")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        save_to_database(location, weather_data['temperature'], weather_data['humidity'], weather_data['wind_speed'])
    except ValueError as e:
        print(str(e))

# GUI interface (optional)
def gui_interface():
    def fetch_weather():
        location = entry_location.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location.")
            return

        try:
            weather_data = get_weather_data(location)
            result_label.config(text=f"Weather in {location.capitalize()}:\n"
                                     f"Temperature: {weather_data['temperature']} °C\n"
                                     f"Humidity: {weather_data['humidity']}%\n"
                                     f"Wind Speed: {weather_data['wind_speed']} m/s")
            save_to_database(location, weather_data['temperature'], weather_data['humidity'], weather_data['wind_speed'])
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    app = tk.Tk()
    app.title("Weather App")

    tk.Label(app, text="Enter location:").grid(row=0, column=0, padx=10, pady=10)
    entry_location = tk.Entry(app)
    entry_location.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(app, text="Get Weather", command=fetch_weather).grid(row=0, column=2, padx=10, pady=10)

    result_label = tk.Label(app, text="", justify=tk.LEFT)
    result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    app.mainloop()

# Main execution
if __name__ == "__main__":
    setup_database()

    mode = input("Choose mode (console/gui): ").strip().lower()
    if mode == "console":
        console_interface()
    elif mode == "gui":
        gui_interface()
    else:
        print("Invalid mode selected. Exiting.")