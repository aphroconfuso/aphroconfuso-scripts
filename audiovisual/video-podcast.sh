#!/bin/bash

# Usage:
# ./makepodcast.sh audio.mp3 image.jpg "My Podcast Title\nEpisode 1" "/path/to/font.ttf" logo.png
# outro.mp4 is optional, will be appended with 2s crossfade if present.

AUDIO="$1"
IMAGE="$2"
TEXT="$3"
FONT="$4"
LOGO="$5"

PODCAST="podcast.mp4"
FINAL="output.mp4"

# Step 1. Make the base podcast video with waveform, text, and logo
ffmpeg -y -i "$AUDIO" -loop 1 -i "$IMAGE" -i "$LOGO" \
-filter_complex "[0:a]showwaves=s=1280x200:mode=line:rate=25:colors=white[sw]; \
[1:v][sw]overlay=(W-w)/2:H-h-50[tmp]; \
[tmp][2:v]overlay=W-w-20:20,drawtext=fontfile='$FONT':text='$TEXT':x=50:y=50:fontsize=48:fontcolor=white:line_spacing=10" \
-c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest "$PODCAST"

# Step 2. Append outro if it exists
if [ -f outro.mp4 ]; then
  echo "🎬 Adding outro with crossfade..."
  ffmpeg -y -i "$PODCAST" -i outro.mp4 -filter_complex "\
  [0:v]format=yuv420p, setpts=PTS-STARTPTS[v0]; \
  [1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p,setpts=PTS-STARTPTS+T/TB[v1]; \
  [v0][v1]xfade=transition=fade:duration=2:offset=END-2[v]; \
  [0:a]aresample=async=1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -c:a aac -shortest "$FINAL"
else
  echo "ℹ️ No outro.mp4 found — keeping podcast only."
  mv "$PODCAST" "$FINAL"
fi

echo "✅ Done! Created $FINAL"
