from pathlib import Path
from datetime import datetime
from time import sleep

from picamera2 import Picamera2


class CameraService:

    def __init__(
        self,
        camera_id=0
    ):

        # ==================================================
        # KAMERA ID
        # ==================================================

        self.camera_id = camera_id

        # ==================================================
        # PROJE KLASÖRÜ
        # ==================================================

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        # ==================================================
        # FOTOĞRAF KLASÖRÜ
        # ==================================================

        self.image_dir = (
            self.project_root
            / "images"
            / f"camera_{camera_id}"
        )

        self.image_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # KAMERA
        # ==================================================

        self.camera = None

        self.connected = False

        # Kamerayı başlat
        self.initialize_camera()

    # ==================================================
    # KAMERAYI BAŞLAT
    # ==================================================

    def initialize_camera(self):

        try:

            print(
                f"Kamera {self.camera_id} "
                f"başlatılıyor..."
            )

            self.camera = Picamera2(
                self.camera_id
            )

            # ==================================================
            # FOTOĞRAF AYARLARI
            # ==================================================

            config = (
                self.camera
                .create_still_configuration(
                    main={
                        "size": (
                            2304,
                            1296
                        )
                    }
                )
            )

            self.camera.configure(
                config
            )

            # ==================================================
            # KAMERAYI BAŞLAT
            # ==================================================

            self.camera.start()

            # Kameranın hazır olması için bekle
            sleep(2)

            self.connected = True

            print(
                f"Kamera {self.camera_id} hazır."
            )

        except Exception as error:

            self.camera = None

            self.connected = False

            print(
                f"Kamera {self.camera_id} "
                f"başlatılamadı: {error}"
            )

    # ==================================================
    # KAMERA BAĞLANTISI
    # ==================================================

    def check_connection(self):

        if self.camera is not None:

            self.connected = True

        else:

            self.connected = False

        return self.connected

    # ==================================================
    # FOTOĞRAF ÇEK
    # ==================================================

    def capture_photo(self):

        if not self.check_connection():

            print(
                f"Kamera {self.camera_id} "
                f"bağlı değil."
            )

            return None

        try:

            # ==================================================
            # TARİH / SAAT
            # ==================================================

            timestamp = datetime.now()

            filename = (
                timestamp.strftime(
                    "%Y-%m-%d_%H-%M-%S"
                )
                + f"_cam{self.camera_id}.jpg"
            )

            image_path = (
                self.image_dir
                / filename
            )

            # ==================================================
            # FOTOĞRAF ÇEK
            # ==================================================

            print(
                f"Kamera {self.camera_id} "
                f"fotoğraf çekiyor..."
            )

            self.camera.capture_file(
                str(image_path)
            )

            # ==================================================
            # DOSYA KONTROLÜ
            # ==================================================

            if not image_path.exists():

                print(
                    f"Kamera {self.camera_id}: "
                    "Fotoğraf oluşturulamadı."
                )

                return None

            # ==================================================
            # FOTOĞRAFI BYTE OLARAK OKU
            # ==================================================

            with open(
                image_path,
                "rb"
            ) as file:

                image_data = file.read()

            print(
                f"Kamera {self.camera_id} "
                f"fotoğraf çekildi: "
                f"{image_path}"
            )

            # ==================================================
            # CONTROLLER'A GERİ DÖN
            # ==================================================

            return {
                "camera_id": self.camera_id,
                "path": str(image_path),
                "filename": filename,
                "data": image_data,
                "timestamp": timestamp,
            }

        except Exception as error:

            print(
                f"Kamera {self.camera_id} "
                f"fotoğraf çekme hatası: {error}"
            )

            return None

    # ==================================================
    # KAMERAYI KAPAT
    # ==================================================

    def close(self):

        if self.camera is not None:

            try:

                self.camera.stop()

                self.camera.close()

                print(
                    f"Kamera {self.camera_id} "
                    "kapatıldı."
                )

            except Exception as error:

                print(
                    f"Kamera {self.camera_id} "
                    f"kapatılırken hata: {error}"
                )

            finally:

                self.camera = None

                self.connected = False
