import sys

from PySide6.QtWidgets import QApplication

from app.models.project_model import ProjectModel
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController
from app.services.camera_service import CameraService


def main():

    # ==================================================
    # UYGULAMAYI BAŞLAT
    # ==================================================

    app = QApplication(sys.argv)

    # ==================================================
    # MODEL
    # ==================================================

    model = ProjectModel()

    # ==================================================
    # ANA PENCERE
    # ==================================================

    view = MainWindow()

    # ==================================================
    # KAMERA SERVİSİ
    # ==================================================

    camera_service = CameraService()

    # ==================================================
    # CONTROLLER
    # ==================================================

    controller = MainController(
        model,
        view,
        camera_service
    )

    # ==================================================
    # CONTROLLER BAŞLAT
    # ==================================================

    controller.start()

    # ==================================================
    # PENCEREYİ GÖSTER
    # ==================================================

    view.show()

    # ==================================================
    # UYGULAMAYI ÇALIŞTIR
    # ==================================================

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()