#!/bin/bash

# Extract music_dir from config.json
music_dir=$(jq -r '.path' config.json)
music_dir=$(echo $music_dir | envsubst)
playlist_file="playlist.m3u"
rm -f "$playlist_file"
touch "$playlist_file"
formats=$(jq -r '.formats[]' config.json)
for format in $formats; do
    find "$music_dir" -name "*.$format" >> "$playlist_file"
done
