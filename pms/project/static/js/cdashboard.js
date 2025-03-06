// Function to show the groups page by default
function showPage(pageId) {
    // Hide all sections except groups
    document.querySelectorAll(".page").forEach(page => {
        page.style.display = "none";
    });

    // Show only groups section
    document.getElementById(pageId).style.display = "block";

    // Update active state in the sidebar
    document.querySelectorAll(".sidebar ul li a").forEach(link => {
        link.classList.remove("active");
    });

    event.currentTarget.classList.add("active");
}

// Show the "Groups" page by default when the dashboard loads
document.addEventListener("DOMContentLoaded", () => {
    showPage('groups');
});

