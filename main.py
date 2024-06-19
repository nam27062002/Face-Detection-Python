from extract import FrameExtractor
from face_detector import FaceExtractor
from model import ImageClassifier
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from Firebase import FirebaseStorageManager

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

def classify_image(file, classifier, directory):
    global ans
    class_name, _ = classifier.predict(f"{directory}/{file}")
    class_name = int(class_name)
    if class_name == 1:
        ans.append(file)


def convert_seconds_to_hms(s):
    hours = s // 3600
    s %= 3600
    minutes = s // 60
    seconds = s % 60
    return f"{hours} giờ, {minutes} phút, {seconds} giây"


if "__main__" == __name__:

    # # extract video
    # start_time = time.time()
    # video_path = 'video.mp4'
    # output_folder = 'Assets/Extract'
    # second_interval = 1
    # extractor = FrameExtractor(video_path, output_folder, second_interval)
    # extractor.extract_frames()
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Thời gian thực hiện extract video: {execution_time} giây")
    #
    # # face detector
    # start_time = time.time()
    # face_extractor = FaceExtractor()
    # face_extractor.process_images()
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Thời gian thực hiện face detector: {execution_time} giây")

    # matching
    directory = 'Assets/Cache/'
    classifier = ImageClassifier("keras_Model.h5", "labels.txt")
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # ans = []
    # with ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(classify_image, file, classifier, directory) for file in files]
    #     for future in as_completed(futures):
    #         future.result()
    #
    # numbers = []
    # for file_name in ans:
    #     number_part = file_name.split('_')[0]
    #     try:
    #         number = int(number_part)
    #         numbers.append(number)
    #     except ValueError:
    #         pass
    # numbers.sort()
    # print(numbers)
    # print(f"Thời gian xuất hiện đối tượng: {convert_seconds_to_hms(numbers[0])}")
    # print(f"Thời gian kết thúc đối tượng: {convert_seconds_to_hms(numbers[-1])}")




