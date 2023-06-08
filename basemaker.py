import random
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def crop_random_section(video_path, output_path, duration=120):
    # Load the video clip
    video = VideoFileClip(video_path)

    # Get the total duration of the video
    total_duration = video.duration

    # Generate a random start time within the video duration
    start_time = random.uniform(0, total_duration - duration)

    # Define the end time based on the start time and desired duration
    end_time = start_time + duration

    # Generate a random filename for the cropped video
    cropped_output_path = "cropped_video.mp4"

    # Crop the video using ffmpeg_extract_subclip
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=cropped_output_path)

    # Load the cropped video
    cropped_video = VideoFileClip(cropped_output_path)

    # Define the target width and height for the cropped video
    target_width = 540
    target_height = 960

    # Calculate the left and right margins to be cropped
    left_margin = int((cropped_video.size[0] - target_width) / 2)
    right_margin = cropped_video.size[0] - target_width - left_margin

    # Crop the video by removing the left and right edges
    cropped_video = cropped_video.crop(x1=left_margin, x2=cropped_video.size[0] - right_margin)

    # Write the cropped video to the output path
    cropped_video.write_videofile(output_path, codec="libx264")

    # Return the path of the TikTok-ready video
    return output_path
