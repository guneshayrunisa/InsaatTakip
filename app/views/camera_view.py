from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)


class CameraView(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            35,
            30,
            35,
            25
        )

        layout.setSpacing(20)

        # ==========================================
        # BAŞLIK
        # ==========================================

        title = QLabel("Kamera")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Raspberry Pi kamera bağlantısını "
            "ve çekimleri yönetin."
        )

        subtitle.setObjectName("page_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ==========================================
        # KAMERA DURUMU
        # ==========================================

        status_card = QFrame()
        status_card.setObjectName("card")

        status_layout = QHBoxLayout(
            status_card
        )

        camera_icon = QLabel("📷")
        camera_icon.setObjectName(
            "large_icon"
        )

        information = QVBoxLayout()

        camera_title = QLabel(
            "Raspberry Pi Kamera"
        )

        camera_title.setObjectName(
            "card_title"
        )

        self.connection_status = QLabel(
            "● Bağlantı bekleniyor"
        )

        self.connection_status.setObjectName(
            "camera_status"
        )

        information.addWidget(camera_title)
        information.addWidget(
            self.connection_status
        )

        status_layout.addWidget(camera_icon)
        status_layout.addLayout(information)

        status_layout.addItem(
            QSpacerItem(
                40,
                20,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )
        )

        self.check_connection_button = QPushButton(
            "Bağlantıyı Kontrol Et"
        )

        self.check_connection_button.setObjectName(
            "secondary_button"
        )

        self.check_connection_button.setMinimumHeight(
            40
        )

        status_layout.addWidget(
            self.check_connection_button
        )

        layout.addWidget(status_card)

        # ==========================================
        # KAMERA ÖNİZLEME
        # ==========================================

        preview_card = QFrame()
        preview_card.setObjectName("card")

        preview_layout = QVBoxLayout(
            preview_card
        )

        preview_title = QLabel(
            "Kamera Önizleme"
        )

        preview_title.setObjectName(
            "card_title"
        )

        preview_layout.addWidget(
            preview_title
        )

        self.preview = QLabel(
            "📷\n\n"
            "Kamera görüntüsü burada görünecek"
        )

        self.preview.setObjectName(
            "camera_preview"
        )

        self.preview.setMinimumHeight(300)

        preview_layout.addWidget(
            self.preview
        )

        layout.addWidget(preview_card)

        # ==========================================
        # BUTONLAR
        # ==========================================

        buttons = QHBoxLayout()

        self.capture_button = QPushButton(
            "📷  Fotoğraf Çek"
        )

        self.capture_button.setObjectName(
            "primary_button"
        )

        self.capture_button.setMinimumHeight(48)

        self.auto_capture_button = QPushButton(
            "⏱  Otomatik Çekimi Ayarla"
        )

        self.auto_capture_button.setObjectName(
            "secondary_button"
        )

        self.auto_capture_button.setMinimumHeight(
            48
        )

        buttons.addWidget(
            self.capture_button
        )

        buttons.addWidget(
            self.auto_capture_button
        )

        layout.addLayout(buttons)

        # ==========================================
        # BİLGİ
        # ==========================================

        info = QLabel(
            "Çekimler Raspberry Pi üzerinde "
            "kaydedilecektir."
        )

        info.setObjectName("footer")

        layout.addWidget(info)

        layout.addStretch()