from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def parse_timestamp_file(file):
    timestamps = []
    f = open(file, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        timestamp, title = line.split(" ", 1)
        timestamps.append({
            'timestamp': to_seconds(timestamp),
            'title': title.strip()
        })
    f.close()
    return timestamps


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


def cut_video(video, timestamps):
    i = 0
    video_dur = video.duration
    # todo: create tmp directory to store clips
    while i < len(timestamps) - 1:
        if i is len(timestamps) - 1:
            start_time = timestamps[i]['timestamp']
            end_time = video_dur
        else:
            start_time = timestamps[i]['timestamp']
            end_time = timestamps[i+1]['timestamp']
        output = f"output/0{i+1}.mp4" if (i + 1) < 10 else f"output/{i+1}.mp4"
        ffmpeg_extract_subclip("input/15.mp4", start_time, end_time, targetname=output)
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
    timestamps = parse_timestamp_file('input/timestamps.txt')
    cut_video(video, timestamps)
    concatenate_clips()


if __name__ == "__main__":
    main()
