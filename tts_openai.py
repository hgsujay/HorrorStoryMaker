from openai import OpenAI
import random
import os


def generate_tts(input_text, speech_file_path, voice):
    client = OpenAI(api_key="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")
    # speech_file_path = "speech.mp3"
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
