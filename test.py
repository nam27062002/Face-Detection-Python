import moviepy.editor as mp


def get_video_duration(video_path):
    # Load the video
    clip = mp.VideoFileClip(video_path)

    # Get the duration of the video in seconds
    duration = clip.duration

    return duration


# Replace "video.mp4" with the path to your video file
video_path = "Videos/video_1.mp4"

# Get the duration of the video and print it
duration = get_video_duration(video_path)
print(f"The duration of the video is {duration} seconds.")
