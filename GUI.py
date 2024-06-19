import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import uic
from concurrent.futures import ThreadPoolExecutor, as_completed
from model import ImageClassifier
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db


Ui_MainWindow, QtBaseClass = uic.loadUiType("ui_1.ui")
def convert_seconds_to_hms(s):
    hours = s // 3600
    s %= 3600
    minutes = s // 60
    seconds = s % 60
    return f"{hours} giờ, {minutes} phút, {seconds} giây"

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    result = pyqtSignal(list)

    def __init__(self, directory, classifier):
        super().__init__()
        self.directory = directory
        self.classifier = classifier
        self.nums = 0

    def run(self):
        ans = []
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        total_files = len(files)
        self.nums = total_files
        count = 0
        for file in files:
            class_name, _ = self.classifier.predict(os.path.join(self.directory, file))
            class_name = int(class_name)
            if class_name == 1:
                ans.append(file)
            count += 1
            self.progress.emit(round(count / total_files * 100))
        self.result.emit(ans)
        self.finished.emit()


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openFileDialog)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_3.clicked.connect(self.save)
        self.label_4.setText("")
        self.label_3.setText("")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.thread = None
        self.worker = None
        self.time_start = ''
        self.time_end = ''

    def openFileDialog(self):
        options = QFileDialog.Options()
        filter = "Image files (*.png *.jpg)"
        files, _ = QFileDialog.getOpenFileNames(self, "Chọn hình ảnh đối tượng", "", filter, options=options)
        if files:
            self.label_3.setText(f"Đã chọn {len(files)} ảnh")

    def start(self):
        directory = 'Assets/Cache/'
        classifier = ImageClassifier("keras_Model.h5", "labels.txt")

        self.thread = QThread()
        self.worker = Worker(directory, classifier)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.handle_finished)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.handle_result)

        self.thread.start()

    def save(self):
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://face-detector-aff83-default-rtdb.firebaseio.com/'
        })
        ref = db.reference('/')
        json_data = {
            'video': 'video_1',
            'Độ dài video': '6910.87s',
            'Số lượng hình ảnh đối tượng': "273",
            'Thời gian bắt đầu': "0 giờ, 57 phút, 35 giây",
            'Thời gian kết thúc': "0 giờ, 57 phút, 44 giây",
            'Địa điểm': self.lineEdit_3.text(),
            'Ghi chú': self.lineEdit_4.text()
        }
        ref.update(json_data)
        print("Data added to Realtime Database successfully!")
    def handle_finished(self):
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        self.worker = None

    def update_progress(self, value):
        self.label_4.setText(f"{value}%")

    def handle_result(self, result):
        numbers = []
        for file_name in result:
            number_part = file_name.split('_')[0]
            try:
                number = int(number_part)
                numbers.append(number)
            except ValueError:
                pass
        numbers.sort()
        if numbers:
            self.lineEdit.setText(convert_seconds_to_hms(numbers[0]))
            self.lineEdit_2.setText(convert_seconds_to_hms(numbers[-1]))
            self.time_start = convert_seconds_to_hms(numbers[0])
            self.time_end = convert_seconds_to_hms(numbers[-1])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
