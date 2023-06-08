from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, concatenate_videoclips,concatenate, CompositeAudioClip, AudioFileClip
import pyttsx3
import textwrap3
from pydub import AudioSegment
import pydub

pydub.AudioSegment.converter = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\ffmpeg.exe"


def generate_audio(content, output_file):
    # Read the content from the text file
    # Set the language and generate the audio using pyttsx3

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 160)

    print("Rate is", engine.getProperty('rate'))
    # Save the audio to the output file
    engine.save_to_file(content, output_file)
    engine.runAndWait()

    print(f"Audio generated and saved as '{output_file}'.")




def add_text_overlay(video_clip, text, duration, words_per_subtitle=5, fontsize=40, offset=-0.3):
    words = text.split()  # Split the text into individual words
    num_words = len(words)
    num_subtitles = (num_words + words_per_subtitle - 1) // words_per_subtitle  # Calculate the number of subtitles
    subtitle_duration = duration / num_subtitles  # Duration for each subtitle

    text_clips = []  # List to store the TextClip objects for each subtitle

    for i in range(num_subtitles):
        start_index = i * words_per_subtitle
        end_index = min(start_index + words_per_subtitle, num_words)

        subtitle_words = words[start_index:end_index]  # Get the words for the current subtitle
        subtitle_text = ' '.join(subtitle_words)  # Join the words to form the subtitle text

        # Check if the width of the subtitle text exceeds the width of the video
        if TextClip(subtitle_text, fontsize=fontsize).w > video_clip.w:
            # If the width exceeds, split the text into multiple lines
            subtitle_text = '\n'.join(textwrap3.wrap(subtitle_text, width=int(video_clip.w / fontsize)))

        # Calculate the start and end times for each subtitle with an offset
        start_time = i * subtitle_duration - offset
        end_time = (i + 1) * subtitle_duration

        # Create a TextClip for the current subtitle
        subtitle_clip = TextClip(subtitle_text, fontsize=fontsize, color='white', size=video_clip.size)

        # Set the duration of the subtitle clip
        subtitle_clip = subtitle_clip.set_duration(end_time - start_time)

        # Position the subtitle clip at the center of the screen
        subtitle_clip = subtitle_clip.set_position(('center', 'center'))

        # Set the start and end times for the subtitle clip
        subtitle_clip = subtitle_clip.set_start(start_time).set_end(end_time)

        # Append the subtitle clip to the list
        text_clips.append(subtitle_clip)

    # Calculate the end time for the last subtitle clip to match the duration of the video
    last_subtitle_end_time = duration - offset
    last_subtitle_clip = text_clips[-1].set_end(last_subtitle_end_time)

    # Replace the last subtitle clip in the list with the adjusted one
    text_clips[-1] = last_subtitle_clip

    # Concatenate all the subtitle clips into a single TextClip
    text_clip = concatenate_videoclips(text_clips)

    # Overlay the TextClip on the video clip
    video_with_text = CompositeVideoClip([video_clip, text_clip])

    return video_with_text





def add_audio_to_video(video_path, tts_audio_path, output_path, thought):
    # Load video clip
    video_clip = VideoFileClip(video_path)

    # Load audio clips
    video_audio_clip = video_clip.audio
    audio_clip1 = AudioFileClip(tts_audio_path)
    #audio_clip2 = AudioFileClip(music_audio_path)

    # Set the duration of the video and audio clips
    video_duration = video_clip.duration
    new_duration = audio_clip1.duration

    # Trim the video and audio clips to match the duration of the new audio
    video_clip = video_clip.subclip(0, min(video_duration, new_duration))
    video_audio_clip = video_audio_clip.subclip(0, min(video_duration, new_duration))
    audio_clip1 = audio_clip1.subclip(0, new_duration)
    #audio_clip2 = audio_clip2.subclip(0, new_duration)

    # Combine the audio clips
    #new_audio_clip = CompositeAudioClip([audio_clip1, audio_clip2])

    # Combine the existing audio and new audio
    final_audio_clip = CompositeAudioClip([video_audio_clip, audio_clip1])

    # Set the combined audio to the video clip
    video_clip = video_clip.set_audio(final_audio_clip)

    # Add text overlay to the video clip
    video_with_text = add_text_overlay(video_clip, thought, min(video_duration, new_duration))

    # Write the video clip with the combined audio and text overlay to a new file
    video_with_text.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close the clips
    video_clip.close()
    video_audio_clip.close()
    #new_audio_clip.close()
    final_audio_clip.close()


# Path to the text file and output audio file
def make_video(thought , location):

    output_audio = "sound.mp3"

    # Call the function to generate the audio
    generate_audio(thought, output_audio)

    # Paths to the input video, audio, and output video
    input_video = "base.mp4"
    input_audio = "sound.mp3"
    output_video = location
    #input_music = "music.mp3"

    # Call the function to add audio to the video
    add_audio_to_video(input_video, input_audio, output_video, thought)