const routesDiv = document.getElementById("routes");
const nextBtn = document.getElementById("next-btn");

/* Toggle dropdown */
routesDiv.addEventListener("click", (e) => {
    /* Toggle dropdown when choose stop button is clicked */
    if (e.target.classList.contains("choose-stop-btn")) {
        const dropdown = e.target.closest(".stop-dropdown");
        
        // Close all other dropdowns
        document.querySelectorAll(".stop-dropdown").forEach(d => {
            if (d !== dropdown) d.classList.remove("active");
        });
        
        // Toggle current dropdown
        dropdown.classList.toggle("active");
    }
    
    /* Select stop from dropdown */
    if (e.target.classList.contains("stop-option")) {
        const stopName = e.target.getAttribute("data-stop");
        const input = e.target.closest(".route-box").querySelector("input");
        input.value = stopName;
        
        // Close dropdown
        e.target.closest(".stop-dropdown").classList.remove("active");
    }
    
    /* Open maps */
    if (e.target.classList.contains("map-btn")) {
        window.open("https://www.google.com/maps", "_blank");
    }
});

/* Close dropdown when clicking outside */
document.addEventListener("click", (e) => {
    if (!e.target.closest(".stop-dropdown")) {
        document.querySelectorAll(".stop-dropdown").forEach(d => {
            d.classList.remove("active");
        });
    }
});

/* Next button handler */
if (nextBtn) {
    nextBtn.addEventListener("click", () => {
        window.location.href = "/addinfo/";
    });
}