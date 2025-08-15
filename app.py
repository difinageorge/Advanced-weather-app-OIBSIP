import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Replace with your OpenWeatherMap API Key
API_KEY = "1191720523938c10f625690393116229"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch and display weather
def get_weather():
    city = city_entry.get()
    unit = unit_var.get()
    units_param = "metric" if unit == "C" else "imperial"

    params = {"q": city, "appid": API_KEY, "units": units_param}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        desc = data['weather'][0]['description'].capitalize()
        icon_code = data['weather'][0]['icon']

        # Display weather info
        weather_label.config(text=f"{city}\n{desc}\nTemp: {temp}°{unit}\nHumidity: {humidity}%\nWind: {wind} m/s")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo

    else:
        messagebox.showerror("Error", "City not found or API request failed.")

# GUI setup
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("400x450")
root.resizable(False, False)

# City input
tk.Label(root, text="Enter City:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

# Unit selection
unit_var = tk.StringVar(value="C")
tk.Radiobutton(root, text="Celsius", variable=unit_var, value="C").pack()
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="F").pack()

# Get weather button
tk.Button(root, text="Get Weather", command=get_weather).pack(pady=10)

# Weather display
weather_label = tk.Label(root, text="", font=("Arial", 12))
weather_label.pack(pady=10)

# Weather icon
icon_label = tk.Label(root)
icon_label.pack(pady=5)

root.mainloop()
