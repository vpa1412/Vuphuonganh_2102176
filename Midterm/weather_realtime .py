import os
import csv
import requests
import pandas as pd
from datetime import datetime

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


API_KEY = "ce01e2fc2c3be45a92d3e7d4819dfa72"
CITIES = ["Hanoi", "Hue", "Ho Chi Minh City"]  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CSV_FILENAME = "weather_data.csv"


if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Timestamp",
            "City",
            "Country",
            "Temperature (°C)",
            "Feels Like (°C)",
            "Humidity (%)",
            "Wind Speed (m/s)",
            "Weather Description"
        ])

# DASH 
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Weather Comparison Across Multiple Cities"),

    # Block to display text (weather for each city)
    html.Div(id="weather-text", style={"margin-bottom": "20px"}),

    # Comparison chart
    dcc.Graph(id="weather-chart"),

    # Interval: Trigger callback every 30 seconds
    dcc.Interval(
        id="interval-component",
        interval=30 * 1000,
        n_intervals=0
    )
])


# CALLBACK
@app.callback(
    Output("weather-chart", "figure"),
    Output("weather-text", "children"),
    Input("interval-component", "n_intervals")
)
def update_weather(n):
    """
    Every 30 seconds:
      1) Fetch weather data for each city.
      2) Append the data to the CSV.
      3) Read DataFrame to draw a comparison bar chart among cities.
    """
    rows = []
    status_texts = []

    for city in CITIES:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            
            # Extract information
            city_name = data["name"]
            country = data["sys"]["country"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            weather_desc = data["weather"][0]["description"].capitalize()

            # Log text
            status_texts.append(
                f"{city_name}, {country} -> Temp: {temperature}°C, "
                f"Feels: {feels_like}°C, Humi: {humidity}%, "
                f"Wind: {wind_speed} m/s, {weather_desc}"
            )

            # Save to CSV
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(CSV_FILENAME, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp,
                    city_name,
                    country,
                    temperature,
                    feels_like,
                    humidity,
                    wind_speed,
                    weather_desc
                ])

            # Prepare data for charting
            rows.extend([
                {"City": city_name, "Metric": "Temperature (°C)", "Value": temperature},
                {"City": city_name, "Metric": "Feels Like (°C)", "Value": feels_like},
                {"City": city_name, "Metric": "Humidity (%)",     "Value": humidity},
                {"City": city_name, "Metric": "Wind Speed (m/s)", "Value": wind_speed}
            ])
        else:
            status_texts.append(f"Error retrieving data for {city}.")

    # If no data is retrieved, draw an empty chart
    if not rows:
        fig = px.bar(title="No data to display.")
        return fig, "No data available."

    df = pd.DataFrame(rows)

    fig = px.bar(
        df,
        x="Metric",
        y="Value",
        color="City",
        barmode="group",
        text="Value",
        title="Weather Comparison Across Multiple Cities"
    )
    fig.update_traces(textposition="outside")

    # list of <p> elements for each city’s weather status
    final_paragraphs = [html.P(text) for text in status_texts]

    return fig, final_paragraphs

if __name__ == "__main__":
    app.run_server(debug=True, port=8054)