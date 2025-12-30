const routesDiv = document.getElementById("routes");
const addBtn = document.getElementById("add-route-btn");
const MAX_ROUTES = 4;

/* Add Route */
addBtn.addEventListener("click", () => {
    if (routesDiv.children.length >= MAX_ROUTES) {
        alert("Maximum 4 stops allowed");
        return;
    }

    const div = document.createElement("div");
    div.className = "route-box";

    div.innerHTML = `
        <input type="text" placeholder="Enter Location">
        <button type="button" class="icon-btn location-btn">📍</button>
        <button type="button" class="icon-btn map-btn">🗺️</button>
        <button type="button" class="icon-btn delete-btn">✖</button>
    `;

    routesDiv.appendChild(div);
});

/* Handle Clicks */
routesDiv.addEventListener("click", (e) => {

    /* Delete */
    if (e.target.classList.contains("delete-btn")) {
        e.target.parentElement.remove();
    }

    /* Location */
    if (e.target.classList.contains("location-btn")) {
        const input = e.target.previousElementSibling;

        navigator.geolocation.getCurrentPosition(
            pos => {
                input.value =
                    pos.coords.latitude.toFixed(5) +
                    ", " +
                    pos.coords.longitude.toFixed(5);
            },
            () => alert("Location access denied")
        );
    }

    /* Maps */
    if (e.target.classList.contains("map-btn")) {
        window.open("https://www.google.com/maps", "_blank");
    }
});

/* Final Submit */
function setRoute() {
    alert("Route set successfully!");
}
