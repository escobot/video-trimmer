import math
import random

from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def parse_video_timestamps(file, duration):
    """
    Parses the timestamp file and returns list of clip timestamps.
    @:param timestamp file path
    @:param duration of the entire video
    @:returns list of clips
    """
    clips = []

    # set clip start times and titles
    f = open(file, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        start, title = line.split(" ", 1)
        clips.append({
            'start': to_seconds(start),
            'title': title.strip()
        })
    f.close()

    # set clip end times
    i = 0
    while i < len(clips) - 1:
        clips[i]['end'] = clips[i+1]['start']
        i = i + 1
    clips[-1]['end'] = math.floor(duration)

    return clips


def to_seconds(timestamp):
    h, m, s = 0, 0, 0
    t = timestamp.split(":")
    if len(t) == 3:
        h, m, s = t
    else:
        m, s = t
    return int(h) * 3600 + int(m) * 60 + int(s)


def to_hours(timestamp):
    t = timestamp.split(":")
    if len(t) == 2:
        timestamp = "00:" + timestamp
    return timestamp.strip()


def cut_video(timestamps):
    i = 0
    # todo: create tmp directory to store clips
    while i < len(timestamps):
        output = f"output/0{i}.mp4" if i < 10 else f"output/{i}.mp4"
        ffmpeg_extract_subclip("input/15.mp4", timestamps[i]['start'], timestamps[i]['end'], targetname=output)
        i = i + 1


def concatenate_clips():
    paths = next(os.walk('output'))[2]
    clips = []
    for c in paths:
        clips.append(VideoFileClip("output/" + c))
    final = concatenate_videoclips(clips)
    final.write_videofile("final.mp4", fps=60)


def main():
    video = VideoFileClip("input/15.mp4")
    timestamps = parse_video_timestamps('input/timestamps.txt', video.duration)
    cut_video(timestamps)
    concatenate_clips()


if __name__ == "__main__":
    main()
