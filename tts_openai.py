from openai import OpenAI
import random
import os
import json

config = json.load(open("config.json"))
open_ai_api_key = config["openai_api_key"]


def generate_tts(input_text, speech_file_path, voice):
    client = OpenAI(api_key=open_ai_api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=input_text
    )
    response.stream_to_file(speech_file_path)


def GenerateSpeechForThread(reddit_object):
    path = os.path.join("Outputs", reddit_object.thread_id, "speech")
    if not os.path.exists(path):
        os.makedirs(path)
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    voice = random.choice(voices)
    speech_file_path = os.path.join(path, "thread_" + reddit_object.thread_id + ".mp3")
    generate_tts(reddit_object.thread_title + reddit_object.thread_body,
                 speech_file_path, voice)
