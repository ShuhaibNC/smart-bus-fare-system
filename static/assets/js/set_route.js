const routesDiv = document.getElementById("routes");
const addBtn = document.getElementById("add-route-btn");
const MAX_ROUTES = 4;

/* Renumber stop labels */
function renumberStops() {
    const labels = routesDiv.querySelectorAll(".route-label");
    labels.forEach((label, index) => {
        label.textContent = `Stop ${index + 1}`;
    });
}

/* Add new stop */
addBtn.addEventListener("click", () => {
    if (routesDiv.children.length >= MAX_ROUTES) {
        alert("You can add up to 4 stops only");
        return;
    }

    const div = document.createElement("div");
    div.className = "route-box modern-route";

    div.innerHTML = `
        <label class="route-label"></label>

        <input
            type="text"
            name="stops[]"
            placeholder="Enter location"
            required
            class="input-modern"
        >

        <div class="route-actions">
            <button type="button" class="route-icon-btn location-btn">Current location</button>
            <button type="button" class="route-icon-btn map-btn">Open map</button>
            <button type="button" class="route-icon-btn delete-btn">Remove</button>
        </div>
    `;

    routesDiv.appendChild(div);
    renumberStops();
});

/* Button actions inside routes */
routesDiv.addEventListener("click", (e) => {

    /* Remove stop */
    if (e.target.classList.contains("delete-btn")) {
        e.target.closest(".route-box").remove();
        renumberStops();
    }

    /* Fill with current GPS coordinates */
    if (e.target.classList.contains("location-btn")) {
        const input = e.target.closest(".route-box").querySelector("input");

        navigator.geolocation.getCurrentPosition(
            pos => {
                input.value =
                    pos.coords.latitude.toFixed(5) +
                    ", " +
                    pos.coords.longitude.toFixed(5);
            },
            () => alert("Location permission denied")
        );
    }

    /* Open maps */
    if (e.target.classList.contains("map-btn")) {
        window.open("https://www.google.com/maps", "_blank");
    }
});

/* Optional hook */
function setRoute() {
    alert("Route saved successfully");
}
