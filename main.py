import videomaking
import readdit
import pydub
import youtubeuploading

pydub.AudioSegment.converter = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\ffmpeg.exe"


thoughts = readdit.get_hot_posts()
print(len(thoughts))


videomaking.make_video(thoughts[3])
credentials_file_path = "auth.json"
video_file_path = "final.mp4"
title = "Shower Thoughts #1"
description = "Shower Thoughts #0 like and subscribe for more"
youtubeuploading.upload_video_to_youtube(video_file_path, title, description, credentials_file_path)
