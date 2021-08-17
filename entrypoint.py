import math
import random

from moviepy.editor import *


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


def cut_video(video, timestamps):
    clips = []
    for clip in timestamps:
        clips.append({
            'clip': video.subclip(clip['start'], clip['end']),
            'title': clip['title'],
            'duration': clip['end'] - clip['start']
        })
    return clips


def generate_final_video(clips):
    random.shuffle(clips)

    f = open('timestamps.txt', 'w')
    only_clips = []
    duration = 0
    for clip in clips:
        if duration == 0:
            f.write(f'00:00:00 {clip["title"]}\n')
            duration = duration + clip["duration"]
            only_clips.append(clip["clip"])
        else:
            f.write(f'{seconds_to_h_m_s(duration)} {clip["title"]}\n')
            duration = duration + clip["duration"]
            only_clips.append(clip["clip"])
    f.close()

    video = concatenate_videoclips(only_clips)
    video.write_videofile("final.mp4", fps=60)


def seconds_to_h_m_s(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d}'


def main():
    # todo: error handing if timestamps don't match video
    video = VideoFileClip("input/15.mp4")
    timestamps = parse_video_timestamps('input/timestamps.txt', video.duration)
    clips = cut_video(video, timestamps)

    generate_final_video(clips)


if __name__ == "__main__":
    main()
