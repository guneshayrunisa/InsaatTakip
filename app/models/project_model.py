from app.data.database import Database


class ProjectModel:

    def __init__(self):

        # ==================================================
        # DATABASE
        # ==================================================

        self.database = Database()

        # ==================================================
        # KAMERA
        # ==================================================

        self.camera_connected = False

        # ==================================================
        # OTOMATİK ÇEKİM
        # ==================================================

        self.auto_capture_enabled = False

        self.auto_capture_time = None

        # ==================================================
        # FOTOĞRAF BİLGİLERİ
        # ==================================================

        self.total_images = (
            self.database.get_photo_count()
        )

        self.last_capture = None
        self.last_image_path = None

        # Veritabanındaki son fotoğrafı al
        last_photo = (
            self.database.get_last_photo()
        )

        if last_photo:

            self.last_image_path = (
                last_photo["file_path"]
            )

            self.last_capture = (
                last_photo["captured_at"]
            )

        # ==================================================
        # TIME-LAPSE
        # ==================================================

        self.timelapse_count = 0

    # ==================================================
    # FOTOĞRAF EKLE
    # ==================================================

    def add_photo(
        self,
        file_path,
        captured_at,
        camera_id=0
    ):

        photo_id = (
            self.database.add_photo(
                file_path=file_path,
                captured_at=captured_at,
                camera_id=camera_id
            )
        )

        # Modeldeki toplam sayıyı güncelle
        self.total_images = (
            self.database.get_photo_count()
        )

        # Son fotoğraf bilgilerini güncelle
        self.last_image_path = file_path
        self.last_capture = captured_at

        return photo_id

    # ==================================================
    # FOTOĞRAF SAYISINI YENİLE
    # ==================================================

    def refresh_photo_count(self):

        self.total_images = (
            self.database.get_photo_count()
        )

        return self.total_images

    # ==================================================
    # SON FOTOĞRAFI YENİLE
    # ==================================================

    def refresh_last_photo(self):

        last_photo = (
            self.database.get_last_photo()
        )

        if last_photo:

            self.last_image_path = (
                last_photo["file_path"]
            )

            self.last_capture = (
                last_photo["captured_at"]
            )

        else:

            self.last_image_path = None
            self.last_capture = None

        return last_photo
