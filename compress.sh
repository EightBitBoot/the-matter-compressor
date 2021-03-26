#!/bin/bash

if [[ "$#" -ne 2 ]]
then
    echo "Incorrect number of parameters"
    echo "Usage: compress.sh <compression-round> <crf>"
    exit 1
fi

ffmpeg -hide_banner -loglevel error -i static/media/movie.mp4 -c:v libx264 -c:a copy -crf "$2" static/media/new.mp4

if [[ ! -d "static/media/history" ]]
then
    mkdir static/media/history
fi
xz -c static/media/new.mp4 > "static/media/history/compress$1-crf$2.mp4.xz"

mv static/media/new.mp4 static/media/movie.mp4