from fastapi import APIRouter
from app.services.camera_manager import CameraManager
from app.data.database import Database


router = APIRouter(
    prefix="/api/cameras",
    tags=["Cameras"]
)


database = Database()
camera_manager = CameraManager(
    camera_count=2
)

@router.get("")
def get_cameras():

    # Kamera bağlantılarını güncelle
    camera_manager.refresh_connections()

    # Veritabanındaki kameralar
    cameras = database.get_all_cameras()

    # Gerçekten bağlı kameralar
    connected_camera_ids = set(
        camera_manager.get_connected_cameras()
    )

    result = []

    for camera in cameras:

        camera_data = dict(camera)

        camera_id = camera_data["id"]

        camera_data["connected"] = (
            camera_id in connected_camera_ids
        )

        result.append(
            camera_data
        )

    return {
        "cameras": result
    }

# ==================================================
# FOTOĞRAF ÇEK
# ==================================================

@router.post("/{camera_id}/capture")
def capture_photo(camera_id: int):

    result = camera_manager.capture_photo(
        camera_id
    )

    if result is None:

        return {
            "success": False,
            "camera_id": camera_id,
            "message": "Fotoğraf çekilemedi."
        }

    return {
        "success": True,
        "camera_id": camera_id,
        "message": "Fotoğraf başarıyla çekildi.",
        "photo": {
            "path": result["path"],
            "filename": result["filename"],
            "timestamp": str(
                result["timestamp"]
            )
        }
    }