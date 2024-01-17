import requests
import json
from bs4 import BeautifulSoup
import random
import pyttsx3
import time

def text_to_speech(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speed (words per minute)
    female_voice = None
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            female_voice = voice
            break

    if female_voice:
        engine.setProperty('voice', female_voice.id)
    else:
        print("Female voice not found. Using the default voice.")

    engine.say(text)
    engine.runAndWait()

def start():
    categories = ['india', 'business', 'politics', 'sports', 'technology', 'startups', 'entertainment', 'hatke', 'international', 'automobile', 'science', 'travel', 'miscellaneous', 'fashion', 'education']
    url = f'https://www.inshorts.com/en/read/{categories[random.randint(0, len(categories))]}'

    response = requests.get(url)
    html_data = response.text

    soup = BeautifulSoup(html_data, 'html.parser')

    script_tag = soup.find('script', text=lambda x: x and 'window.__STATE__ =' in x)

    if script_tag:
        # Extract the content of the script tag
        script_content = script_tag.text

        json_content = script_content.replace('window.__STATE__ = ', '')

        try:
            # Load the JSON content into a Python dictionary
            state_data = json.loads(json_content[:-1])

            # Display the resulting dictionary
            for i in state_data["news_list"]["list"]:
                text_to_speech(str(i["news_obj"]["title"] + i["news_obj"]["content"]), "en")
                print(i["news_obj"]["title"])
                print(i["news_obj"]["content"])
                print(i["news_obj"]["image_url"])
                time.sleep(5)


        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        
    else:
        print("Script tag with window.__STATE__ not found.")
start()
