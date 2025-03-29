import os
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from datetime import datetime


# Create search tool
def create_search_tool():
    search = DuckDuckGoSearchRun()
    return Tool(
        name="Search",
        func=search.run,
        description="Search the web for information on any topic. Use this for general knowledge queries. Don't make multiple calls to the same tool in a single query.",
    )

# Create a weather tool using OpenWeatherMap API
def get_weather(location: str) -> str:
    """Get the current weather for a location using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # For Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            weather_desc = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            
            return f"Current weather in {location}: {weather_desc}, Temperature: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%, Wind speed: {wind_speed} m/s"
        else:
            return f"Error getting weather data: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Failed to get weather data: {str(e)}"

def create_weather_tool():
    return Tool(
        name="WeatherInfo",
        func=get_weather,
        description="Get current weather information for a specific location. Input should be a city name.",
    )

# Create a calculator tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

def create_calculator_tool():
    return Tool(
        name="Calculator",
        func=calculate,
        description="Calculate mathematical expressions. Input should be a valid mathematical expression.",
    )

# Function to get all tools
def get_tools():
    return [
        create_search_tool(),
        create_weather_tool(),
        create_calculator_tool()
    ]
