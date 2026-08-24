from fastapi import APIRouter

from app.data.database import Database


router = APIRouter(
    prefix="/api",
    tags=["Status"]
)


database = Database()


@router.get("/status")
def get_status():

    total_images = database.get_photo_count()

    last_photo = database.get_last_photo()

    auto_capture = database.get_auto_capture_settings()

    return {
        "system": "online",

        "total_images": total_images,

        "last_photo": (
            dict(last_photo)
            if last_photo
            else None
        ),

        "auto_capture": (
            dict(auto_capture)
            if auto_capture
            else None
        )
    }