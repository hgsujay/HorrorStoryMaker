import time
from movie_maker import make_horror_movie
from ffmpeg_utils import add_bgm, speedup_video
from story import Story
from compose_story import compose_story
import json


config = json.load(open("config.json"))
start_time = time.time()
compose_story()
story = Story()
output_video_path = make_horror_movie(story, config["video_width"], config["video_height"], config["video_fps"])
# output_video_path = "Outputs/2024_01_02_10_23_54/Output."
speedup_video_path = output_video_path[:-4] + "_spedup.mp4"
speedup_video(output_video_path, speedup_video_path, 59)
final_video_path = output_video_path[:-4] + "_final.mp4"
add_bgm(speedup_video_path, "bgm/bgm.m4a", final_video_path)
end_time = time.time()
total_time = end_time - start_time
print("Total time taken: ", total_time)
