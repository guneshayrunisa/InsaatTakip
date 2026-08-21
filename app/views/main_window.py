from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QFrame,
)

from app.views.home_view import HomeView
from app.views.camera_view import CameraView
from app.views.calendar_view import CalendarView
from app.views.gallery_view import GalleryView
from app.views.timelapse_view import TimelapseView


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "İnşaat Takip Sistemi"
        )

        self.resize(
            1280,
            760
        )

        self.setup_ui()
        self.apply_style()

    # ==================================================
    # ARAYÜZÜ OLUŞTUR
    # ==================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QHBoxLayout(
            central
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(0)

        # ==================================================
        # SIDEBAR
        # ==================================================

        self.sidebar = QFrame()

        self.sidebar.setObjectName(
            "sidebar"
        )

        self.sidebar.setFixedWidth(
            240
        )

        sidebar_layout = QVBoxLayout(
            self.sidebar
        )

        sidebar_layout.setContentsMargins(
            20,
            25,
            20,
            20
        )

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        logo = QLabel(
            "🏗  İNŞAAT\n    TAKİP"
        )

        logo.setObjectName(
            "logo"
        )

        sidebar_layout.addWidget(
            logo
        )

        sidebar_layout.addSpacing(
            30
        )

        # ==================================================
        # MENÜ BUTONLARI
        # ==================================================

        self.home_button = QPushButton(
            "⌂   Ana Sayfa"
        )

        self.camera_button = QPushButton(
            "◉   Kamera"
        )

        self.calendar_button = QPushButton(
            "□   Takvim"
        )

        self.gallery_button = QPushButton(
            "▣   Galeri"
        )

        self.timelapse_button = QPushButton(
            "▶   Time-lapse"
        )

        # --------------------------------------------------
        # Menüye ekle
        # --------------------------------------------------

        sidebar_layout.addWidget(
            self.home_button
        )

        sidebar_layout.addWidget(
            self.camera_button
        )

        sidebar_layout.addWidget(
            self.calendar_button
        )

        sidebar_layout.addWidget(
            self.gallery_button
        )

        sidebar_layout.addWidget(
            self.timelapse_button
        )

        sidebar_layout.addStretch()

        # ==================================================
        # AYARLAR
        # ==================================================

        self.settings_button = QPushButton(
            "⚙   Ayarlar"
        )

        sidebar_layout.addWidget(
            self.settings_button
        )

        # ==================================================
        # SAYFALAR
        # ==================================================

        self.pages = QStackedWidget()

        # ==================================================
        # 0 - ANA SAYFA
        # ==================================================

        self.home_view = HomeView()

        self.pages.addWidget(
            self.home_view
        )

        # ==================================================
        # 1 - KAMERA
        # ==================================================

        self.camera_view = CameraView()

        self.pages.addWidget(
            self.camera_view
        )

        # ==================================================
        # 2 - TAKVİM
        # ==================================================

        self.calendar_view = CalendarView()

        self.pages.addWidget(
            self.calendar_view
        )

        # ==================================================
        # 3 - GALERİ
        # ==================================================

        self.gallery_view = GalleryView()

        self.pages.addWidget(
            self.gallery_view
        )

        # ==================================================
        # 4 - TIME-LAPSE
        # ==================================================

        self.timelapse_view = TimelapseView()

        self.pages.addWidget(
            self.timelapse_view
        )

        # ==================================================
        # 5 - AYARLAR
        # ==================================================

        self.settings_view = self.create_placeholder(
            "Ayarlar"
        )

        self.pages.addWidget(
            self.settings_view
        )

        # ==================================================
        # ANA LAYOUT'A EKLE
        # ==================================================

        layout.addWidget(
            self.sidebar
        )

        layout.addWidget(
            self.pages
        )

    # ==================================================
    # PLACEHOLDER
    # ==================================================

    def create_placeholder(
        self,
        title
    ):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "page_title"
        )

        layout.addWidget(
            title_label
        )

        layout.addStretch()

        message = QLabel(
            f"{title} bölümü hazırlanıyor."
        )

        message.setObjectName(
            "page_message"
        )

        layout.addWidget(
            message
        )

        layout.addStretch()

        return page

    # ==================================================
    # STİL
    # ==================================================

    def apply_style(self):

        self.setStyleSheet("""

        QMainWindow {
            background-color: #101418;
        }

        QWidget {
            font-family: "Segoe UI";
        }

        /* ==========================================
           SIDEBAR
           ========================================== */

        #sidebar {
            background-color: #171c21;
            border-right: 1px solid #252c33;
        }

        #logo {
            color: white;
            font-size: 22px;
            font-weight: bold;
        }

        /* ==========================================
           BUTONLAR
           ========================================== */

        QPushButton {
            background-color: transparent;
            color: #aeb7c2;
            border: none;
            border-radius: 8px;
            text-align: left;
            padding-left: 15px;
            font-size: 14px;
            min-height: 48px;
        }

        QPushButton:hover {
            background-color: #222a31;
            color: white;
        }

        /* ==========================================
           BAŞLIKLAR
           ========================================== */

        #page_title {
            color: white;
            font-size: 28px;
            font-weight: bold;
        }

        #page_subtitle {
            color: #7f8a96;
            font-size: 13px;
        }

        #page_message {
            color: #7f8a96;
            font-size: 16px;
        }

        /* ==========================================
           SİSTEM DURUMU
           ========================================== */

        #status {
            color: #6fcf97;
            background-color: #17251e;
            border-radius: 15px;
            padding: 8px 14px;
            font-size: 12px;
        }

        /* ==========================================
           İSTATİSTİK KARTLARI
           ========================================== */

        #stat_card {
            background-color: #171c21;
            border: 1px solid #252c33;
            border-radius: 12px;
            min-height: 80px;
        }

        #stat_icon {
            font-size: 25px;
        }

        #stat_title {
            color: #7f8a96;
            font-size: 11px;
        }

        #stat_value {
            color: white;
            font-size: 22px;
            font-weight: bold;
        }

        /* ==========================================
           KART
           ========================================== */

        #card {
            background-color: #171c21;
            border: 1px solid #252c33;
            border-radius: 12px;
        }

        #card_title {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        /* ==========================================
           GÖRÜNTÜ
           ========================================== */

        #image_preview,
        #camera_preview {
            background-color: #0d1115;
            border: 1px dashed #343d46;
            border-radius: 8px;
            color: #66717d;
            font-size: 14px;
        }

        /* ==========================================
           BİLGİ
           ========================================== */

        #info_label {
            color: #7f8a96;
            font-size: 12px;
        }

        /* ==========================================
           ANA BUTON
           ========================================== */

        #primary_button {
            background-color: #2f80ed;
            color: white;
            text-align: center;
            padding: 0 20px;
            border-radius: 8px;
            font-weight: bold;
        }

        #primary_button:hover {
            background-color: #4a91ef;
        }

        /* ==========================================
           İKİNCİL BUTON
           ========================================== */

        #secondary_button {
            background-color: #222a31;
            color: white;
            text-align: center;
            padding: 0 18px;
            border-radius: 8px;
        }

        #secondary_button:hover {
            background-color: #303a43;
        }

        /* ==========================================
           KAMERA
           ========================================== */

        #camera_status {
            color: #f2c94c;
            font-size: 12px;
        }

        #large_icon {
            font-size: 35px;
        }

        /* ==========================================
           FOOTER
           ========================================== */

        #footer {
            color: #65717d;
            font-size: 11px;
        }

        /* ==========================================
           GALERİ
           ========================================== */

        #gallery_scroll {
            background-color: transparent;
            border: none;
        }

        #gallery_scroll QWidget {
            background-color: transparent;
        }

        """)