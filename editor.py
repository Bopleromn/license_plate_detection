from moviepy.editor import VideoFileClip

# Загрузите видеофайл
video = VideoFileClip("sample.mp4")

#мените длину видео
new_video = video.subclip(0, 5)

# Сохраните новое видео
new_video.write_videofile("new_sample.mp4")

