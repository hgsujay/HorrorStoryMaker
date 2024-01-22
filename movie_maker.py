from moviepy.editor import ImageClip, AudioFileClip, vfx, CompositeVideoClip, TextClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from subtitle_maker import generate_subtitles_using_vosk, convert_mp3_to_wav
import textwrap
import numpy as np


def generator(txt, width, height):
    # Wrap long lines
    txt = '\n'.join(textwrap.wrap(txt, width=20))
    return TextClip(txt, font='Comic-Sans-MS-Bold', size=(width, height),
                    fontsize=80,
                    color='white',
                    stroke_color="black",
                    stroke_width=4)


def custom_fadein(clip, duration, initial_color=[0, 0, 0]):
    fadein_clip = vfx.fadein(clip, duration, initial_color)
    return fadein_clip.fx(vfx.colorx, 0.3)


def zoom_fx(t):
    # z = 2 - 0.1*(t)
    # return z if z > 0.5 else 0.5
    # return 0.52734375
    return 0.5 + 0.1*np.abs(np.sin(t*0.3))


def make_horror_movie(story, width, height, fps):
    paras = story.paragraphs
    composite_clips = []
    for i in range(len(paras)):
        para = paras[i]
        image_clip = ImageClip(para.image)
        audio_clip = AudioFileClip(para.voiceover)

        clip_img = (
            image_clip
            .resize(zoom_fx)
            .set_position(('center', 'center'))
            .set_duration(audio_clip.duration)
            .set_fps(fps)
            )
        clip = CompositeVideoClip([clip_img], size=(width, height))
        srt_path = "Outputs/"+story.id+"/"+str(para.order)+".srt"

        wav_path = para.voiceover[0:-4]+".wav"
        convert_mp3_to_wav(para.voiceover, wav_path)
        generate_subtitles_using_vosk(wav_path, srt_path, 7)
        # add subtitle track to the video
        gen_lamb = lambda txt: generator(txt, width, height)
        subtitles = SubtitlesClip(srt_path, gen_lamb)
        subtitles = subtitles.set_position(("center"))

        clip = clip.set_audio(audio_clip)
        clip = CompositeVideoClip([clip, subtitles], size=(width, height))
        composite_clips.append(clip)

    final_clip = concatenate_videoclips(composite_clips)
    output_path = "Outputs/"+story.id+"/output.mp4"
    final_clip.write_videofile(output_path, fps=fps)
    return output_path
