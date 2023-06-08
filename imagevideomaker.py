from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def overlay_image_on_video(video_path, image_url, output_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Download the image using the provided URL
    image_clip = ImageClip(image_url)

    # Calculate the desired width and height based on 75% of the video's dimensions
    desired_width = int(video_clip.w * 0.75)
    desired_height = int(video_clip.h * 0.75)

    # Resize the image to match the desired width while maintaining aspect ratio
    image_clip = image_clip.resize(width=desired_width)

    # Calculate the x and y coordinates to center the image
    x = int((video_clip.w - image_clip.w) / 2)
    y = int((video_clip.h - image_clip.h) / 2)

    # Set the position and duration of the image clip
    image_clip = image_clip.set_position((x, y)).set_duration(video_clip.duration)

    # Overlay the image clip onto the video clip
    video_with_overlay = CompositeVideoClip([video_clip, image_clip])

    # Write the final video with the overlay to the specified output path
    video_with_overlay.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close the video clips
    video_clip.close()
    image_clip.close()

