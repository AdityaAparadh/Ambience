# Ambience

Ambience is a Python script for Linux desktops that creates a seamless ambient music experience. It plays ambient music when no other media is detected, automatically fading the music when other media starts playing.

Under the hood, it spawns a VLC subprocess and plays music randomly from your selected directory. When any other media is detected to be playing at more than 0% volume, the music automatically fades to a minimum or pauses playing depending on your preference.
## Prerequisites
1. Python 3 or above 
2. Make sure your system uses PulseAudio server
3. Before using Ambience, ensure you have the following packages installed:
- vlc
- cvlc
- jq
- playerctl
- pacmd
- pactl

You can install these packages using your system's package manager. The last two are installed by default if your system uses PulseAudio server.

## Configuration

Ambience allows users to customize the behavior according to their preferences through the `config.json` file. Here's the default configuration file:

```json
{
    "path": "$HOME/Music/",
    "peak_volume": 0.4,
    "min_volume": 0,
    "formats": ["flac", "mp3", "ogg", "wav", "m4a"],
    "check_interval": 1,
    "fade_duration": 3,
    "fade_steps": 20
}
```

## Usage


1. Clone this repository into a suitable directory:
 ```
git clone https://github.com/AdityaAparadh/Ambience
```

2. Navigate to Ambience directory:
```
cd Ambience
```

3. Adjust `config.json` according to your preferences. Make sure `"path"` points to the directory where your music is stored.

  
4. Run the `main.py` script:
```
python main.py
```
    OR

```
python3 main.py
```
