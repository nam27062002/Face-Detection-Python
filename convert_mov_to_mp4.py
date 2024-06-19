import moviepy.editor as mp


def convert_mov_to_mp4(mov_file, mp4_file):
    clip = mp.VideoFileClip(mov_file)
    clip.write_videofile(mp4_file)


convert_mov_to_mp4("Videos/IMG_3536(5).mov", "Videos/video_7.mp4")


print("input.mov was successfully converted to .mp4 and saved as video_2.mp4")
