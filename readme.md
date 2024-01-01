# Project Name

This uses AI to create videos for Youtube shorts.
The steps include the following:
- Creates a horror story using OpenAI
- Create Text2Speech using OpenAI speech API
- Creates images using Stable Diffusion locally
- Uses RESRGAN to upscale the images locally
- Generates Subtitles using VOSK locally
- Puts everything togther using MoviePy
- Uses ffmpeg to speed up the video to keep it within 1 min
- Adds a BGM track using ffmpeg 


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

This project runs on Windows with a Nvidia GPU with CUDA installed

Create a virtual environment and install all the requirements

```python
python -m venv .venv
pip install -r requirements. txt

```
Major requirements are Torch, MoviePy, Vosk, OpenAI, Diffusers, ffmpeg, etc

Create a `config.json` file and add your Open AI api key like this.
```
{
    "openai_api_key": "YOUR OPEN AI API KEY HERE"
}
```

## Usage

Open and run `horror_story_maker.py`
It should generate a `input.txt`, that contians a new story.
It will create a new folder in the `Outputs` directory and add all the images, speech, srt files, and final videos.

The generated videos:
output.mp4 --> Output from MoviePy
output_spedup.mp4 --> Video spedup to fit within 60 seconds
output_final.mp4 --> Video with BGM added. Upload this to Youtube Shorts

## TODO
Create a youtube uploader script to automatically upload the videos to Youtube
