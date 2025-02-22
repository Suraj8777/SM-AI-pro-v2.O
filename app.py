from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import requests
import random

app = Flask(__name__)
CORS(app)

# API Keys Configuration
API_KEYS = {
    'weather': 'a5caf05ac5bff33416c4fafb3d168ae1',
    'openai': [
        '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',
        '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',
        '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'
    ]
}

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={API_KEYS['weather']}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def get_ai_response(prompt):
    current_key = random.choice(API_KEYS['openai'])
    openai.api_key = current_key
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

@app.route('/process', methods=['POST'])
def process_query():
    data = request.get_json()
    query = data['query'].lower()
    
    if 'weather' in query:
        city = query.split('in ')[1] if 'in ' in query else 'London'
        weather_data = get_weather(city)
        return jsonify({'response': f"Weather in {city}: {weather_data['main']['temp']}°C"})
    else:
        ai_response = get_ai_response(query)
        return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
