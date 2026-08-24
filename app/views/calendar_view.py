from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTimeEdit,
    QSpinBox,
    QComboBox,
    QFrame,
)
from PySide6.QtCore import Qt, QTime


class CalendarView(QWidget):

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

        # ==================================================
        # BAŞLIK
        # ==================================================

        title = QLabel(
            "Takvim"
        )

        title.setObjectName(
            "page_title"
        )

        subtitle = QLabel(
            "Otomatik fotoğraf çekim zamanlarını yönetin."
        )

        subtitle.setObjectName(
            "page_subtitle"
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # ==================================================
        # AYAR KARTI
        # ==================================================

        card = QFrame()

        card.setObjectName(
            "card"
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        card_layout.setSpacing(
            18
        )

        # ==================================================
        # AÇIKLAMA
        # ==================================================

        info = QLabel(
            "Belirlediğiniz başlangıç saatinden itibaren "
            "belirlediğiniz aralıklarla otomatik fotoğraf çekin."
        )

        info.setObjectName(
            "info_label"
        )

        info.setWordWrap(
            True
        )

        info.setStyleSheet(
            "font-size: 15px;"
        )

        card_layout.addWidget(
            info
        )

        # ==================================================
        # BAŞLANGIÇ SAATİ
        # ==================================================

        time_layout = QHBoxLayout()

        time_layout.setSpacing(
            20
        )

        time_label = QLabel(
            "Başlangıç saati:"
        )

        time_label.setObjectName(
            "card_title"
        )

        time_label.setMinimumWidth(
            210
        )

        time_label.setStyleSheet(
            "font-size: 14px; "
            "font-weight: 600;"
        )

        self.time_edit = QTimeEdit()

        self.time_edit.setDisplayFormat(
            "HH:mm"
        )

        self.time_edit.setTime(
            QTime(18, 0)
        )

        self.time_edit.setMinimumHeight(
            40
        )

        self.time_edit.setMinimumWidth(
            150
        )

        self.time_edit.setStyleSheet(
            """
            QTimeEdit {
                font-size: 14px;
                padding: 6px 10px;
            }

            QTimeEdit::up-button,
            QTimeEdit::down-button {
                width: 28px;
            }
            """
        )

        time_layout.addWidget(
            time_label
        )

        time_layout.addWidget(
            self.time_edit
        )

        time_layout.addStretch()

        card_layout.addLayout(
            time_layout
        )

        # ==================================================
        # AYIRICI
        # ==================================================

        separator_1 = QFrame()

        separator_1.setFrameShape(
            QFrame.Shape.HLine
        )

        separator_1.setFrameShadow(
            QFrame.Shadow.Sunken
        )

        card_layout.addWidget(
            separator_1
        )

        # ==================================================
        # ÇEKİM SIKLIĞI
        # ==================================================

        interval_layout = QHBoxLayout()

        interval_layout.setSpacing(
            20
        )

        interval_label = QLabel(
            "Çekim sıklığı:"
        )

        interval_label.setObjectName(
            "card_title"
        )

        interval_label.setMinimumWidth(
            210
        )

        interval_label.setStyleSheet(
            "font-size: 14px; "
            "font-weight: 600;"
        )

        # --------------------------------------------------
        # SAYI
        # --------------------------------------------------

        self.interval_spin = QSpinBox()

        self.interval_spin.setMinimum(
            1
        )

        self.interval_spin.setMaximum(
            9999
        )

        self.interval_spin.setValue(
            1
        )

        self.interval_spin.setMinimumHeight(
            40
        )

        self.interval_spin.setMinimumWidth(
            150
        )

        self.interval_spin.setStyleSheet(
            """
            QSpinBox {
                font-size: 14px;
                padding: 6px 10px;
            }

            QSpinBox::up-button,
            QSpinBox::down-button {
                width: 28px;
            }
            """
        )

        # --------------------------------------------------
        # BİRİM
        # --------------------------------------------------

        self.interval_combo = QComboBox()

        self.interval_combo.addItem(
            "Dakika",
            "minutes"
        )

        self.interval_combo.addItem(
            "Saat",
            "hours"
        )

        self.interval_combo.addItem(
            "Gün",
            "days"
        )

        self.interval_combo.setMinimumHeight(
            50
        )

        self.interval_combo.setMinimumWidth(
            190
        )

        self.interval_combo.setStyleSheet(
            """
            QComboBox {
                font-size: 14px;
                padding: 8px 12px;
            }

            QComboBox QAbstractItemView {
                font-size: 14px;
            }
            """
        )

        interval_layout.addWidget(
            interval_label
        )

        interval_layout.addWidget(
            self.interval_spin
        )

        interval_layout.addWidget(
            self.interval_combo
        )

        interval_layout.addStretch()

        card_layout.addLayout(
            interval_layout
        )

        # ==================================================
        # AYIRICI
        # ==================================================

        separator_2 = QFrame()

        separator_2.setFrameShape(
            QFrame.Shape.HLine
        )

        separator_2.setFrameShadow(
            QFrame.Shadow.Sunken
        )

        card_layout.addWidget(
            separator_2
        )

        # ==================================================
        # KAMERA SEÇİMİ
        # ==================================================

        camera_layout = QHBoxLayout()

        camera_layout.setSpacing(
            20
        )

        camera_label = QLabel(
            "Kamera:"
        )

        camera_label.setObjectName(
            "card_title"
        )

        camera_label.setMinimumWidth(
            210
        )

        camera_label.setStyleSheet(
            "font-size: 14px; "
            "font-weight: 600;"
        )

        self.camera_combo = QComboBox()

        self.camera_combo.setMinimumHeight(
            40
        )

        self.camera_combo.setMinimumWidth(
            395
        )

        self.camera_combo.setStyleSheet(
            """
            QComboBox {
                font-size: 14px;
                padding: 6px 10px;
            }

            QComboBox QAbstractItemView {
                font-size: 14px;
            }
            """
        )

        camera_layout.addWidget(
            camera_label
        )

        camera_layout.addWidget(
            self.camera_combo
        )

        camera_layout.addStretch()

        card_layout.addLayout(
            camera_layout
        )

        # ==================================================
        # AKTİF / PASİF BUTONU
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            10
        )

        self.toggle_button = QPushButton(
            "▶  Otomatik Çekimi Aktif Et"
        )

        self.toggle_button.setObjectName(
            "primary_button"
        )

        self.toggle_button.setMinimumHeight(
            44
        )

        self.toggle_button.setMinimumWidth(
            330
        )

        self.toggle_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                padding: 8px 18px;
            }
            """
        )

        button_layout.addWidget(
            self.toggle_button
        )

        button_layout.addStretch()

        card_layout.addLayout(
            button_layout
        )

        layout.addWidget(
            card
        )

        # ==================================================
        # DURUM KARTI
        # ==================================================

        status_card = QFrame()

        status_card.setObjectName(
            "card"
        )

        status_layout = QVBoxLayout(
            status_card
        )

        status_layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        self.status_label = QLabel(
            "Otomatik çekim: Pasif"
        )

        self.status_label.setObjectName(
            "page_message"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setWordWrap(
            True
        )

        self.status_label.setStyleSheet(
            "font-size: 14px;"
        )

        status_layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            status_card
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

        self.camera_combo.blockSignals(
            True
        )

        self.camera_combo.clear()

        for camera_id in camera_ids:

            self.camera_combo.addItem(
                f"Kamera {camera_id}",
                camera_id
            )

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

        elif camera_ids:

            self.camera_combo.setCurrentIndex(
                0
            )

        else:

            self.camera_combo.addItem(
                "Kamera bulunamadı",
                None
            )

        self.camera_combo.blockSignals(
            False
        )

    # ==================================================
    # SEÇİLİ KAMERA
    # ==================================================

    def get_selected_camera_id(self):

        return (
            self.camera_combo.currentData()
        )