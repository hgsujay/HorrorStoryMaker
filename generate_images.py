from openai import OpenAI
import requests
import shutil
from diffusers import DiffusionPipeline
import torch
import json
import os


config = json.load(open("config.json"))
open_ai_api_key = config["openai_api_key"]
additional_style_tags = config["additional_style_tags"]
sd_model = config["sd_model"]
pipe = DiffusionPipeline.from_pretrained(
                                        sd_model,
                                        torch_dtype=torch.float16,
                                        use_safetensors=True,
                                        variant="fp16")
# pipe = DiffusionPipeline.from_pretrained(sd_model)
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


def generate_images_using_sd(image_description, img_file_path):
    prompt = image_description + " " + additional_style_tags
    images = pipe(prompt=prompt, height=config["sd_base_image_height"], width=config["sd_base_image_width"],
                  negative_prompt="worst, bad, text").images[0]
    images.save(img_file_path)
    # upscale the image using real-esrgan
    os.chdir(os.getcwd())

    cmd = os.getcwd() + "\\RESRGAN\\realesrgan-ncnn-vulkan.exe -i " + img_file_path + " -o " + img_file_path + " -s " + str(config["resrgan_upscale_factor"])
    os.system(cmd)
