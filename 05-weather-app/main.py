import requests
from dotenv import load_dotenv
import os


def get_weather(city):
  load_dotenv()
  api_key = os.getenv("API_KEY")
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  response = requests.get(url)
  data = response.json() #the response just comes back as JSON formatted text over the internet, and response.json() converts it into a Python dictionary for you to work with
  return data

def display_weather(data):
    city = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    
    print(f"\nCity: {city}")
    print(f"Temperature: {temp}°C")
    print(f"Feels like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Condition: {description}")

def main():
    while True:
        print("\n1. View a city's weather details")
        print("2. Quit")
        choice = int(input("Enter choice: "))
        if choice == 1:
           city = input("Enter city name: ")
           data = get_weather(city)
           display_weather(data) 
        elif choice == 2:
            break
     

main()


