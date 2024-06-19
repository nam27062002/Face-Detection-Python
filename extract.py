import cv2
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

class FrameExtractor:
    def __init__(self, video_path, output_folder, second_interval=1, max_workers=5):
        self.video_path = video_path
        self.output_folder = output_folder
        self.second_interval = second_interval
        self.max_workers = max_workers
        self.clear_cache()

    def clear_cache(self):
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)

    def extract_frame(self, frame_index):
        video_capture = cv2.VideoCapture(self.video_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_number = int(fps * self.second_interval * frame_index)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, image = video_capture.read()
        if success:
            frame_filename = os.path.join(self.output_folder, f"{frame_index}.jpg")
            cv2.imwrite(frame_filename, image)
        video_capture.release()

    def extract_frames(self):
        video_capture = cv2.VideoCapture(self.video_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        video_capture.release()
        total_frames_to_extract = int(duration / self.second_interval)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.extract_frame, range(total_frames_to_extract))