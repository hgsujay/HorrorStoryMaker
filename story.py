import os
import time
import random
from tts_openai import generate_tts
from generate_images import generate_images_using_sd


# paragraph class contains body, images, audio
class Paragraph:
    def __init__(self, body, story_id, order):
        self.story_id = story_id
        self.order = order
        self.body = body
        self.image = ""
        self.voiceover = ""
        self.path = os.path.join("Outputs", self.story_id, str(self.order))

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_images(self):
        img_file_path = os.path.join(self.path, "images.png")
        # generate_images_using_sd(self.body, img_file_path)
        self.image = img_file_path

    def generate_voiceover(self, voice):
        speech_file_path = os.path.join(self.path, "speech.mp3")
        # generate_tts(self.body, speech_file_path, voice)
        self.voiceover = speech_file_path


# story class contains, title, body and paragraphs
class Story:
    def __init__(self, file_path="input.txt"):
        self.id = ""
        self.title = ""
        self.body = ""
        self.paragraphs: list[Paragraph] = []
        self.load_story(file_path)
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        self.narrator = random.choice(voices)

        for paragraph in self.paragraphs:
            paragraph.generate_voiceover(self.narrator)
            paragraph.generate_images()

    def load_story(self, file_path):
        self.generate_timestamp()
        with open(file_path, 'r') as file:
            # Read the entire content of the file
            text = file.read()
            # Split the text into paragraphs
            paragraphs = text.strip().split('\n\n')
            self.title = paragraphs[0]
            order = 0
            for paragraph in paragraphs:
                self.paragraphs.append(Paragraph(paragraph, self.id, order))
                order += 1

    def generate_timestamp(self):
        # Generate a string with format yyyy_mm_dd_hh_mm_ss
        self.id = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        self.id = "2023_12_31_16_34_40"
        print(self.id)
