from pathlib import Path
from datetime import datetime

import cv2


class TimelapseService:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.image_dir = self.project_root / "images"
        self.video_dir = self.project_root / "videos"

        self.image_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)

    # ==================================================
    # TIME-LAPSE OLUŞTUR
    # ==================================================

    def create_timelapse(self, fps=2):

        images = sorted(
            self.image_dir.glob("*.jpg")
        )

        if len(images) < 2:
            return None

        # İlk görüntüyü oku
        first_image = cv2.imread(
            str(images[0])
        )

        if first_image is None:
            return None

        height, width = first_image.shape[:2]

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        video_path = (
            self.video_dir /
            f"timelapse_{timestamp}.mp4"
        )

        # MP4 codec
        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        video = cv2.VideoWriter(
            str(video_path),
            fourcc,
            fps,
            (width, height)
        )

        if not video.isOpened():
            return None

        # Fotoğrafları videoya ekle
        for image_path in images:

            frame = cv2.imread(
                str(image_path)
            )

            if frame is None:
                continue

            # Boyutlar farklıysa düzelt
            frame = cv2.resize(
                frame,
                (width, height)
            )

            video.write(frame)

        video.release()

        return str(video_path)

    # ==================================================
    # VİDEO SAYISI
    # ==================================================

    def get_video_count(self):

        return len(
            list(
                self.video_dir.glob("*.mp4")
            )
        )