from app.services.camera_service import CameraService


class CameraManager:

    def __init__(
        self,
        camera_count=2,
        existing_camera=None
    ):

        self.camera_count = camera_count

        self.cameras = {}

        print(
            f"Kamera yöneticisi başlatılıyor. "
            f"Beklenen kamera sayısı: {camera_count}"
        )

        # ==================================================
        # MEVCUT KAMERA
        # ==================================================

        if existing_camera is not None:

            if existing_camera.check_connection():

                self.cameras[0] = existing_camera

                print(
                    "Mevcut kamera Kamera 0 olarak kullanılıyor."
                )

        # ==================================================
        # DİĞER KAMERALARI BAŞLAT
        # ==================================================

        self.initialize_cameras()

    # ==================================================
    # KAMERALARI BAŞLAT
    # ==================================================

    def initialize_cameras(self):

        # Kamera 0 zaten mevcutsa tekrar başlatma.
        # 1'den başlayarak diğer kameraları dene.

        for camera_id in range(
            1,
            self.camera_count
        ):

            try:

                print(
                    f"Kamera {camera_id} başlatılıyor..."
                )

                camera = CameraService(
                    camera_id=camera_id
                )

                if camera.check_connection():

                    self.cameras[camera_id] = camera

                    print(
                        f"Kamera {camera_id} hazır."
                    )

                else:

                    camera.close()

                    print(
                        f"Kamera {camera_id} bağlı değil."
                    )

            except Exception as error:

                print(
                    f"Kamera {camera_id} "
                    f"başlatılamadı: {error}"
                )

    # ==================================================
    # BAĞLI KAMERALAR
    # ==================================================

    def get_connected_cameras(self):

        return list(
            self.cameras.keys()
        )

    # ==================================================
    # KAMERA GETİR
    # ==================================================

    def get_camera(
        self,
        camera_id
    ):

        return self.cameras.get(
            camera_id
        )

    # ==================================================
    # TEK KAMERADAN FOTOĞRAF
    # ==================================================

    def capture_photo(
        self,
        camera_id
    ):

        camera = self.get_camera(
            camera_id
        )

        if camera is None:

            print(
                f"Kamera {camera_id} bağlı değil."
            )

            return None

        return camera.capture_photo()

    # ==================================================
    # TÜM KAMERALARDAN FOTOĞRAF
    # ==================================================

    def capture_all(self):

        results = {}

        for camera_id, camera in (
            self.cameras.items()
        ):

            print(
                f"Kamera {camera_id} "
                f"fotoğraf çekiyor..."
            )

            result = camera.capture_photo()

            if result is not None:

                results[camera_id] = result

        return results

    # ==================================================
    # KAMERALARI KAPAT
    # ==================================================

    def close_all(self):

        for camera_id, camera in (
            self.cameras.items()
        ):

            try:

                camera.close()

            except Exception as error:

                print(
                    f"Kamera {camera_id} "
                    f"kapatılırken hata: {error}"
                )

        self.cameras.clear()
