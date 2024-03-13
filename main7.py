# Imports necessary modules
import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and configure labels and entry fields
city_label = tk.Label(root, text="City:")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

temperature_label = tk.Label(root, text="Temperature:")
temperature_label.pack()
temperature_entry = tk.Entry(root)
temperature_entry.pack()

weather_label = tk.Label(root, text="Weather:")
weather_label.pack()
weather_entry = tk.Entry(root)
weather_entry.pack()

# Create buttons for CRUD operations
fetch_button = tk.Button(root, text="Fetch Weather")
fetch_button.pack()
save_button = tk.Button(root, text="Save Weather")
save_button.pack()
delete_button = tk.Button(root, text="Delete Weather")
delete_button.pack()

# Create a label to display weather information
weather_info_label = tk.Label(root, text="")
weather_info_label.pack()

# Database connection
conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS weather_data
             (city TEXT, temperature REAL, weather TEXT)''')
conn.commit()

# CRUD functions
def save_weather():
    try:
        city = city_entry.get()
        temperature = float(temperature_entry.get())  # Convert temperature to float
        weather = weather_entry.get()
        c.execute("INSERT INTO weather_data VALUES (?, ?, ?)", (city, temperature, weather))
        conn.commit()
        messagebox.showinfo("Success", "Weather data saved successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid temperature format. Please enter a valid number.")

def read_weather():
    city = city_entry.get()
    c.execute("SELECT * FROM weather_data WHERE city=?", (city,))
    data = c.fetchone()
    if data:
        city, temperature, weather = data
        weather_info_label.config(text=f"City: {city}\nTemperature: {temperature}°C\nWeather: {weather}")
    else:
        messagebox.showwarning("Not Found", "Weather data not found for the specified city.")

def update_weather():
    try:
        city = city_entry.get()
        temperature = float(temperature_entry.get())  # Convert temperature to float
        weather = weather_entry.get()
        c.execute("UPDATE weather_data SET temperature=?, weather=? WHERE city=?", (temperature, weather, city))
        conn.commit()
        messagebox.showinfo("Success", "Weather data updated successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid temperature format. Please enter a valid number.")

def delete_weather():
    city = city_entry.get()
    c.execute("DELETE FROM weather_data WHERE city=?", (city,))
    conn.commit()
    messagebox.showinfo("Success", "Weather data deleted successfully.")

def fetch_weather():
    city = city_entry.get()
    api_key = "7f44d50559f6c562f75b3299581c4079"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        temperature_entry.delete(0, tk.END)
        weather_entry.delete(0, tk.END)
        temperature_entry.insert(0, temperature)
        weather_entry.insert(0, weather)
        weather_info_label.config(text=f"Temperature: {temperature}°C\nWeather: {weather}")
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

# Define auto-refresh function
def auto_refresh():
    fetch_weather()
    root.after(15000, auto_refresh)  # Refresh every 15 seconds

# Configure buttons to call CRUD functions
fetch_button.config(command=fetch_weather)
save_button.config(command=save_weather)
delete_button.config(command=delete_weather)

# Start auto-refresh
auto_refresh()

# Start the GUI main loop
root.mainloop()

# Close database connection
conn.close()
