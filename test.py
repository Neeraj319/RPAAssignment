from moviepy.editor import VideoFileClip
import sys

clip = VideoFileClip(sys.argv[1])
print(clip.duration)
