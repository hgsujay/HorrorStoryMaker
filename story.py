import os
import time
import random
from tts_openai import generate_tts
from generate_images import generate_images_using_sd
import json


# paragraph class contains body, images, audio
class Paragraph:
    def __init__(self, body, story_id, order, image_description):
        self.story_id = story_id
        self.order = order
        self.body = body
        self.image = ""
        self.voiceover = ""
        self.image_desctiption = image_description
        self.path = os.path.join("Outputs", self.story_id, str(self.order))

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_images(self, prompt_override=""):
        img_file_path = os.path.join(self.path, "images.png")
        print("Generating images for paragraph " + str(self.order))
        print("Generating images for: " + self.body)
        if prompt_override != "":
            generate_images_using_sd("", prompt_override, img_file_path)
        else:
            generate_images_using_sd(self.image_desctiption, img_file_path)
        self.image = img_file_path

    def generate_voiceover(self, voice):
        speech_file_path = os.path.join(self.path, "speech.mp3")
        generate_tts(self.body, speech_file_path, voice)
        self.voiceover = speech_file_path


# story class contains, title, body and paragraphs
class Story:
    def __init__(self, file_path="input.json"):
        self.id = ""
        self.title = ""
        self.body = ""
        self.paragraphs: list[Paragraph] = []
        self.load_story_from_json(file_path)
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
            context = ""
            for paragraph in paragraphs:
                if context == "":
                    config = json.load(open("config.json"))
                    para_obj = Paragraph(paragraph, self.id, order, config["title_image_location"])
                else:
                    para_obj = Paragraph(paragraph, self.id, order, context)
                self.paragraphs.append(para_obj)
                context = context + " " + paragraph
                order += 1

    def load_story_from_json(self, json_file_path):
        self.generate_timestamp()
        with open(json_file_path, 'r') as file:
            json_obj = json.load(file)
            self.title = json_obj['title']
            self.paragraphs = []
            config = json.load(open("config.json"))
            order = 0
            para_obj = Paragraph(self.title, self.id, order, config["title_image_location"])
            self.paragraphs.append(para_obj)
            order += 1
            for para in json_obj['paragraphs']:
                para_obj = Paragraph(para['content'], self.id, order, para['image_description'])
                self.paragraphs.append(para_obj)
                order += 1

    def generate_timestamp(self):
        # Generate a string with format yyyy_mm_dd_hh_mm_ss
        self.id = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        # self.id = "2024_01_03_09_47_17"
        print(self.id)

    def regenerate_images(self, order):
        for paragraph in self.paragraphs:
            if paragraph.order == order:
                paragraph.generate_images()
                break
