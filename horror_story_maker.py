import time
import json
import shutil
from compose_story import compose_story
from story import Story
from movie_maker import make_horror_movie
from ffmpeg_utils import add_bgm, speedup_video
# from youtube_uploader import upload_to_youtube


config = json.load(open("config.json"))
start_time = time.time()
compose_story()
story = Story()
output_video_path = make_horror_movie(story, config["video_width"], config["video_height"], config["video_fps"])
# output_video_path = "Outputs/2024_01_02_10_23_54/Output.mp4"
speedup_video_path = output_video_path[:-4] + "_spedup.mp4"
speedup_video(output_video_path, speedup_video_path, 59)
final_video_path = output_video_path[:-4] + "_final.mp4"
add_bgm(speedup_video_path, "bgm/bgm.m4a", final_video_path)
end_time = time.time()
total_time = end_time - start_time
print("Total time taken: ", total_time)


# Fetch the title from the input file
with open("input.txt", 'r') as file:
    text = file.read()
    paragraphs = text.strip().split('\n\n')
    title = paragraphs[0]

# move the story file to the output folder
shutil.move("input.txt", "Outputs/" +
            story.id +
            "/input.txt")

# upload the video to youtube
# upload_to_youtube(final_video_path, title)
