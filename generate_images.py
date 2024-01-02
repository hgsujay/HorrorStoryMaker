from openai import OpenAI
import requests
import shutil
from diffusers import DiffusionPipeline
import torch
import json
import os


config = json.load(open("config.json"))
open_ai_api_key = config["openai_api_key"]
sd_model = config["sd_model"]
pipe = DiffusionPipeline.from_pretrained(
                                        sd_model,
                                        torch_dtype=torch.float16,
                                        use_safetensors=True,
                                        variant="fp16")
pipe.to("cuda")


def generate_images_open_ai(input_text, img_file_path):
    client = OpenAI(api_key=open_ai_api_key)
    response = client.images.generate(
                            model="dall-e-3",
                            prompt=input_text,
                            size="1024x1792",
                            quality="hd",
                            n=1)

    image_url = response.data[0].url
    print(image_url)
    res = requests.get(image_url, stream=True)
    with open(img_file_path, 'wb') as out_file:
        shutil.copyfileobj(res.raw, out_file)


def generate_images_using_sd(input_text, img_file_path):
    client = OpenAI(api_key=open_ai_api_key)
    response = client.chat.completions.create(
                        model="gpt-3.5-turbo-1106",
                        # response_format={"type": "json_object"},
                        messages=[
                                {"role": "system", "content": "You are a helpful assistant designed to generate midjourney prompts" +
                                 "You are given a text, and you will generate a midjourney prompt, less than 70 characters."},
                                {"role": "user", "content": input_text + " horror style, dark, creepy, pixar style"}])

    prompt = response.choices[0].message.content + " horror style, dark, creepy, pixar style"
    images = pipe(prompt=prompt, height=config["sd_base_image_height"], width=config["sd_base_image_width"], negative_prompt="worst, bad, text").images[0]
    images.save(img_file_path)
    # upscale the image using real-esrgan
    os.chdir(os.getcwd())

    cmd = os.getcwd() + "\\RESRGAN\\realesrgan-ncnn-vulkan.exe -i " + img_file_path + " -o " + img_file_path + " -s " + str(config["resrgan_upscale_factor"])
    os.system(cmd)


# generate_images_using_sd(
#                         "One night, unable to resist their call, I rose and danced with them." +
#                         " We moved through the darkness, the shadows enveloping me, caressing me with cold, intangible fingers." +
#                         " Their whispers grew louder, turning into chants that echoed in the confines of my room.",
#                         "forest.png")
