import subprocess

def get_track():
    try:
        out = subprocess.check_output(["cmus-remote", "-Q"], text=True, stderr=subprocess.DEVNULL)
    except:
        return None, None, 0, 0

    artist = None
    title = None
    duration = 0
    position = 0

    for line in out.splitlines():
        if line.startswith("tag artist"):
            artist = line.split(" ", 2)[2]
        elif line.startswith("tag title"):
            title = line.split(" ", 2)[2]
        elif line.startswith("duration "):
            try:
                duration = float(line.split(" ", 1)[1])
            except:
                pass
        elif line.startswith("position "):
            try:
                position = float(line.split(" ", 1)[1])
            except:
                pass

    return artist, title, position, duration
