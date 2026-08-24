import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        # ==================================================
        # PROJE ANA KLASÖRÜ
        # ==================================================

        self.base_dir = (
            Path(__file__).resolve().parent.parent.parent
        )

        # ==================================================
        # DATA KLASÖRÜ
        # ==================================================

        self.data_dir = self.base_dir / "data"

        self.data_dir.mkdir(
            exist_ok=True
        )

        # ==================================================
        # DATABASE
        # ==================================================

        self.db_path = (
            self.data_dir / "insaat_takip.db"
        )

        self.create_tables()

    # ==================================================
    # BAĞLANTI
    # ==================================================

    def get_connection(self):

        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ==================================================
    # TABLOLARI OLUŞTUR
    # ==================================================

    def create_tables(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        # ==================================================
        # KAMERALAR
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cameras (

                id INTEGER PRIMARY KEY,

                name TEXT NOT NULL,

                model TEXT,

                location TEXT,

                enabled INTEGER NOT NULL DEFAULT 1

            )
        """)

        # ==================================================
        # VARSAYILAN KAMERA
        # ==================================================

        cursor.execute("""
            INSERT OR IGNORE INTO cameras (
                id,
                name,
                model,
                location,
                enabled
            )
            VALUES (
                0,
                'Kamera 1',
                'IMX708',
                '',
                1
            )
        """)

        # ==================================================
        # FOTOĞRAFLAR
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS photos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                camera_id INTEGER NOT NULL DEFAULT 0,

                file_path TEXT NOT NULL,

                captured_at TEXT NOT NULL,

                FOREIGN KEY (camera_id)
                    REFERENCES cameras(id)

            )
        """)

        # ==================================================
        # ESKİ DATABASE İÇİN CAMERA_ID MIGRATION
        # ==================================================

        cursor.execute(
            "PRAGMA table_info(photos)"
        )

        columns = [
            row["name"]
            for row in cursor.fetchall()
        ]

        if "camera_id" not in columns:

            cursor.execute("""
                ALTER TABLE photos
                ADD COLUMN camera_id
                INTEGER NOT NULL DEFAULT 0
            """)

        # ==================================================
        # TIME-LAPSE
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timelapses (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                file_path TEXT NOT NULL,

                created_at TEXT NOT NULL

            )
        """)

        # ==================================================
        # OTOMATİK ÇEKİM AYARLARI
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auto_capture_settings (

                id INTEGER PRIMARY KEY,

                enabled INTEGER NOT NULL DEFAULT 0,

                camera_id INTEGER,

                start_time TEXT,

                interval_value INTEGER,

                interval_unit TEXT,

                FOREIGN KEY (camera_id)
                    REFERENCES cameras(id)

            )
        """)

        # ==================================================
        # VARSAYILAN OTOMATİK ÇEKİM KAYDI
        # ==================================================

        cursor.execute("""
            INSERT OR IGNORE INTO auto_capture_settings (
                id,
                enabled,
                camera_id,
                start_time,
                interval_value,
                interval_unit
            )
            VALUES (
                1,
                0,
                NULL,
                NULL,
                NULL,
                NULL
            )
        """)

        connection.commit()

        connection.close()

    # ==================================================
    # FOTOĞRAF EKLE
    # ==================================================

    def add_photo(
        self,
        file_path,
        captured_at,
        camera_id=0
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO photos (
                camera_id,
                file_path,
                captured_at
            )
            VALUES (?, ?, ?)
            """,
            (
                int(camera_id),
                str(file_path),
                str(captured_at)
            )
        )

        connection.commit()

        photo_id = cursor.lastrowid

        connection.close()

        return photo_id

    # ==================================================
    # FOTOĞRAF SAYISI
    # ==================================================

    def get_photo_count(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM photos"
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count

    # ==================================================
    # TÜM FOTOĞRAFLAR
    # ==================================================

    def get_all_photos(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                camera_id,
                file_path,
                captured_at
            FROM photos
            ORDER BY id DESC
        """)

        photos = cursor.fetchall()

        connection.close()

        return photos

    # ==================================================
    # KAMERAYA GÖRE FOTOĞRAFLAR
    # ==================================================

    def get_photos_by_camera(
        self,
        camera_id
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                camera_id,
                file_path,
                captured_at
            FROM photos
            WHERE camera_id = ?
            ORDER BY id DESC
            """,
            (
                int(camera_id),
            )
        )

        photos = cursor.fetchall()

        connection.close()

        return photos

    # ==================================================
    # SON FOTOĞRAF
    # ==================================================

    def get_last_photo(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                camera_id,
                file_path,
                captured_at
            FROM photos
            ORDER BY id DESC
            LIMIT 1
        """)

        photo = cursor.fetchone()

        connection.close()

        return photo

    # ==================================================
    # KAMERALARI GETİR
    # ==================================================

    def get_all_cameras(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                model,
                location,
                enabled
            FROM cameras
            WHERE enabled = 1
            ORDER BY id
        """)

        cameras = cursor.fetchall()

        connection.close()

        return cameras

    # ==================================================
    # OTOMATİK ÇEKİM AYARLARINI KAYDET
    # ==================================================

    def save_auto_capture_settings(
        self,
        enabled,
        camera_id=None,
        start_time=None,
        interval_value=None,
        interval_unit=None
    ):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE auto_capture_settings
            SET
                enabled = ?,
                camera_id = ?,
                start_time = ?,
                interval_value = ?,
                interval_unit = ?
            WHERE id = 1
            """,
            (
                1 if enabled else 0,
                camera_id,
                start_time,
                interval_value,
                interval_unit
            )
        )

        connection.commit()

        connection.close()

    # ==================================================
    # OTOMATİK ÇEKİM AYARLARINI GETİR
    # ==================================================

    def get_auto_capture_settings(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                enabled,
                camera_id,
                start_time,
                interval_value,
                interval_unit
            FROM auto_capture_settings
            WHERE id = 1
        """)

        settings = cursor.fetchone()

        connection.close()

        if settings is None:

            return {
                "enabled": False,
                "camera_id": None,
                "start_time": None,
                "interval_value": None,
                "interval_unit": None
            }

        return {
            "enabled": bool(
                settings["enabled"]
            ),

            "camera_id":
                settings["camera_id"],

            "start_time":
                settings["start_time"],

            "interval_value":
                settings["interval_value"],

            "interval_unit":
                settings["interval_unit"]
        }