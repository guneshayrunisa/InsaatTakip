from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QFrame,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class GalleryView(QWidget):

    def __init__(self):

        super().__init__()

        # ==================================================
        # PROJE KLASÖRÜ
        # ==================================================

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        self.image_dir = (
            self.project_root / "images"
        )

        # ==================================================
        # SEÇİLİ KAMERA
        # ==================================================

        self.selected_camera = 0

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

        # ==================================================
        # BAŞLIK
        # ==================================================

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel(
            "Galeri"
        )

        title.setObjectName(
            "page_title"
        )

        subtitle = QLabel(
            "Projede çekilen görüntüleri görüntüleyin."
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

        header.addStretch()

        # ==================================================
        # KAMERA SEÇİMİ
        # ==================================================

        camera_label = QLabel(
            "Kamera:"
        )

        camera_label.setObjectName(
            "info_label"
        )

        header.addWidget(
            camera_label
        )

        self.camera_combo = QComboBox()

        self.camera_combo.setMinimumWidth(
            150
        )

        # Kamera 0
        self.camera_combo.addItem(
            "Kamera 0",
            0
        )

        # Kamera 1
        self.camera_combo.addItem(
            "Kamera 1",
            1
        )

        self.camera_combo.currentIndexChanged.connect(
            self.camera_changed
        )

        header.addWidget(
            self.camera_combo
        )

        # ==================================================
        # YENİLE BUTONU
        # ==================================================

        self.refresh_button = QPushButton(
            "↻  Yenile"
        )

        self.refresh_button.setObjectName(
            "secondary_button"
        )

        self.refresh_button.setMinimumHeight(
            40
        )

        self.refresh_button.clicked.connect(
            self.load_images
        )

        header.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            header
        )

        # ==================================================
        # FOTOĞRAF ALANI
        # ==================================================

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setObjectName(
            "gallery_scroll"
        )

        self.gallery_widget = QWidget()

        self.grid = QGridLayout(
            self.gallery_widget
        )

        self.grid.setSpacing(
            15
        )

        self.grid.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.scroll_area.setWidget(
            self.gallery_widget
        )

        layout.addWidget(
            self.scroll_area
        )

    # ==================================================
    # KAMERA DEĞİŞTİR
    # ==================================================

    def camera_changed(
        self,
        index
    ):

        camera_id = (
            self.camera_combo
            .itemData(index)
        )

        self.selected_camera = (
            camera_id
        )

        self.load_images()

    # ==================================================
    # GALERİYİ YÜKLE
    # ==================================================

    def load_images(self):

        # ==================================================
        # ESKİ KARTLARI TEMİZLE
        # ==================================================

        while self.grid.count():

            item = self.grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

        # ==================================================
        # KAMERA KLASÖRÜ
        # ==================================================

        camera_dir = (
            self.image_dir
            / f"camera_{self.selected_camera}"
        )

        camera_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==================================================
        # FOTOĞRAFLARI BUL
        # ==================================================

        images = sorted(
            camera_dir.glob("*.jpg"),
            key=lambda path: path.stat().st_mtime,
            reverse=True
        )

        # ==================================================
        # FOTOĞRAF YOK
        # ==================================================

        if not images:

            empty_label = QLabel(
                f"📷\n\n"
                f"Kamera {self.selected_camera} "
                f"için henüz görüntü bulunmuyor."
            )

            empty_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty_label.setObjectName(
                "page_message"
            )

            self.grid.addWidget(
                empty_label,
                0,
                0
            )

            return

        # ==================================================
        # FOTOĞRAF KARTLARI
        # ==================================================

        columns = 3

        for index, image_path in enumerate(
            images
        ):

            card = self.create_image_card(
                image_path
            )

            row = (
                index // columns
            )

            column = (
                index % columns
            )

            self.grid.addWidget(
                card,
                row,
                column
            )

    # ==================================================
    # FOTOĞRAF KARTI
    # ==================================================

    def create_image_card(
        self,
        image_path
    ):

        card = QFrame()

        card.setObjectName(
            "card"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        # ==================================================
        # FOTOĞRAF
        # ==================================================

        image = QLabel()

        image.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        image.setMinimumSize(
            250,
            150
        )

        pixmap = QPixmap(
            str(image_path)
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                250,
                150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            image.setPixmap(
                pixmap
            )

        layout.addWidget(
            image
        )

        # ==================================================
        # KAMERA BİLGİSİ
        # ==================================================

        camera_label = QLabel(
            f"Kamera {self.selected_camera}"
        )

        camera_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        camera_label.setObjectName(
            "info_label"
        )

        layout.addWidget(
            camera_label
        )

        # ==================================================
        # DOSYA ADI
        # ==================================================

        filename = QLabel(
            image_path.stem
        )

        filename.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        filename.setObjectName(
            "info_label"
        )

        layout.addWidget(
            filename
        )

        return card
