import os
import wave
from vosk import Model, KaldiRecognizer
import json
import time
import sys
import ffmpeg


def generate_subtitles_using_cli(audio_path, srt_path):
    # vosk-transcriber -i .\thread_18azj40.mp3 -t srt -o test.srt
    # set vosk log level to 0 to suppress the output
    os.system("vosk-transcriber -i " + audio_path + " -t srt -o " + srt_path + " -l 0")


def generate_subtitles_using_vosk(wav_path, srt_path, line_length=15):
    wf = wave.open(wav_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    model = Model(lang="en-us")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetPartialWords(True)
    # rec.SetMaxAlternatives(10)
    rec.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass
    results = json.loads(rec.FinalResult())
    print(results)

    # Write the results to the SRT file
    with open(srt_path, 'w') as f:
        srt_text = ""
        srt_end = 0
        srt_start = 0
        count = 1
        for i, res in enumerate(results['result']):
            start = round(res['start'], 3)
            end = round(res['end'], 3)
            text = res['word']
            if srt_text == "":
                srt_start = start
            if len(srt_text) + len(text) < line_length:
                srt_text += text + " "
                srt_end = end
            else:
                srt_text += text + " "
                srt_end = end
                timecode = seconds_to_srt_timeformat(srt_start) + " --> " + seconds_to_srt_timeformat(srt_end)
                f.write(f"{count}\n{timecode}\n{srt_text}\n\n")
                srt_text = ""
                count += 1
        # WRITE THE LAST LINE TO SRT FILE
        if srt_text != "":
            # srt_end = end
            timecode = seconds_to_srt_timeformat(start) + " --> " + seconds_to_srt_timeformat(srt_end)
            f.write(f"{count}\n{timecode}\n{srt_text}\n\n")


def seconds_to_srt_timeformat(seconds):
    # Convert seconds to HH:MM:SS,ms
    # cut off the milliseconds to 3 decimal places
    ms = round(seconds-int(seconds), 3)
    return time.strftime('%H:%M:%S,', time.gmtime(seconds)) + str(ms)[2:]


def convert_mp3_to_wav(mp3_path, wav_path):
    audio_input = ffmpeg.input(mp3_path)
    audio_output = ffmpeg.output(audio_input, wav_path)
    ffmpeg.run(audio_output, overwrite_output=True)
