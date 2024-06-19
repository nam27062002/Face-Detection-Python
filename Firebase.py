import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


class FirebaseStorageManager:
    def __init__(self, service_account_path='serviceAccountKey.json', storage_bucket_name='face-detector-aff83.appspot.com'):
        self.cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(self.cred, {
            'storageBucket': storage_bucket_name
        })
        self.bucket = storage.bucket()

    def upload_video(self, local_path, remote_name):
        blob = self.bucket.blob(remote_name)
        blob.upload_from_filename(local_path)
        return blob.public_url

    def upload_videos(self, videos):
        urls = {}
        for local_path, remote_name in videos.items():
            urls[remote_name] = self.upload_video(local_path, remote_name)
        return urls

    def get_video_url(self, remote_name):
        blob = self.bucket.blob(remote_name)
        return blob.public_url

    def delete_video(self, remote_name):
        blob = self.bucket.blob(remote_name)
        blob.delete()

    def list_videos(self, prefix=None):
        blobs = self.bucket.list_blobs(prefix=prefix)
        video_list = [blob.name for blob in blobs]
        return video_list


if __name__ == '__main__':
    manager = FirebaseStorageManager()


    # videos = {
    #     'Videos/video_1.mp4': 'Videos_1.mp4',
    #     'Videos/video_2.mp4': 'Videos_2.mp4',
    #     'Videos/video_3.mp4': 'Videos_3.mp4',
    #     'Videos/video_4.mp4': 'Videos_4.mp4',
    #     'Videos/video_5.mp4': 'Videos_5.mp4',
    #     'Videos/video_6.mp4': 'Videos_6.mp4',
    #     'Videos/video_7.mp4': 'Videos_7.mp4',
    # }
    # urls = manager.upload_videos(videos)
    # for name, url in urls.items():
    #     print(f"Uploaded {name} to {url}")

    video_list = manager.list_videos(prefix="Videos")
