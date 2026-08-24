const API_URL = "http://127.0.0.1:8000";


// ==================================================
// API'DEN VERİLERİ AL
// ==================================================

async function loadDashboard() {

    try {

        const statusResponse =
            await fetch(
                `${API_URL}/api/status`
            );

        const statusData =
            await statusResponse.json();


        const camerasResponse =
            await fetch(
                `${API_URL}/api/cameras`
            );

        const camerasData =
            await camerasResponse.json();


        updateSystemStatus(
            statusData
        );

        updateCameras(
            camerasData.cameras
        );

    }
    catch (error) {

        console.error(
            "API bağlantı hatası:",
            error
        );

        showOffline();

    }

}


// ==================================================
// SİSTEM DURUMU
// ==================================================

function updateSystemStatus(
    data
) {

    const status =
        document.getElementById(
            "system-status"
        );

    const dot =
        document.getElementById(
            "status-dot"
        );


    if (data.system === "online") {

        status.textContent =
            "Sistem çevrimiçi";

        dot.style.background =
            "#4ade80";

    }
    else {

        status.textContent =
            "Sistem çevrimdışı";

        dot.style.background =
            "#ef4444";

    }


    // FOTOĞRAF SAYISI

    document.getElementById(
        "image-count"
    ).textContent =
        data.total_images ?? "-";


    // SON FOTOĞRAF

    const lastPhoto =
        document.getElementById(
            "last-photo"
        );


    if (data.last_photo) {

        lastPhoto.innerHTML = `

            <div>
                <strong>
                    Dosya:
                </strong>

                ${data.last_photo.file_path}

            </div>

            <div>
                <strong>
                    Kamera:
                </strong>

                ${data.last_photo.camera_id}

            </div>

            <div>
                <strong>
                    Tarih:
                </strong>

                ${data.last_photo.captured_at}

            </div>

        `;

    }
    else {

        lastPhoto.textContent =
            "Henüz fotoğraf çekilmedi.";

    }


    // OTOMATİK ÇEKİM

    const autoCapture =
        document.getElementById(
            "auto-capture-status"
        );


    if (
        data.auto_capture &&
        data.auto_capture.enabled
    ) {

        autoCapture.textContent =
            "Aktif";

    }
    else {

        autoCapture.textContent =
            "Pasif";

    }

}


// ==================================================
// KAMERALAR
// ==================================================

function updateCameras(
    cameras
) {

    const list =
        document.getElementById(
            "camera-list"
        );


    document.getElementById(
        "camera-count"
    ).textContent =
        cameras.length;


    const connected =
        cameras.filter(
            camera =>
                camera.connected
        ).length;


    document.getElementById(
        "connected-camera-count"
    ).textContent =
        connected;


    if (!cameras.length) {

        list.textContent =
            "Kamera bulunamadı.";

        return;

    }


    list.innerHTML = "";


    cameras.forEach(
        camera => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "camera-item";


            const statusClass =
                camera.connected
                    ? "connected"
                    : "disconnected";


            const statusText =
                camera.connected
                    ? "● Bağlı"
                    : "● Bağlı değil";


            item.innerHTML = `

                <div class="camera-info">

                    <span class="camera-name">
                        ${camera.name}
                    </span>

                    <span class="camera-model">
                        ${camera.model ?? ""}
                    </span>

                </div>

                <span class="${statusClass}">
                    ${statusText}
                </span>

            `;


            list.appendChild(
                item
            );

        }
    );

}


// ==================================================
// API BAĞLANTISI YOK
// ==================================================

function showOffline() {

    document.getElementById(
        "system-status"
    ).textContent =
        "Sistem çevrimdışı";


    document.getElementById(
        "status-dot"
    ).style.background =
        "#ef4444";

}


// ==================================================
// SAYFA AÇILDIĞINDA
// ==================================================

loadDashboard();


// Her 10 saniyede bir güncelle

setInterval(
    loadDashboard,
    10000
);