import glob
import json
import random  

def generate_playlist():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    
    path = config_data['music_directory']
    extensions = config_data['file_extensions']
    
    files = []
    for extension in extensions:
        files.extend(glob.glob(f'{path}/*.{extension}'))
    
    random.shuffle(files)  
    
    with open('playlist.m3u', 'w') as playlist_file:
        for file in files:
            playlist_file.write(f'{file}\n')
    
    print('Playlist generated and shuffled successfully!')
