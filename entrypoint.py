import subprocess


def parse_timestamp_file(file):
    timestamps = []
    f = open(file, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        timestamps.append({'timestamp': to_hours(line)})
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


def cut_video(timestamps):
    i = 0
    while i < len(timestamps):
        start_time = timestamps[i]['timestamp']
        end_time = timestamps[i+1]['timestamp']
        output = f"output/{i+1}.mp4"
        subprocess.run(
            ['ffmpeg', '-i', 'input/video.mp4', '-ss', start_time, '-t', end_time, '-async', '1', '-c', 'copy', output])
        i = i + 1


def main():
    times = parse_timestamp_file('input/timestamps2.txt')
    cut_video(times)


if __name__ == "__main__":
    main()
