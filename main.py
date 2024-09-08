import vlc
import time
import json
import sink
import playlist
import sys
import curses
import signal
import threading

with open('config.json', 'r') as f:
    config = json.load(f)
#Constants
FILE_PATH = 'playlist.m3u'
MAX_VOLUME = config.get('max_volume', 100)
MIN_VOLUME = config.get('min_volume', 0)
FADE_IN_DURATION = config.get('fade_in_duration', 2)
FADE_OUT_DURATION = config.get('fade_out_duration', 2)

user_paused = False
other_media_detected = False

def signal_handler(sig, frame):
    try: 
        print("Exiting gracefully...")
        sys.exit(0)
    except Exception as e :
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def fade_volume(upward, media_player):
    try:
        current_volume = media_player.audio_get_volume()
        if upward:
            for i in range(current_volume, MAX_VOLUME + 1):
                media_player.audio_set_volume(i)
                time.sleep(FADE_IN_DURATION / (MAX_VOLUME - current_volume + 1))
        else:
            for i in range(current_volume, MIN_VOLUME - 1, -1):
                media_player.audio_set_volume(i)
                time.sleep(FADE_OUT_DURATION / (current_volume - MIN_VOLUME + 1))
    except Exception as e:
        print(f"Error in fading volume: {e}")

def other_media_monitor(player, media_player):
    global other_media_detected, user_paused
    while True:
        other_media_detected = sink.other_media_playing()

        if other_media_detected:
            fade_volume(False, media_player)
            if MIN_VOLUME == 0:
                player.pause()
        else:
            if not user_paused:
                player.play()
                fade_volume(True, media_player)

        time.sleep(0.5)  

def main(stdscr):
    global user_paused, other_media_detected, current_title
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)  

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))

    playlist.generate_playlist()

    instance = vlc.Instance()
    media_list = instance.media_list_new([FILE_PATH])
    player = instance.media_list_player_new()
    player.set_media_list(media_list)
    player.play()
    media_player = player.get_media_player()
    media_player.audio_set_volume(MAX_VOLUME)

    current_title= media_player.get_media()
    
    media_monitor_thread = threading.Thread(target=other_media_monitor, args=(player, media_player), daemon=True)
    media_monitor_thread.start()

    while True:
        title = media_player.get_media().get_meta(vlc.Meta.Title)
        stdscr.clear()
        stdscr.addstr(0, 0, "✨ Ambience ✨")
        stdscr.addstr(2, 0, f"🔊 Volume: {media_player.audio_get_volume()}")
        stdscr.addstr(3, 0, f"🎵Status: {'▶️ Playing' if player.is_playing() else '⏸️ Paused'}")

        if other_media_detected:
            stdscr.addstr(5, 0, "🔇 Other media detected, lowering volume...")
        else:
            stdscr.addstr(5, 0, "🔊 No other media detected, resuming playback...")
       
        if(title):
            stdscr.addstr(4, 0, "🎵Playing : "+title)

        stdscr.addstr(7,0, " <- or h  : last track  ")
        stdscr.addstr(8,0, " -> or l  : next track  ")
        stdscr.addstr(9,0, " space  : pause/play track  ")


        key = stdscr.getch()
        if key == ord('q'):
            fade_volume(False, media_player)
            break
        elif key == ord(' '):
            if player.is_playing():
                player.pause()
                user_paused = True
            else:
                player.play()
                user_paused = False
        elif key == curses.KEY_RIGHT or key == ord('l'):
            player.next()
        elif key == curses.KEY_LEFT or key == ord('h'):
            player.previous()

        stdscr.refresh()
        time.sleep(0.1) 

if __name__ == "__main__":
    curses.wrapper(main)
