from pathlib import Path
from datetime import datetime

import cv2


class TimelapseService:

    def __init__(self):

        # ==================================================
        # PROJE KLASÖRÜ
        # ==================================================

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        # ==================================================
        # ANA KLASÖRLER
        # ==================================================

        self.image_dir = (
            self.project_root / "images"
        )

        self.video_dir = (
            self.project_root / "videos"
        )

        self.image_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.video_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # KAMERA FOTOĞRAF KLASÖRÜ
    # ==================================================

    def get_camera_image_dir(
        self,
        camera_id
    ):

        camera_dir = (
            self.image_dir
            / f"camera_{camera_id}"
        )

        camera_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        return camera_dir

    # ==================================================
    # KAMERA VİDEO KLASÖRÜ
    # ==================================================

    def get_camera_video_dir(
        self,
        camera_id
    ):

        camera_dir = (
            self.video_dir
            / f"camera_{camera_id}"
        )

        camera_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        return camera_dir

    # ==================================================
    # TIME-LAPSE OLUŞTUR
    # ==================================================

    def create_timelapse(
        self,
        camera_id=0,
        fps=2
    ):

        # ==================================================
        # KAMERANIN FOTOĞRAFLARINI AL
        # ==================================================

        image_dir = (
            self.get_camera_image_dir(
                camera_id
            )
        )

        images = sorted(
            image_dir.glob("*.jpg")
        )

        # En az 2 fotoğraf gerekli
        if len(images) < 2:

            return None

        # ==================================================
        # İLK GÖRÜNTÜYÜ OKU
        # ==================================================

        first_image = cv2.imread(
            str(images[0])
        )

        if first_image is None:

            return None

        height, width = (
            first_image.shape[:2]
        )

        # ==================================================
        # VİDEO DOSYA YOLU
        # ==================================================

        timestamp = (
            datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
        )

        video_dir = (
            self.get_camera_video_dir(
                camera_id
            )
        )

        video_path = (
            video_dir
            / f"timelapse_cam{camera_id}_{timestamp}.mp4"
        )

        # ==================================================
        # MP4 CODEC
        # ==================================================

        fourcc = (
            cv2.VideoWriter_fourcc(
                *"mp4v"
            )
        )

        video = cv2.VideoWriter(
            str(video_path),
            fourcc,
            fps,
            (width, height)
        )

        if not video.isOpened():

            return None

        # ==================================================
        # FOTOĞRAFLARI VİDEOYA EKLE
        # ==================================================

        for image_path in images:

            frame = cv2.imread(
                str(image_path)
            )

            if frame is None:

                continue

            # Boyutlar farklıysa düzelt
            if (
                frame.shape[1] != width
                or frame.shape[0] != height
            ):

                frame = cv2.resize(
                    frame,
                    (width, height)
                )

            video.write(
                frame
            )

        # ==================================================
        # VİDEOYU KAPAT
        # ==================================================

        video.release()

        # Dosyanın gerçekten oluşturulduğunu kontrol et
        if not video_path.exists():

            return None

        return str(
            video_path
        )

    # ==================================================
    # VİDEO SAYISI
    # ==================================================

    def get_video_count(
        self,
        camera_id=None
    ):

        # ==================================================
        # BELİRLİ KAMERA
        # ==================================================

        if camera_id is not None:

            video_dir = (
                self.get_camera_video_dir(
                    camera_id
                )
            )

            return len(
                list(
                    video_dir.glob("*.mp4")
                )
            )

        # ==================================================
        # TÜM KAMERALAR
        # ==================================================

        total = 0

        camera_dirs = (
            self.video_dir.glob(
                "camera_*"
            )
        )

        for camera_dir in camera_dirs:

            if not camera_dir.is_dir():

                continue

            total += len(
                list(
                    camera_dir.glob("*.mp4")
                )
            )

        return total