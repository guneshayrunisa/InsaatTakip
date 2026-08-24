from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
)

from PySide6.QtCore import Qt


class TimelapseView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    # ==================================================
    # ARAYÜZ
    # ==================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            35,
            30,
            35,
            25
        )

        layout.setSpacing(20)

        # --------------------------------------------------
        # BAŞLIK
        # --------------------------------------------------

        title = QLabel(
            "Time-lapse"
        )

        title.setObjectName(
            "page_title"
        )

        subtitle = QLabel(
            "Proje görüntülerinden time-lapse videosu oluşturun."
        )

        subtitle.setObjectName(
            "page_subtitle"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # --------------------------------------------------
        # BİLGİ KARTI
        # --------------------------------------------------

        card = QFrame()

        card.setObjectName(
            "card"
        )

        card_layout = QVBoxLayout(
            card
        )

        info = QLabel(
            "Seçilen kameranın fotoğrafları "
            "kullanılarak video oluşturulur."
        )

        info.setObjectName(
            "info_label"
        )

        card_layout.addWidget(info)

        # --------------------------------------------------
        # AYARLAR
        # --------------------------------------------------

        settings = QHBoxLayout()

        # --------------------------------------------------
        # KAMERA SEÇİMİ
        # --------------------------------------------------

        camera_label = QLabel(
            "Kamera:"
        )

        self.camera_combo = QComboBox()

        settings.addWidget(
            camera_label
        )

        settings.addWidget(
            self.camera_combo
        )

        # --------------------------------------------------
        # FPS SEÇİMİ
        # --------------------------------------------------

        fps_label = QLabel(
            "Video hızı:"
        )

        self.fps_combo = QComboBox()

        self.fps_combo.addItem(
            "1 FPS",
            1
        )

        self.fps_combo.addItem(
            "2 FPS",
            2
        )

        self.fps_combo.addItem(
            "5 FPS",
            5
        )

        self.fps_combo.addItem(
            "10 FPS",
            10
        )

        settings.addWidget(
            fps_label
        )

        settings.addWidget(
            self.fps_combo
        )

        settings.addStretch()

        # --------------------------------------------------
        # TIME-LAPSE OLUŞTUR BUTONU
        # --------------------------------------------------

        self.create_button = QPushButton(
            "▶  Time-lapse Oluştur"
        )

        self.create_button.setObjectName(
            "primary_button"
        )

        self.create_button.setMinimumHeight(
            42
        )

        settings.addWidget(
            self.create_button
        )

        card_layout.addLayout(
            settings
        )

        layout.addWidget(
            card
        )

        # --------------------------------------------------
        # DURUM
        # --------------------------------------------------

        self.status_label = QLabel(
            "Henüz time-lapse oluşturulmadı."
        )

        self.status_label.setObjectName(
            "page_message"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.status_label
        )

        layout.addStretch()

    # ==================================================
    # KAMERA LİSTESİNİ GÜNCELLE
    # ==================================================

    def set_camera_options(
        self,
        camera_ids
    ):

        current_camera = (
            self.camera_combo.currentData()
        )

        self.camera_combo.clear()

        for camera_id in camera_ids:

            self.camera_combo.addItem(
                f"Kamera {camera_id}",
                camera_id
            )

        # Önceki seçim hâlâ mevcutsa onu koru
        if current_camera in camera_ids:

            index = (
                self.camera_combo.findData(
                    current_camera
                )
            )

            if index >= 0:

                self.camera_combo.setCurrentIndex(
                    index
                )

        # Hiç kamera yoksa
        if not camera_ids:

            self.camera_combo.addItem(
                "Kamera bulunamadı",
                None
            )

    # ==================================================
    # SEÇİLİ KAMERA
    # ==================================================

    def get_selected_camera_id(self):

        return (
            self.camera_combo.currentData()
        )