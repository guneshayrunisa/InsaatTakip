from PySide6.QtCore import QTimer

from app.services.timelapse_service import TimelapseService
from app.services.camera_manager import CameraManager
import json
from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from app.services.camera_health_service import CameraHealthService

class MainController:

    def __init__(
        self,
        model,
        view,
        camera_service
    ):

        self.model = model
        self.view = view
        
        # Eski camera service referansı
        self.camera_service = camera_service
        # ==================================================
        # KAMERA SAĞLIK ANALİZİ
        # ==================================================

        self.camera_health_service = (
            CameraHealthService()
        )

        self.camera_reference = None

        self.load_camera_reference()
        # ==================================================
        # CAMERA MANAGER
        # ==================================================

        # Şimdilik 2 kamera destekliyoruz.
        #
        # Fiziksel olarak yalnızca Kamera 0 bağlıysa
        # CameraManager sadece onu kullanacaktır.
        #
        # İkinci kamera bağlandığında Kamera 1 de
        # otomatik olarak kullanılacaktır.

        self.camera_manager = CameraManager(
            camera_count=2,
            existing_camera=camera_service
        )

        # Eski tek kamera servisini artık kullanmıyoruz.
        #
        # main.py tarafından oluşturulduğu için açık
        # kalmasını istemiyoruz.

        if (
            self.camera_service is not None
            and self.camera_service
            not in self.camera_manager.cameras.values()
        ):

            try:

                self.camera_service.close()

            except Exception:

                pass

        # ==================================================
        # TIME-LAPSE SERVİSİ
        # ==================================================

        self.timelapse_service = (
            TimelapseService()
        )

        # ==================================================
        # OTOMATİK ÇEKİM TIMER
        # ==================================================

        self.auto_capture_timer = QTimer()

        self.auto_capture_timer.timeout.connect(
            self.check_auto_capture
        )

        # Her saniye kontrol et
        self.auto_capture_timer.start(1000)

        # Aynı gün içerisinde tekrar çekim yapmamak için
        self.last_auto_capture_date = None

    # ==================================================
    # BAŞLAT
    # ==================================================

    def start(self):

        self.connect_signals()

        self.load_initial_data()

        self.check_camera()

    # ==================================================
    # SİNYALLER
    # ==================================================

    def connect_signals(self):

        # ==================================================
        # ANA SAYFA
        # ==================================================

        self.view.home_button.clicked.connect(
            lambda: self.change_page(0)
        )

        # ==================================================
        # KAMERA
        # ==================================================

        self.view.camera_button.clicked.connect(
            lambda: self.change_page(1)
        )

        # ==================================================
        # TAKVİM
        # ==================================================

        self.view.calendar_button.clicked.connect(
            self.open_calendar
        )

        self.view.calendar_view.toggle_button.clicked.connect(
            self.toggle_auto_capture
        )

        # ==================================================
        # GALERİ
        # ==================================================

        self.view.gallery_button.clicked.connect(
            self.open_gallery
        )

        # ==================================================
        # TIME-LAPSE
        # ==================================================

        self.view.timelapse_button.clicked.connect(
            self.open_timelapse
        )

        self.view.timelapse_view.create_button.clicked.connect(
            self.create_timelapse
        )

        # ==================================================
        # AYARLAR
        # ==================================================

        self.view.settings_button.clicked.connect(
            lambda: self.change_page(5)
        )

        # ==================================================
        # FOTOĞRAF ÇEKME
        # ==================================================

        self.view.home_view.capture_button.clicked.connect(
            self.capture_photo
        )

        self.view.camera_view.capture_button.clicked.connect(
            self.capture_photo
        )

        # ==================================================
        # KAMERA BAĞLANTI KONTROLÜ
        # ==================================================

        self.view.camera_view.check_connection_button.clicked.connect(
            self.check_camera
        )

    # ==================================================
    # İLK VERİLERİ YÜKLE
    # ==================================================

    def load_initial_data(self):

        self.view.home_view.update_data(
            total_images=self.model.total_images,
            last_capture=self.model.last_capture,
            timelapse_count=self.model.timelapse_count,
        )
        self.view.gallery_view.load_images()

        # Uygulama açılırken son fotoğrafı göster
        if self.model.last_image_path:
            self.view.home_view.update_image(
                self.model.last_image_path
            )

    # ==================================================
    # KAMERA REFERANSINI YÜKLE
    # ==================================================

    def load_camera_reference(self):

        reference_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "camera_references"
            / "camera_0_reference.json"
        )

        if not reference_path.exists():

            print(
                "Kamera 0 referans dosyası bulunamadı."
            )

            return

        try:

            with open(
                reference_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.camera_reference = (
                    json.load(file)
                )

            print(
                "Kamera 0 referansı yüklendi."
            )

        except Exception as error:

            self.camera_reference = None

            print(
                f"Kamera referansı yüklenemedi: {error}"
            )

    # ==================================================
    # SAYFA DEĞİŞTİR
    # ==================================================

    def change_page(self, index):

        self.view.pages.setCurrentIndex(
            index
        )

    # ==================================================
    # KAMERA KONTROLÜ
    # ==================================================

    def check_camera(self):

        connected_cameras = (
            self.camera_manager
            .get_connected_cameras()
        )

        connected = (
            len(connected_cameras) > 0
        )

        self.model.camera_connected = (
            connected
        )

        if connected:

            self.view.camera_view.connection_status.setText(
                f"● Kamera bağlı "
                f"({len(connected_cameras)} kamera)"
            )

            print(
                "Bağlı kameralar:",
                connected_cameras
            )

        else:

            self.view.camera_view.connection_status.setText(
                "● Kamera bağlantısı yok"
            )

            print(
                "Bağlı kamera bulunamadı."
            )

    # ==================================================
    # FOTOĞRAF ÇEK
    # ==================================================

    def capture_photo(self):

        # ==================================================
        # ŞİMDİLİK KAMERA 0
        # ==================================================

        result = (
            self.camera_manager.capture_photo(
                0
            )
        )

        if result is None:

            print(
                "Kamera 0'dan fotoğraf çekilemedi."
            )

            return
        # ==================================================
        # KAMERA SAĞLIK ANALİZİ
        # ==================================================

        image_path = result["path"]

        health_result = (
            self.camera_health_service.analyze(
                image_path
            )
        )

        reference_result = None

        if self.camera_reference is not None:

            reference_result = (
                self.camera_health_service
                .compare_with_regional_reference(
                    image_path,
                    self.camera_reference
                )
            )
        # ==================================================
        # KAMERA UYARISI
        # ==================================================

        warning_message = None

        if not health_result["ok"]:

            warning_message = (
                health_result["message"]
            )

        elif (
            reference_result is not None
            and not reference_result["ok"]
        ):

            warning_message = (
                reference_result["message"]
            )

        if warning_message:

            print(
                f"KAMERA UYARISI: "
                f"{warning_message}"
            )

            QMessageBox.warning(
                self.view,
                "Kamera Uyarısı",
                warning_message
            )
        # ==================================================
        # TARİH
        # ==================================================

        captured_at = (
            result["timestamp"].strftime(
                "%d.%m.%Y %H:%M:%S"
            )
        )

        # ==================================================
        # VERİTABANINA KAYDET
        # ==================================================

        self.model.add_photo(
            file_path=result["path"],
            captured_at=captured_at,
            camera_id=result["camera_id"]
        )

        # ==================================================
        # ANA SAYFAYI GÜNCELLE
        # ==================================================

        self.view.home_view.update_data(
            total_images=self.model.total_images,
            last_capture=self.model.last_capture,
            timelapse_count=self.model.timelapse_count,
        )

        # ==================================================
        # SON FOTOĞRAFI GÖSTER
        # ==================================================

        self.view.home_view.update_image(
            result["path"]
        )

        # ==================================================
        # TERMINALE BİLGİ
        # ==================================================

        print(
            f"Kamera {result['camera_id']} "
            f"fotoğrafı veritabanına kaydedildi:"
        )

        print(
            f"Dosya: {result['path']}"
        )

    # ==================================================
    # GALERİ
    # ==================================================

    def open_gallery(self):

        self.view.pages.setCurrentIndex(
            3
        )

        self.view.gallery_view.load_images()

    # ==================================================
    # TIME-LAPSE SAYFASI
    # ==================================================

    def open_timelapse(self):

        self.view.pages.setCurrentIndex(
            4
        )

        count = (
            self.timelapse_service
            .get_video_count()
        )

        self.view.timelapse_view.status_label.setText(
            f"Mevcut time-lapse sayısı: {count}"
        )

    # ==================================================
    # TIME-LAPSE OLUŞTUR
    # ==================================================

    def create_timelapse(self):

        fps = (
            self.view.timelapse_view
            .fps_combo.currentData()
        )

        self.view.timelapse_view.status_label.setText(
            "Time-lapse oluşturuluyor..."
        )

        result = (
            self.timelapse_service
            .create_timelapse(
                fps=fps
            )
        )

        if result is None:

            self.view.timelapse_view.status_label.setText(
                "Time-lapse oluşturulamadı.\n\n"
                "En az 2 fotoğraf gerekli."
            )

            return

        count = (
            self.timelapse_service
            .get_video_count()
        )

        self.model.timelapse_count = (
            count
        )

        self.view.timelapse_view.status_label.setText(
            "Time-lapse başarıyla oluşturuldu.\n\n"
            f"Dosya: {result}\n\n"
            f"Toplam video: {count}"
        )

        self.view.home_view.update_data(
            total_images=self.model.total_images,
            last_capture=self.model.last_capture,
            timelapse_count=self.model.timelapse_count,
        )

    # ==================================================
    # TAKVİM SAYFASI
    # ==================================================

    def open_calendar(self):

        self.view.pages.setCurrentIndex(
            2
        )

        if self.model.auto_capture_enabled:

            self.view.calendar_view.status_label.setText(
                f"Otomatik çekim aktif • "
                f"Saat: "
                f"{self.model.auto_capture_time}"
            )

            self.view.calendar_view.toggle_button.setText(
                "■  Otomatik Çekimi Durdur"
            )

        else:

            self.view.calendar_view.status_label.setText(
                "Otomatik çekim: Pasif"
            )

            self.view.calendar_view.toggle_button.setText(
                "▶  Otomatik Çekimi Aktif Et"
            )

    # ==================================================
    # OTOMATİK ÇEKİMİ AÇ / KAPAT
    # ==================================================

    def toggle_auto_capture(self):

        # ==================================================
        # AKTİFSE KAPAT
        # ==================================================

        if self.model.auto_capture_enabled:

            self.model.auto_capture_enabled = (
                False
            )

            self.model.auto_capture_time = (
                None
            )

            self.last_auto_capture_date = (
                None
            )

            self.view.calendar_view.status_label.setText(
                "Otomatik çekim: Pasif"
            )

            self.view.calendar_view.toggle_button.setText(
                "▶  Otomatik Çekimi Aktif Et"
            )

            print(
                "Otomatik çekim kapatıldı."
            )

            return

        # ==================================================
        # AKTİF ET
        # ==================================================

        selected_time = (
            self.view.calendar_view
            .time_edit.time()
        )

        time_string = (
            selected_time.toString(
                "HH:mm"
            )
        )

        self.model.auto_capture_enabled = (
            True
        )

        self.model.auto_capture_time = (
            time_string
        )

        self.last_auto_capture_date = (
            None
        )

        self.view.calendar_view.status_label.setText(
            f"Otomatik çekim aktif • "
            f"Her gün {time_string}"
        )

        self.view.calendar_view.toggle_button.setText(
            "■  Otomatik Çekimi Durdur"
        )

        print(
            f"Otomatik çekim aktif: "
            f"{time_string}"
        )

    # ==================================================
    # OTOMATİK ÇEKİM KONTROLÜ
    # ==================================================

    def check_auto_capture(self):

        # ==================================================
        # OTOMATİK ÇEKİM AKTİF Mİ?
        # ==================================================

        if not self.model.auto_capture_enabled:

            return

        # ==================================================
        # SAAT BELİRLENMİŞ Mİ?
        # ==================================================

        if not self.model.auto_capture_time:

            return

        from datetime import datetime

        now = datetime.now()

        current_time = (
            now.strftime(
                "%H:%M"
            )
        )

        current_date = (
            now.strftime(
                "%Y-%m-%d"
            )
        )

        # ==================================================
        # SAAT KONTROLÜ
        # ==================================================

        if (
            current_time
            != self.model.auto_capture_time
        ):

            return

        # ==================================================
        # BUGÜN ZATEN ÇEKİLDİ Mİ?
        # ==================================================

        if (
            self.last_auto_capture_date
            == current_date
        ):

            return

        # ==================================================
        # TÜM BAĞLI KAMERALARDAN FOTOĞRAF ÇEK
        # ==================================================

        results = (
            self.camera_manager
            .capture_all()
        )

        if not results:

            print(
                "Hiçbir kameradan fotoğraf çekilemedi."
            )

            return

        # ==================================================
        # HER KAMERANIN FOTOĞRAFINI KAYDET
        # ==================================================

        last_result = None

        for camera_id, result in (
            results.items()
        ):

            timestamp = (
                result["timestamp"]
            )

            image_path = (
                result["path"]
            )

            captured_at = (
                timestamp.strftime(
                    "%d.%m.%Y %H:%M:%S"
                )
            )

            # ----------------------------------------------
            # DATABASE
            # ----------------------------------------------

            photo_id = (
                self.model.database.add_photo(
                    file_path=image_path,
                    captured_at=captured_at,
                    camera_id=camera_id
                )
            )

            print(
                f"Kamera {camera_id} "
                f"fotoğrafı veritabanına kaydedildi."
            )

            print(
                f"ID: {photo_id}"
            )

            print(
                f"Dosya: {image_path}"
            )

            # Son çekilen sonucu sakla
            last_result = result

        # ==================================================
        # BUGÜN ÇEKİLDİ OLARAK İŞARETLE
        # ==================================================

        self.last_auto_capture_date = (
            current_date
        )

        # ==================================================
        # MODELİ GÜNCELLE
        # ==================================================

        self.model.total_images = (
            self.model.database
            .get_photo_count()
        )

        if last_result is not None:

            self.model.last_image_path = (
                last_result["path"]
            )

            self.model.last_capture = (
                last_result["timestamp"]
                .strftime(
                    "%d.%m.%Y %H:%M:%S"
                )
            )

        # ==================================================
        # ANA SAYFAYI GÜNCELLE
        # ==================================================

        self.view.home_view.update_data(
            total_images=self.model.total_images,
            last_capture=self.model.last_capture,
            timelapse_count=self.model.timelapse_count,
        )

        # ==================================================
        # SON FOTOĞRAFI GÖSTER
        # ==================================================

        if last_result is not None:

            self.view.home_view.update_image(
                last_result["path"]
            )

        print(
            "Otomatik çekim tamamlandı."
        )

    # ==================================================
    # KAPAT
    # ==================================================

    def close(self):

        try:

            self.auto_capture_timer.stop()

        except Exception:

            pass

        try:

            self.camera_manager.close_all()

        except Exception:

            pass
