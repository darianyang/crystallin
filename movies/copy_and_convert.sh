#!/bin/bash
# copy over movies and convert from mp4 to mov
# put name of file without .x format

NAME=$1

# copy
scp dty7@h2p.crc.pitt.edu:~/crystallin-movie/$NAME.mp4 .

# convert
ffmpeg -i $NAME.mp4 -vcodec mpeg4 -q:v 1 $NAME.mov &&

# remove mp4
rm -v $NAME.mp4
