import argparse
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
        clips[i]['end'] = clips[i + 1]['start']
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


def generate_final_video(clips, output):
    random.shuffle(clips)

    f = open(f'{output}.txt', 'w')
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
    video.write_videofile(f"{output}.mp4")


def seconds_to_h_m_s(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d}'


def main(video_file, timestamps_file, output_name):
    """
    @:param video_file path to the mp4 video
    @:param timestamps_file path to timestamps text file
    @:param output_name of the generated video and timestamps
    """
    video = VideoFileClip(video_file)
    timestamps = parse_video_timestamps(timestamps_file, video.duration)
    clips = cut_video(video, timestamps)

    generate_final_video(clips, output_name)


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--video', '-v', action='store', type=str, required=True)
    my_parser.add_argument('--timestamps', '-t', action='store', type=str, required=True)
    my_parser.add_argument('--output', '-o', action='store', type=str, required=True)
    args = my_parser.parse_args()
    main(args.video, args.timestamps, args.output)
