from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import pyttsx3



def make_video(thought):
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

    def add_audio_to_video(video_path, audio_path, output_path):
        # Load video clip
        video_clip = VideoFileClip(video_path)

        # Load audio clips
        video_audio_clip = video_clip.audio
        new_audio_clip = AudioFileClip(audio_path)

        # Set the duration of the video and audio clips
        video_duration = video_clip.duration
        new_duration = new_audio_clip.duration

        # Trim the video and audio clips to match the duration of the new audio
        video_clip = video_clip.subclip(0, min(video_duration, new_duration))
        video_audio_clip = video_audio_clip.subclip(0, min(video_duration, new_duration))
        new_audio_clip = new_audio_clip.subclip(0, min(video_duration, new_duration))

        # Combine the existing audio and new audio
        final_audio_clip = CompositeAudioClip([video_audio_clip, new_audio_clip])

        # Set the combined audio to the video clip
        video_clip = video_clip.set_audio(final_audio_clip)

        # Write the video clip with the combined audio to a new file
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Close the clips
        video_clip.close()
        video_audio_clip.close()
        new_audio_clip.close()
        final_audio_clip.close()

    # Path to the text file and output audio file

    print(thought)
    output_audio = "sound.mp3"

    # Call the function to generate the audio
    generate_audio(thought, output_audio)

    # Paths to the input video, audio, and output video
    input_video = "base.mp4"
    input_audio = "sound.mp3"
    middleman = "middle.mp4"
    output_video = "final.mp4"
    input_music = "music.mp3"

    # Call the function to add audio to the video
    add_audio_to_video(input_video, input_audio, middleman)
    add_audio_to_video(middleman, input_music, output_video)