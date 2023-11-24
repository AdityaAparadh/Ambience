import subprocess
import time
import json
import os

def is_media_playing():
    try:
        result = subprocess.run(['pacmd', 'list-sink-inputs'], capture_output=True, text=True, check=True)
        streams = result.stdout.split('index:')
        for stream in streams:
            if 'state: RUNNING' in stream:
                ignore_stream = False
                for app in config['ignore_apps']:
                    if app.lower() in stream.lower() or 'vlc' in stream.lower():
                        ignore_stream = True
                        break
                if not ignore_stream:
                    player_name = stream.split('application.name = ')[1].split('\n')[0].strip()
                    print("External Media Playing :", player_name)
                    return True
        return False
    except subprocess.CalledProcessError:
        return False

def play_ambient_music():
    global player
    player = subprocess.Popen(['cvlc', 'playlist.m3u', '--random', '--loop', '--gain', str(config['peak_volume'])])

global controller
controller = subprocess.Popen('echo', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def Control(instruction):
    subprocess.run(['playerctl','--player=vlc', instruction])

def Fade(target, interval, steps):
    current_volume = subprocess.check_output(['playerctl', '--player=vlc', 'volume'])
    current_volume = float(current_volume.strip())
    step = (target - current_volume) / steps
    for _ in range(steps):
        current_volume += step
        current_volume = max(0, min(1, current_volume))
        subprocess.run(['playerctl', '--player=vlc', 'volume', str(current_volume)])
        time.sleep(interval/steps)


def main():
    with open('config.json', 'r') as f:
        global config
        config = json.load(f)    
    DELAY = config['check_interval']
    print("DELAY : ", DELAY)
    subprocess.run(['./playlist.sh'], shell=True)

    ambient_music_playing = False
    play_ambient_music()
    while True:
        time.sleep(DELAY)
        os.system("clear")
        media = is_media_playing()
        print("External Media Playing: " + str(media))
        current_volume = subprocess.check_output(['playerctl', '--player=vlc', 'volume'])
        current_volume = float(current_volume.strip())
        formatted_volume = "{:.2f}%".format(current_volume * 100)
        print("Volume : " + str(formatted_volume))
        
        if media and ambient_music_playing:
            Fade(config['min_volume'], config['fade_duration'], config['fade_steps'])
            if(config['min_volume'] == 0):
                Control('pause')
                ambient_music_playing = False
        elif not media :
            Control('play')
            Fade(config['peak_volume'], config['fade_duration'], config['fade_steps'])
            ambient_music_playing = True

if __name__ == "__main__":
        main()
