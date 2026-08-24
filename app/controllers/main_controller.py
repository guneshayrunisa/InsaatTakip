from PySide6.QtCore import QTimer, QTime
from app.services.timelapse_service import TimelapseService
from app.services.camera_manager import CameraManager
from datetime import datetime, timedelta

class MainController:

    def __init__(
        self,
        model,
        view
    ):

        self.model = model
        self.view = view

        # ==================================================
        # CAMERA MANAGER
        # ==================================================

        self.camera_manager = CameraManager(
            camera_count=2
        )

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

        # OTOMATİK ÇEKİM AYARLARI
        # ==================================================

        self.auto_capture_camera_id = None

        self.auto_capture_interval_seconds = None

        self.next_auto_capture_time = None

    # ==================================================
    # BAŞLAT
    # ==================================================

    def start(self):

        self.connect_signals()

        self.load_initial_data()

        self.check_camera()

        self.restore_auto_capture()

    # ==================================================
    # KAYITLI OTOMATİK ÇEKİMİ GERİ YÜKLE
    # ==================================================

    def restore_auto_capture(self):

        # ==================================================
        # AKTİF DEĞİLSE
        # ==================================================

        if not self.model.auto_capture_enabled:

            return

        # ==================================================
        # GEREKLİ AYARLAR
        # ==================================================

        camera_id = (
            self.model.auto_capture_camera_id
        )

        start_time = (
            self.model.auto_capture_time
        )

        interval_value = (
            self.model.auto_capture_interval_value
        )

        interval_unit = (
            self.model.auto_capture_interval_unit
        )

        if (
            camera_id is None
            or start_time is None
            or interval_value is None
            or interval_unit is None
        ):

            print(
                "Kayıtlı otomatik çekim ayarları eksik."
            )

            self.model.auto_capture_enabled = False

            self.model.save_auto_capture_settings()

            return

        # ==================================================
        # ARALIĞI SANİYEYE ÇEVİR
        # ==================================================

        if interval_unit == "minutes":

            interval_seconds = (
                interval_value * 60
            )

        elif interval_unit == "hours":

            interval_seconds = (
                interval_value * 60 * 60
            )

        elif interval_unit == "days":

            interval_seconds = (
                interval_value * 24 * 60 * 60
            )

        else:

            print(
                "Geçersiz otomatik çekim aralığı."
            )

            return

        # ==================================================
        # CONTROLLER AYARLARI
        # ==================================================

        self.auto_capture_camera_id = (
            camera_id
        )

        self.auto_capture_interval_seconds = (
            interval_seconds
        )

        # ==================================================
        # İLK ÇEKİM ZAMANINI HESAPLA
        # ==================================================

        try:

            hour, minute = map(
                int,
                start_time.split(":")
            )

        except Exception:

            print(
                "Kayıtlı başlangıç saati okunamadı."
            )

            return

        now = datetime.now()

        first_capture = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        # ==================================================
        # BAŞLANGIÇ SAATİ GEÇMİŞSE
        # ==================================================

        if first_capture <= now:

            first_capture += timedelta(
                seconds=interval_seconds
            )

            # Hâlâ geçmişteyse gerekli kadar
            # interval ekle
            while first_capture <= now:

                first_capture += timedelta(
                    seconds=interval_seconds
                )

        self.next_auto_capture_time = (
            first_capture
        )

        # ==================================================
        # TAKVİM ARAYÜZÜNÜ GÜNCELLE
        # ==================================================

        self.view.calendar_view.set_camera_options(
            self.camera_manager
            .get_connected_cameras()
        )

        # Kamera seç
        camera_index = (
            self.view.calendar_view
            .camera_combo
            .findData(camera_id)
        )

        if camera_index >= 0:

            self.view.calendar_view.camera_combo.setCurrentIndex(
                camera_index
            )

        # Saat
        self.view.calendar_view.time_edit.setTime(
            self.view.calendar_view
            .time_edit
            .time()
            .fromString(
                start_time,
                "HH:mm"
            )
        )

        # Interval
        self.view.calendar_view.interval_spin.setValue(
            interval_value
        )

        # Birim
        interval_index = (
            self.view.calendar_view
            .interval_combo
            .findData(
                interval_unit
            )
        )

        if interval_index >= 0:

            self.view.calendar_view.interval_combo.setCurrentIndex(
                interval_index
            )

        # ==================================================
        # BUTON / DURUM
        # ==================================================

        self.view.calendar_view.toggle_button.setText(
            "■  Otomatik Çekimi Durdur"
        )

        self.view.calendar_view.status_label.setText(
            f"Otomatik çekim aktif\n"
            f"Kamera: {camera_id}\n"
            f"Başlangıç: {start_time}\n"
            f"Aralık: {interval_value} "
            f"{self._get_interval_unit_text(interval_unit)}\n"
            f"Sonraki çekim: "
            f"{self.next_auto_capture_time.strftime('%H:%M:%S')}"
        )

        print(
            "Kayıtlı otomatik çekim geri yüklendi."
        )

        print(
            f"Kamera: {camera_id}"
        )

        print(
            f"Başlangıç: {start_time}"
        )

        print(
            f"Aralık: {interval_value} "
            f"{interval_unit}"
        )

        print(
            f"Sonraki çekim: "
            f"{self.next_auto_capture_time}"
        )

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

        self.camera_manager.refresh_connections()

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

        # ==================================================
        # KAMERA SEÇİM LİSTESİNİ GÜNCELLE
        # ==================================================

        self.view.camera_view.set_camera_options(
            connected_cameras
        )

        # ==================================================
        # BAĞLANTI DURUMU
        # ==================================================

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
        # SEÇİLİ KAMERA
        # ==================================================

        camera_id = (
            self.view.camera_view
            .get_selected_camera_id()
        )

        if camera_id is None:

            print(
                "Fotoğraf çekilemedi: "
                "Bağlı kamera bulunamadı."
            )

            return

        # ==================================================
        # FOTOĞRAF ÇEK
        # ==================================================

        result = (
            self.camera_manager.capture_photo(
                camera_id
            )
        )

        if result is None:

            print(
                f"Kamera {camera_id} "
                "fotoğraf çekilemedi."
            )

            return

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
            "fotoğrafı veritabanına kaydedildi:"
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

        # ==================================================
        # KAYITLI FOTOĞRAFLARI OLAN KAMERALARI BUL
        # ==================================================

        available_cameras = (
            self.view.gallery_view
            .get_available_camera_ids()
        )

        # ==================================================
        # GALERİDE KAMERA LİSTESİNİ GÜNCELLE
        # ==================================================

        self.view.gallery_view.set_camera_options(
            available_cameras
        )

        # ==================================================
        # FOTOĞRAFLARI YÜKLE
        # ==================================================

        self.view.gallery_view.load_images()

    # ==================================================
    # TIME-LAPSE SAYFASI
    # ==================================================

    def open_timelapse(self):

        self.view.pages.setCurrentIndex(
            4
        )

        # ==================================================
        # BAĞLI KAMERALARI LİSTELE
        # ==================================================

        connected_cameras = (
            self.camera_manager
            .get_connected_cameras()
        )

        self.view.timelapse_view.set_camera_options(
            connected_cameras
        )

        # ==================================================
        # SEÇİLİ KAMERA
        # ==================================================

        camera_id = (
            self.view.timelapse_view
            .get_selected_camera_id()
        )

        if camera_id is None:

            self.view.timelapse_view.status_label.setText(
                "Bağlı kamera bulunamadı."
            )

            return

        # ==================================================
        # SEÇİLİ KAMERANIN VİDEO SAYISI
        # ==================================================

        count = (
            self.timelapse_service
            .get_video_count(
                camera_id=camera_id
            )
        )

        self.view.timelapse_view.status_label.setText(
            f"Kamera {camera_id} için "
            f"mevcut time-lapse sayısı: {count}"
        )

    # ==================================================
    # TIME-LAPSE OLUŞTUR
    # ==================================================

    def create_timelapse(self):

        # ==================================================
        # SEÇİLİ KAMERA
        # ==================================================

        camera_id = (
            self.view.timelapse_view
            .get_selected_camera_id()
        )

        if camera_id is None:

            self.view.timelapse_view.status_label.setText(
                "Time-lapse oluşturmak için "
                "bağlı bir kamera seçin."
            )

            return

        # ==================================================
        # FPS
        # ==================================================

        fps = (
            self.view.timelapse_view
            .fps_combo.currentData()
        )

        # ==================================================
        # DURUM
        # ==================================================

        self.view.timelapse_view.status_label.setText(
            f"Kamera {camera_id} için "
            "time-lapse oluşturuluyor..."
        )

        # ==================================================
        # TIME-LAPSE OLUŞTUR
        # ==================================================

        result = (
            self.timelapse_service
            .create_timelapse(
                camera_id=camera_id,
                fps=fps
            )
        )

        # ==================================================
        # BAŞARISIZ
        # ==================================================

        if result is None:

            self.view.timelapse_view.status_label.setText(
                f"Kamera {camera_id} için "
                "time-lapse oluşturulamadı.\n\n"
                "En az 2 fotoğraf gerekli."
            )

            return

        # ==================================================
        # SEÇİLİ KAMERANIN VİDEO SAYISI
        # ==================================================

        count = (
            self.timelapse_service
            .get_video_count(
                camera_id=camera_id
            )
        )

        # ==================================================
        # TOPLAM VİDEO SAYISI
        # ==================================================

        self.model.timelapse_count = (
            self.timelapse_service
            .get_video_count()
        )

        # ==================================================
        # DURUMU GÜNCELLE
        # ==================================================

        self.view.timelapse_view.status_label.setText(
            "Time-lapse başarıyla oluşturuldu.\n\n"
            f"Kamera: {camera_id}\n"
            f"Dosya: {result}\n\n"
            f"Bu kameranın toplam videosu: {count}\n"
            f"Tüm kameraların toplam videosu: "
            f"{self.model.timelapse_count}"
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
    # TAKVİM SAYFASI
    # ==================================================

    def open_calendar(self):

        self.view.pages.setCurrentIndex(
            2
        )

        # ==================================================
        # BAĞLI KAMERALARI LİSTELE
        # ==================================================

        connected_cameras = (
            self.camera_manager
            .get_connected_cameras()
        )

        self.view.calendar_view.set_camera_options(
            connected_cameras
        )

        # ==================================================
        # KAYITLI AYARLARI ARAYÜZE YANSIT
        # ==================================================

        if self.model.auto_capture_time:

            selected_time = (
                QTime.fromString(
                    self.model.auto_capture_time,
                    "HH:mm"
                )
            )

            if selected_time.isValid():

                self.view.calendar_view.time_edit.setTime(
                    selected_time
                )

        if self.model.auto_capture_interval_value:

            self.view.calendar_view.interval_spin.setValue(
                self.model.auto_capture_interval_value
            )

        if self.model.auto_capture_interval_unit:

            interval_index = (
                self.view.calendar_view
                .interval_combo
                .findData(
                    self.model.auto_capture_interval_unit
                )
            )

            if interval_index >= 0:

                self.view.calendar_view.interval_combo.setCurrentIndex(
                    interval_index
                )

        if self.model.auto_capture_camera_id is not None:

            camera_index = (
                self.view.calendar_view
                .camera_combo
                .findData(
                    self.model.auto_capture_camera_id
                )
            )

            if camera_index >= 0:

                self.view.calendar_view.camera_combo.setCurrentIndex(
                    camera_index
                )

        # ==================================================
        # DURUM
        # ==================================================

        if self.model.auto_capture_enabled:

            self.view.calendar_view.status_label.setText(
                f"Otomatik çekim aktif\n"
                f"Kamera: "
                f"{self.model.auto_capture_camera_id}\n"
                f"Başlangıç: "
                f"{self.model.auto_capture_time}\n"
                f"Aralık: "
                f"{self.model.auto_capture_interval_value} "
                f"{self._get_interval_unit_text(self.model.auto_capture_interval_unit)}"
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

            self.model.auto_capture_enabled = False

            self.model.auto_capture_time = None

            self.auto_capture_camera_id = None

            self.auto_capture_interval_seconds = None

            self.next_auto_capture_time = None

            self.last_auto_capture_date = None

            self.model.save_auto_capture_settings()

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
        # KAMERA KONTROLÜ
        # ==================================================

        camera_id = (
            self.view.calendar_view
            .get_selected_camera_id()
        )

        if camera_id is None:

            self.view.calendar_view.status_label.setText(
                "Otomatik çekim için "
                "bağlı bir kamera seçin."
            )

            print(
                "Otomatik çekim başlatılamadı: "
                "kamera seçilmedi."
            )

            return

        # ==================================================
        # BAŞLANGIÇ SAATİ
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

        # ==================================================
        # ÇEKİM SIKLIĞI
        # ==================================================

        interval_value = (
            self.view.calendar_view
            .interval_spin.value()
        )

        interval_unit = (
            self.view.calendar_view
            .interval_combo.currentData()
        )

        # ==================================================
        # SANİYEYE ÇEVİR
        # ==================================================

        if interval_unit == "minutes":

            interval_seconds = (
                interval_value * 60
            )

        elif interval_unit == "hours":

            interval_seconds = (
                interval_value * 60 * 60
            )

        elif interval_unit == "days":

            interval_seconds = (
                interval_value * 24 * 60 * 60
            )

        else:

            self.view.calendar_view.status_label.setText(
                "Geçersiz çekim sıklığı."
            )

            return

        # ==================================================
        # AYARLARI KAYDET
        # ==================================================

        self.model.auto_capture_enabled = True

        self.model.auto_capture_time = (
            time_string
        )

        self.model.auto_capture_camera_id = (
            camera_id
        )

        self.model.auto_capture_interval_value = (
            interval_value
        )

        self.model.auto_capture_interval_unit = (
            interval_unit
        )

        self.auto_capture_camera_id = (
            camera_id
        )

        self.auto_capture_interval_seconds = (
            interval_seconds
        )

        self.model.save_auto_capture_settings()

        # ==================================================
        # İLK ÇEKİM ZAMANINI HESAPLA
        # ==================================================

        now = datetime.now()

        first_capture = now.replace(
            hour=selected_time.hour(),
            minute=selected_time.minute(),
            second=0,
            microsecond=0
        )

        # Başlangıç saati geçmişse
        # bir sonraki güne taşı
        if first_capture <= now:

            first_capture += timedelta(
                days=1
            )

        self.next_auto_capture_time = (
            first_capture
        )

        self.last_auto_capture_date = None

        # ==================================================
        # DURUM
        # ==================================================

        self.view.calendar_view.status_label.setText(
            f"Otomatik çekim aktif\n"
            f"Kamera: {camera_id}\n"
            f"Başlangıç: {time_string}\n"
            f"Aralık: {interval_value} "
            f"{self._get_interval_unit_text(interval_unit)}"
        )

        self.view.calendar_view.toggle_button.setText(
            "■  Otomatik Çekimi Durdur"
        )

        print(
            "Otomatik çekim aktif."
        )

        print(
            f"Kamera: {camera_id}"
        )

        print(
            f"Başlangıç: {time_string}"
        )

        print(
            f"Aralık: {interval_value} "
            f"{interval_unit}"
        )

        print(
            f"İlk çekim: "
            f"{self.next_auto_capture_time}"
        )

    def _get_interval_unit_text(
        self,
        interval_unit
    ):

        if interval_unit == "minutes":
            return "dakika"

        if interval_unit == "hours":
            return "saat"

        if interval_unit == "days":
            return "gün"

        return ""

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
        # GEREKLİ AYARLAR VAR MI?
        # ==================================================

        if (
            self.auto_capture_camera_id is None
            or self.auto_capture_interval_seconds is None
            or self.next_auto_capture_time is None
        ):

            return

        # ==================================================
        # ZAMAN KONTROLÜ
        # ==================================================

        now = datetime.now()

        if now < self.next_auto_capture_time:

            return

        # ==================================================
        # SEÇİLİ KAMERADAN FOTOĞRAF ÇEK
        # ==================================================

        camera_id = (
            self.auto_capture_camera_id
        )

        # ==================================================
        # KAMERA BAĞLANTI KONTROLÜ
        # ==================================================

        self.camera_manager.refresh_connections()

        connected_cameras = (
            self.camera_manager
            .get_connected_cameras()
        )

        if camera_id not in connected_cameras:

            self.view.calendar_view.status_label.setText(
                f"Otomatik çekim aktif\n"
                f"Kamera {camera_id}\n"
                f"🔴 Kamera bağlantısı bekleniyor..."
            )

            print(
                f"Otomatik çekim beklemede: "
                f"Kamera {camera_id} bağlı değil."
            )

            return

        # ==================================================
        # KAMERA GERÇEKTEN BAĞLI MI?
        # ==================================================

        connected_cameras = (
            self.camera_manager
            .get_connected_cameras()
        )

        if camera_id not in connected_cameras:

            print(
                f"Otomatik çekim beklemede: "
                f"Kamera {camera_id} bağlı değil."
            )

            self.view.calendar_view.status_label.setText(
                f"Otomatik çekim aktif\n"
                f"Kamera: {camera_id}\n"
                f"Kamera bağlantısı bekleniyor..."
            )

            return

        # ==================================================
        # SEÇİLEN KAMERADAN FOTOĞRAF ÇEK
        # ==================================================

        result = (
            self.camera_manager
            .capture_photo(
                camera_id
            )
        )

        if result is None:

            print(
                f"Otomatik çekim başarısız: "
                f"Kamera {camera_id}"
            )

            # Bir sonraki çekim zamanını yine planla
            self.next_auto_capture_time = (
                now
                + timedelta(
                    seconds=self.auto_capture_interval_seconds
                )
            )

            return

        # ==================================================
        # FOTOĞRAF BİLGİLERİ
        # ==================================================

        timestamp = result["timestamp"]

        image_path = result["path"]

        captured_at = (
            timestamp.strftime(
                "%d.%m.%Y %H:%M:%S"
            )
        )

        # ==================================================
        # DATABASE
        # ==================================================

        photo_id = (
            self.model.database.add_photo(
                file_path=image_path,
                captured_at=captured_at,
                camera_id=camera_id
            )
        )

        print(
            f"Otomatik çekim tamamlandı."
        )

        print(
            f"Kamera: {camera_id}"
        )

        print(
            f"ID: {photo_id}"
        )

        print(
            f"Dosya: {image_path}"
        )

        # ==================================================
        # MODELİ GÜNCELLE
        # ==================================================

        self.model.total_images = (
            self.model.database
            .get_photo_count()
        )

        self.model.last_image_path = (
            image_path
        )

        self.model.last_capture = (
            timestamp.strftime(
                "%d.%m.%Y %H:%M:%S"
            )
        )

        # ==================================================
        # BİR SONRAKİ ÇEKİMİ PLANLA
        # ==================================================

        self.next_auto_capture_time = (
            now
            + timedelta(
                seconds=self.auto_capture_interval_seconds
            )
        )

        # ==================================================
        # ARAYÜZÜ GÜNCELLE
        # ==================================================

        self.view.home_view.update_data(
            total_images=self.model.total_images,
            last_capture=self.model.last_capture,
            timelapse_count=self.model.timelapse_count,
        )

        self.view.home_view.update_image(
            image_path
        )

        # ==================================================
        # DURUM
        # ==================================================

        self.view.calendar_view.status_label.setText(
            f"Otomatik çekim aktif\n"
            f"Kamera: {camera_id}\n"
            f"Son çekim: {captured_at}\n"
            f"Sonraki çekim: "
            f"{self.next_auto_capture_time.strftime('%H:%M:%S')}"
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