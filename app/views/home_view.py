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

from PySide6.QtCore import Qt

from PySide6.QtGui import QPixmap


class HomeView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    # ==================================================
    # ARAYÜZÜ OLUŞTUR
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

        # ==================================================
        # ÜST BAŞLIK
        # ==================================================

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel(
            "İnşaat Projesi"
        )

        title.setObjectName(
            "page_title"
        )

        subtitle = QLabel(
            "Proje durumunu ve kamera kayıtlarını takip edin."
        )

        subtitle.setObjectName(
            "page_subtitle"
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header.addLayout(
            title_layout
        )

        header.addItem(
            QSpacerItem(
                40,
                20,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )
        )

        self.status = QLabel(
            "●  Sistem Hazır"
        )

        self.status.setObjectName(
            "status"
        )

        header.addWidget(
            self.status
        )

        layout.addLayout(
            header
        )

        # ==================================================
        # İSTATİSTİK KARTLARI
        # ==================================================

        stats_layout = QHBoxLayout()

        stats_layout.setSpacing(
            15
        )

        self.total_images_card = (
            self.create_stat_card(
                "TOPLAM GÖRÜNTÜ",
                "0",
                "📷"
            )
        )

        self.last_capture_card = (
            self.create_stat_card(
                "SON ÇEKİM",
                "--",
                "◷"
            )
        )

        self.timelapse_card = (
            self.create_stat_card(
                "TIME-LAPSE",
                "0",
                "▶"
            )
        )

        stats_layout.addWidget(
            self.total_images_card
        )

        stats_layout.addWidget(
            self.last_capture_card
        )

        stats_layout.addWidget(
            self.timelapse_card
        )

        layout.addLayout(
            stats_layout
        )

        # ==================================================
        # SON GÖRÜNTÜ KARTI
        # ==================================================

        image_card = QFrame()

        image_card.setObjectName(
            "card"
        )

        image_layout = QVBoxLayout(
            image_card
        )

        image_title = QLabel(
            "Son Görüntü"
        )

        image_title.setObjectName(
            "card_title"
        )

        image_layout.addWidget(
            image_title
        )

        # ==================================================
        # GÖRÜNTÜ ALANI
        # ==================================================

        self.image_preview = QLabel(
            "📷\n\nHenüz görüntü alınmadı"
        )

        self.image_preview.setObjectName(
            "image_preview"
        )

        self.image_preview.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.image_preview.setMinimumHeight(
            280
        )

        image_layout.addWidget(
            self.image_preview
        )

        # ==================================================
        # ALT BİLGİ
        # ==================================================

        bottom_layout = QHBoxLayout()

        self.last_capture_label = QLabel(
            "Son çekim: --"
        )

        self.last_capture_label.setObjectName(
            "info_label"
        )

        bottom_layout.addWidget(
            self.last_capture_label
        )

        bottom_layout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum,
            )
        )

        # ==================================================
        # FOTOĞRAF ÇEK BUTONU
        # ==================================================

        self.capture_button = QPushButton(
            "📷  Şimdi Fotoğraf Çek"
        )

        self.capture_button.setObjectName(
            "primary_button"
        )

        self.capture_button.setMinimumHeight(
            42
        )

        bottom_layout.addWidget(
            self.capture_button
        )

        image_layout.addLayout(
            bottom_layout
        )

        layout.addWidget(
            image_card
        )

        # ==================================================
        # FOOTER
        # ==================================================

        self.footer = QLabel(
            "Kamera bağlantısı bekleniyor  •  "
            "Otomatik çekim: Pasif"
        )

        self.footer.setObjectName(
            "footer"
        )

        layout.addWidget(
            self.footer
        )

        layout.addStretch()

    # ==================================================
    # İSTATİSTİK KARTI OLUŞTUR
    # ==================================================

    def create_stat_card(
        self,
        title,
        value,
        icon
    ):

        card = QFrame()

        card.setObjectName(
            "stat_card"
        )

        layout = QHBoxLayout(
            card
        )

        layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        # --------------------------------------------------
        # İKON
        # --------------------------------------------------

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "stat_icon"
        )

        # --------------------------------------------------
        # BİLGİLER
        # --------------------------------------------------

        information = QVBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "stat_title"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "stat_value"
        )

        information.addWidget(
            title_label
        )

        information.addWidget(
            value_label
        )

        layout.addWidget(
            icon_label
        )

        layout.addLayout(
            information
        )

        # --------------------------------------------------
        # VALUE LABEL'I KAYDET
        # --------------------------------------------------

        card.value_label = value_label

        return card

    # ==================================================
    # MODEL VERİLERİNİ GÜNCELLE
    # ==================================================

    def update_data(
        self,
        total_images,
        last_capture,
        timelapse_count,
    ):

        # --------------------------------------------------
        # TOPLAM GÖRÜNTÜ
        # --------------------------------------------------

        self.total_images_card.value_label.setText(
            str(total_images)
        )

        # --------------------------------------------------
        # SON ÇEKİM
        # --------------------------------------------------

        if last_capture:

            self.last_capture_card.value_label.setText(
                str(last_capture)
            )

            self.last_capture_label.setText(
                f"Son çekim: {last_capture}"
            )

        else:

            self.last_capture_card.value_label.setText(
                "--"
            )

            self.last_capture_label.setText(
                "Son çekim: --"
            )

        # --------------------------------------------------
        # TIME-LAPSE
        # --------------------------------------------------

        self.timelapse_card.value_label.setText(
            str(timelapse_count)
        )

    # ==================================================
    # SON ÇEKİLEN FOTOĞRAFI GÖSTER
    # ==================================================

    def update_image(
        self,
        image_path
    ):

        pixmap = QPixmap(
            image_path
        )

        # Görüntü yüklenemediyse
        if pixmap.isNull():
            return

        # --------------------------------------------------
        # Görüntüyü alana sığdır
        # --------------------------------------------------

        scaled_pixmap = pixmap.scaled(
            self.image_preview.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image_preview.setPixmap(
            scaled_pixmap
        )