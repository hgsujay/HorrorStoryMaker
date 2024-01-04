import ffmpeg
import os
import shutil


def speedup_video(input_video_path, output_video_path, desired_length):
    input = ffmpeg.input(input_video_path)
    # get current length of video
    current_len = float(ffmpeg.probe(input_video_path)['format']['duration'])
    speed = current_len / desired_length
    if speed > 1:
        # speed up video
        input = ffmpeg.input(input_video_path)
        a = input.audio.filter('atempo', speed)
        v = input.video.filter('setpts', f'PTS/{speed}')
        joined = ffmpeg.concat(v, a, v=1, a=1).node
        output = ffmpeg.output(joined[0], joined[1], output_video_path)
        ffmpeg.run(output, overwrite_output=True)
    else:
        speed = 1.2
        # copy video and rename it
        # os.system("cp " + input_video_path + " " + output_video_path)
        # shutil.copyfile(input_video_path, output_video_path)
        # speed up video
        input = ffmpeg.input(input_video_path)
        a = input.audio.filter('atempo', speed)
        v = input.video.filter('setpts', f'PTS/{speed}')
        joined = ffmpeg.concat(v, a, v=1, a=1).node
        output = ffmpeg.output(joined[0], joined[1], output_video_path)
        ffmpeg.run(output, overwrite_output=True)


def add_bgm(input_video, bgm, output_video_path):
    os.system("ffmpeg -y -i " + input_video + " -i " + bgm +
              ' -filter_complex "[1:a]volume=0.2[a1];[0:a][a1]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy ' +
              output_video_path)


# speedup_video("Outputs/18b5qog/output.mp4", "Outputs/18b5qog/thread_18b5qog_spedup.mp4", 59)
# ffmpeg.probe("Outputs/18azj40/output.mp4").get('duration')
# input = ffmpeg.probe(os.getcwd() + "/Outputs/18azj40/output.mp4")
# print(input['format']['duration'])

# add_bgm("Outputs/18b5qog/thread_18b5qog_spedup.mp4", "bgm/bgm.m4a", "Outputs/18b5qog/thread_18b5qog_spedup_bgm.mp4")
