function addRoute() {
    const routes = document.getElementById("routes");

    const div = document.createElement("div");
    div.className = "route-box";

    div.innerHTML = `
        <input type="text" placeholder="Enter Location / Stop">
        <button class="icon-btn" onclick="getLocation(this)">📍</button>
        <button class="icon-btn" onclick="openMaps()">🗺️</button>
    `;

    routes.appendChild(div);
}

function getLocation(btn) {
    const input = btn.previousElementSibling;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                input.value =
                    "Lat: " +
                    position.coords.latitude.toFixed(4) +
                    ", Lng: " +
                    position.coords.longitude.toFixed(4);
            },
            () => alert("Location access denied")
        );
    } else {
        alert("Geolocation not supported");
    }
}

function openMaps() {
    window.open("https://www.google.com/maps", "_blank");
}

function setRoute() {
    alert("Route set successfully!");
    // Later:
    // send data to backend using fetch/AJAX
}
