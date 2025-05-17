import requests

API_KEY = "551fafd8eb2a63d2f26a085556d0b100"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(location):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # for Celsius
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = {
                "location": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize()
            }
            return weather
        else:
            return {"error": data.get("message", "Unable to fetch data.")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_weather(weather):
    if "error" in weather:
        print(f"Error: {weather['error']}")
    else:
        print(f"\n📍 Location: {weather['location']}")
        print(f"🌡 Temperature: {weather['temperature']}°C")
        print(f"💧 Humidity: {weather['humidity']}%")
        print(f"☁️ Weather: {weather['description']}\n")

def main():
    print("=== Weather App ===")
    while True:
        user_input = input("Enter location(s) (comma-separated) or 'quit' to exit: ").strip()
        if user_input.lower() == "quit":
            break
        locations = [loc.strip() for loc in user_input.split(",")]
        for loc in locations:
            weather_data = get_weather(loc)
            display_weather(weather_data)

if __name__ == "__main__":
    main()
