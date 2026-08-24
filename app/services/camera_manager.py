from app.services.camera_service import CameraService


class CameraManager:

    def __init__(
        self,
        camera_count=2
    ):

        self.camera_count = camera_count

        self.cameras = {}

        print(
            f"Kamera yöneticisi başlatılıyor. "
            f"Beklenen kamera sayısı: {camera_count}"
        )

        # ==================================================
        # KAMERALARI BAŞLAT
        # ==================================================

        self.initialize_cameras()

    # ==================================================
    # KAMERALARI BAŞLAT
    # ==================================================

    def initialize_cameras(self):

        for camera_id in range(
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
    # KAMERALARIN GERÇEK BAĞLANTI DURUMUNU KONTROL ET
    # ==================================================

    def refresh_connections(self):

        disconnected_cameras = []

        # ==================================================
        # MEVCUT KAMERALARI KONTROL ET
        # ==================================================

        for camera_id, camera in list(
            self.cameras.items()
        ):

            try:

                if not camera.check_connection():

                    print(
                        f"Kamera {camera_id} "
                        "bağlantısı kesildi."
                    )

                    camera.close()

                    disconnected_cameras.append(
                        camera_id
                    )

            except Exception as error:

                print(
                    f"Kamera {camera_id} "
                    f"kontrol hatası: {error}"
                )

                try:

                    camera.close()

                except Exception:

                    pass

                disconnected_cameras.append(
                    camera_id
                )

        # ==================================================
        # BAĞLANTISI KESİLENLERİ SİL
        # ==================================================

        for camera_id in disconnected_cameras:

            self.cameras.pop(
                camera_id,
                None
            )

        # ==================================================
        # EKSİK KAMERALARI YENİDEN ARA
        # ==================================================

        for camera_id in range(
            self.camera_count
        ):

            if camera_id in self.cameras:

                continue

            try:

                print(
                    f"Kamera {camera_id} "
                    "yeniden aranıyor..."
                )

                camera = CameraService(
                    camera_id=camera_id
                )

                if camera.check_connection():

                    self.cameras[camera_id] = camera

                    print(
                        f"Kamera {camera_id} "
                        "yeniden bağlandı."
                    )

                else:

                    camera.close()

            except Exception as error:

                print(
                    f"Kamera {camera_id} "
                    f"yeniden bağlanamadı: {error}"
                )

        return self.get_connected_cameras()

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