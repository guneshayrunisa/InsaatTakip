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

        layout.addWidget(title)
        layout.addWidget(subtitle)

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

        card_layout.setSpacing(
            20
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

        card_layout.addWidget(
            info
        )

        # ==================================================
        # BAŞLANGIÇ SAATİ
        # ==================================================

        time_layout = QHBoxLayout()

        time_label = QLabel(
            "Başlangıç saati:"
        )

        time_label.setObjectName(
            "card_title"
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
        # ÇEKİM SIKLIĞI
        # ==================================================

        interval_layout = QHBoxLayout()

        interval_label = QLabel(
            "Çekim sıklığı:"
        )

        interval_label.setObjectName(
            "card_title"
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
            40
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
        # AKTİF / PASİF BUTONU
        # ==================================================

        button_layout = QHBoxLayout()

        self.toggle_button = QPushButton(
            "▶  Otomatik Çekimi Aktif Et"
        )

        self.toggle_button.setObjectName(
            "primary_button"
        )

        self.toggle_button.setMinimumHeight(
            42
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

        status_layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            status_card
        )

        layout.addStretch()
