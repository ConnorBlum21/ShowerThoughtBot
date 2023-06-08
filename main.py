import videomaking
import redditshowerthoughts
import pydub
import basemaker
import imagevideomaker
import redditimages

pydub.AudioSegment.converter = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\ffmpeg.exe"


thoughts = redditimages.get_hot_posts()
print(len(thoughts))

input_video_path = "creepybackground.mp4"
output_video_path = "base.mp4"

i = 0
for thought in thoughts:
    print(thought)
    if ".jpg" in thought or ".png" in thought:
        tiktok_video = basemaker.crop_random_section(input_video_path, output_video_path, duration=120)
        print("TikTok-ready video:", tiktok_video)
        location = r"D:\blumm\Reddit Videos\Cursed Images "+str(i)+".mp4"
        imagevideomaker.overlay_image_on_video(output_video_path,thought,location)
        i += 1

