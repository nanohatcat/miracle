import subprocess

def get_track():
    try:
        out = subprocess.check_output(["cmus-remote", "-Q"], text=True)
    except:
        return None, None

    artist = None
    title = None

    for line in out.splitlines():
        if line.startswith("tag artist"):
            artist = line.split(" ", 2)[2]
        elif line.startswith("tag title"):
            title = line.split(" ", 2)[2]

    return artist, title
