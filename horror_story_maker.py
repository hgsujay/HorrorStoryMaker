import time
import json
import shutil
from compose_story import compose_story
from story import Story
from movie_maker import make_horror_movie
from ffmpeg_utils import add_bgm, speedup_video


config = json.load(open("config.json"))
start_time = time.time()
compose_story()
story = Story()
story_id = story.id

output_video_path = make_horror_movie(story, config["video_width"], config["video_height"], config["video_fps"])
# output_video_path = "Outputs/2024_01_02_10_23_54/Output.mp4"
speedup_video_path = output_video_path[:-4] + "_spedup.mp4"
speedup_video(output_video_path, speedup_video_path, 59)
final_video_path = output_video_path[:-4] + "_final.mp4"
add_bgm(speedup_video_path, "bgm/bgm.m4a", final_video_path)

# move the story file to the output folder
shutil.copyfile("input.json", "Outputs/" + story_id + "/" + "input.json")

end_time = time.time()
total_time = end_time - start_time
print("Total time taken: ", total_time)
