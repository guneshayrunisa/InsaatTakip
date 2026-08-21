from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageStat


class CameraHealthService:

    def __init__(self):

        # ==================================================
        # GENEL GÖRÜNTÜ EŞİKLERİ
        # ==================================================

        self.dark_threshold = 25
        self.bright_threshold = 245

        # ==================================================
        # BULANIKLIK
        # ==================================================

        # Laplacian variance
        #
        # Düşük değer -> bulanık
        # Yüksek değer -> daha net

        self.blur_threshold = 20.0

        # ==================================================
        # BÖLGESEL ANALİZ
        # ==================================================

        self.grid_rows = 3
        self.grid_columns = 3

    # ==================================================
    # ANA ANALİZ
    # ==================================================

    def analyze(self, image_path):

        image_path = Path(image_path)

        # --------------------------------------------------
        # DOSYA KONTROLÜ
        # --------------------------------------------------

        if not image_path.exists():

            return {
                "ok": False,
                "problem": "file_not_found",
                "message": "Görüntü dosyası bulunamadı."
            }

        # --------------------------------------------------
        # GÖRÜNTÜYÜ AÇ
        # --------------------------------------------------

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

        except Exception as error:

            return {
                "ok": False,
                "problem": "image_read_error",
                "message": (
                    f"Görüntü okunamadı: {error}"
                )
            }

        width, height = image.size

        # --------------------------------------------------
        # BOYUT KONTROLÜ
        # --------------------------------------------------

        if width < 100 or height < 100:

            return {
                "ok": False,
                "problem": "invalid_image",
                "message": "Görüntü boyutu geçersiz."
            }

        # ==================================================
        # PARLAKLIK
        # ==================================================

        dark_result = self.check_dark_image(
            image
        )

        if not dark_result["ok"]:

            return dark_result

        bright_result = self.check_bright_image(
            image
        )

        if not bright_result["ok"]:

            return bright_result

        # ==================================================
        # BULANIKLIK
        # ==================================================

        blur_result = self.check_blur(
            image_path
        )

        # ==================================================
        # BÖLGESEL ANALİZ
        # ==================================================

        regional_result = (
            self.check_regional_obstruction(
                image_path
            )
        )

        # ==================================================
        # GÖRÜŞ ENGELİ ÖNCELİKLİ
        # ==================================================

        if not regional_result["ok"]:

            return {
                "ok": False,
                "problem": regional_result["problem"],
                "message": regional_result["message"],
                "blur_score": blur_result.get(
                    "blur_score"
                ),
                "suspicious_regions":
                    regional_result.get(
                        "suspicious_regions",
                        []
                    )
            }

        # ==================================================
        # BULANIKLIK
        # ==================================================

        if not blur_result["ok"]:

            return blur_result

        # ==================================================
        # NORMAL
        # ==================================================

        return {
            "ok": True,
            "problem": None,
            "message": "Kamera görüntüsü normal.",
            "width": width,
            "height": height,
            "brightness": dark_result["brightness"],
            "blur_score": blur_result["blur_score"],
            "suspicious_regions": []
        }

    # ==================================================
    # KARANLIK GÖRÜNTÜ
    # ==================================================

    def check_dark_image(self, image):

        grayscale = image.convert(
            "L"
        )

        stat = ImageStat.Stat(
            grayscale
        )

        mean_brightness = float(
            stat.mean[0]
        )

        if mean_brightness <= self.dark_threshold:

            return {
                "ok": False,
                "problem": "too_dark",
                "message": (
                    "Kamera görüntüsü çok karanlık."
                ),
                "brightness": mean_brightness
            }

        return {
            "ok": True,
            "brightness": mean_brightness
        }

    # ==================================================
    # AŞIRI AYDINLIK
    # ==================================================

    def check_bright_image(self, image):

        grayscale = image.convert(
            "L"
        )

        stat = ImageStat.Stat(
            grayscale
        )

        mean_brightness = float(
            stat.mean[0]
        )

        if mean_brightness >= self.bright_threshold:

            return {
                "ok": False,
                "problem": "too_bright",
                "message": (
                    "Kamera görüntüsü çok aydınlık."
                ),
                "brightness": mean_brightness
            }

        return {
            "ok": True,
            "brightness": mean_brightness
        }

    # ==================================================
    # BULANIKLIK
    # ==================================================

    def check_blur(self, image_path):

        image = cv2.imread(
            str(image_path)
        )

        if image is None:

            return {
                "ok": False,
                "problem": "image_read_error",
                "message": (
                    "Bulanıklık analizi için "
                    "görüntü okunamadı."
                )
            }

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------------------
        # LAPLACIAN
        # ----------------------------------------------

        laplacian = cv2.Laplacian(
            gray,
            cv2.CV_64F
        )

        # ----------------------------------------------
        # VARIANCE
        # ----------------------------------------------

        blur_score = float(
            laplacian.var()
        )

        if blur_score < self.blur_threshold:

            return {
                "ok": False,
                "problem": "too_blurry",
                "message": (
                    "Kamera görüntüsü çok bulanık."
                ),
                "blur_score": blur_score
            }

        return {
            "ok": True,
            "blur_score": blur_score
        }

    # ==================================================
    # 3x3 BÖLGESEL GÖRÜŞ ANALİZİ
    # ==================================================

    def check_regional_obstruction(
        self,
        image_path
    ):

        image = cv2.imread(
            str(image_path)
        )

        if image is None:

            return {
                "ok": False,
                "problem": "image_read_error",
                "message": (
                    "Bölgesel analiz için "
                    "görüntü okunamadı."
                )
            }

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        height, width = gray.shape

        region_height = (
            height // self.grid_rows
        )

        region_width = (
            width // self.grid_columns
        )

        suspicious_regions = []
        regions = []

        # ==================================================
        # 3x3 GRID
        # ==================================================

        for row in range(
            self.grid_rows
        ):

            for column in range(
                self.grid_columns
            ):

                y1 = (
                    row * region_height
                )

                y2 = (
                    (row + 1)
                    * region_height
                )

                x1 = (
                    column * region_width
                )

                x2 = (
                    (column + 1)
                    * region_width
                )

                region = gray[
                    y1:y2,
                    x1:x2
                ]

                # ------------------------------------------
                # PIXEL VARYANSI
                # ------------------------------------------

                variance = float(
                    region.var()
                )

                standard_deviation = float(
                    region.std()
                )

                # ------------------------------------------
                # KENAR YOĞUNLUĞU
                # ------------------------------------------

                edges = cv2.Canny(
                    region,
                    50,
                    150
                )

                edge_ratio = float(
                    cv2.countNonZero(edges)
                    / edges.size
                )

                # ------------------------------------------
                # ORTALAMA PARLAKLIK
                # ------------------------------------------

                mean = float(
                    region.mean()
                )

                minimum = int(
                    region.min()
                )

                maximum = int(
                    region.max()
                )

                # ------------------------------------------
                # BÖLGE NUMARASI
                # ------------------------------------------

                region_number = (
                    row * self.grid_columns
                    + column
                    + 1
                )

                region_data = {

                    "region":
                        region_number,

                    "row":
                        row,

                    "column":
                        column,

                    "mean":
                        mean,

                    "variance":
                        variance,

                    "standard_deviation":
                        standard_deviation,

                    "min":
                        minimum,

                    "max":
                        maximum,

                    "edge_ratio":
                        edge_ratio
                }

                regions.append(
                    region_data
                )

        return {
            "ok": True,
            "problem": None,
            "message": (
                "Bölgesel analiz tamamlandı."
            ),
            "suspicious_regions":
                suspicious_regions,
            "regions":
                regions
        }

    # ==================================================
    # BÖLGESEL REFERANS OLUŞTUR
    # ==================================================

    def create_regional_reference(
        self,
        image_paths
    ):

        references = []

        for image_path in image_paths:

            result = (
                self.check_regional_obstruction(
                    image_path
                )
            )

            if not result["ok"]:

                continue

            references.append(
                result["regions"]
            )

        if not references:

            return None

        regional_reference = []

        # ==================================================
        # 9 BÖLGE
        # ==================================================

        for region_index in range(9):

            variances = [
                reference[
                    region_index
                ]["variance"]
                for reference in references
            ]

            edge_ratios = [
                reference[
                    region_index
                ]["edge_ratio"]
                for reference in references
            ]

            standard_deviations = [
                reference[
                    region_index
                ]["standard_deviation"]
                for reference in references
            ]

            regional_reference.append({

                "region":
                    region_index + 1,

                "variance_mean":
                    float(
                        np.mean(
                            variances
                        )
                    ),

                "variance_std":
                    float(
                        np.std(
                            variances
                        )
                    ),

                "edge_mean":
                    float(
                        np.mean(
                            edge_ratios
                        )
                    ),

                "edge_std":
                    float(
                        np.std(
                            edge_ratios
                        )
                    ),

                "std_mean":
                    float(
                        np.mean(
                            standard_deviations
                        )
                    ),

                "std_std":
                    float(
                        np.std(
                            standard_deviations
                        )
                    )
            })

        return regional_reference

    # ==================================================
    # REFERANSLA KARŞILAŞTIR
    # ==================================================

    def compare_with_regional_reference(
        self,
        image_path,
        reference
    ):

        if reference is None:

            return {
                "ok": False,
                "problem": "reference_missing",
                "message": (
                    "Bölgesel referans bulunamadı."
                )
            }

        result = (
            self.check_regional_obstruction(
                image_path
            )
        )

        if not result["ok"]:

            return result

        suspicious_regions = []
        regions = result["regions"]

        # ==================================================
        # HER BÖLGEYİ REFERANSLA KARŞILAŞTIR
        # ==================================================

        for region_data in regions:

            region_number = (
                region_data["region"]
            )

            ref = reference[
                region_number - 1
            ]

            # ------------------------------------------
            # REFERANS DEĞERLERİ
            # ------------------------------------------

            variance_mean = max(
                ref["variance_mean"],
                1.0
            )

            edge_mean = max(
                ref["edge_mean"],
                0.001
            )

            std_mean = max(
                ref["std_mean"],
                1.0
            )

            # ------------------------------------------
            # YENİ DEĞERLER
            # ------------------------------------------

            current_variance = (
                region_data["variance"]
            )

            current_edge = (
                region_data["edge_ratio"]
            )

            current_std = (
                region_data[
                    "standard_deviation"
                ]
            )

            # ------------------------------------------
            # DEĞİŞİM ORANLARI
            # ------------------------------------------

            variance_change = (
                abs(
                    current_variance
                    - variance_mean
                )
                / variance_mean
            )

            edge_change = (
                abs(
                    current_edge
                    - edge_mean
                )
                / edge_mean
            )

            std_change = (
                abs(
                    current_std
                    - std_mean
                )
                / std_mean
            )

            # ------------------------------------------
            # TEK TARAFLI DÜŞÜŞLER
            # ------------------------------------------

            variance_drop = (
                current_variance
                < variance_mean * 0.35
            )

            edge_drop = (
                current_edge
                < edge_mean * 0.35
            )

            std_drop = (
                current_std
                < std_mean * 0.35
            )

            # ------------------------------------------
            # ŞÜPHELİLİK
            # ------------------------------------------
            #
            # Burada henüz kesin alarm vermiyoruz.
            # İlk testlerde hangi bölgelerin
            # nasıl davrandığını görmek istiyoruz.

            suspicious = (
                variance_drop
                and
                edge_drop
                and
                std_drop
            )

            comparison = {

                "region":
                    region_number,

                "variance":
                    current_variance,

                "edge_ratio":
                    current_edge,

                "standard_deviation":
                    current_std,

                "variance_change":
                    variance_change,

                "edge_change":
                    edge_change,

                "std_change":
                    std_change,

                "suspicious":
                    suspicious
            }

            if suspicious:

                suspicious_regions.append(
                    comparison
                )

        # ==================================================
        # SONUÇ
        # ==================================================

        if suspicious_regions:

            return {

                "ok": False,

                "problem":
                    "regional_obstruction",

                "message":
                    (
                        "Kamera görüntüsünün "
                        "bazı bölgelerinde "
                        "anormal değişim "
                        "tespit edildi."
                    ),

                "suspicious_regions":
                    suspicious_regions,

                "regions":
                    regions
            }

        return {

            "ok": True,

            "problem": None,

            "message":
                (
                    "Görüntü bölgesel olarak normal."
                ),

            "suspicious_regions": [],

            "regions":
                regions
        }
