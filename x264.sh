#!/bin/bash

for I in {1..100}
do
    if [ $I -eq 1 ]
    then
        export INFILE=oceans.mp4
    else
        export INFILE=output/x264/x264-$(expr $I - 1).mp4
    fi

    printf "$I:\n"
    time ffmpeg -hide_banner -loglevel error -i $INFILE -c:v libx264 -c:a copy output/x264/x264-$I.mp4 >> x264.time
    printf "Done\n\n"
done
