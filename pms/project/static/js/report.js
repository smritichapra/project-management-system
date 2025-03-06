// View Full Modal
const viewFullModal = document.getElementById("view-full-modal");
const closeViewModal = document.getElementById("close-view-modal");
const fullReportContent = document.getElementById("full-report-content");

// Add Report Modal
const addReportModal = document.getElementById("add-report-modal");
const closeAddModal = document.getElementById("close-add-modal");
const addReportBtn = document.getElementById("add-report-btn");
const addReportForm = document.getElementById("add-report-form");

// Attach click events to "View Full" buttons
document.querySelectorAll(".view-full-btn").forEach((button) => {
    button.addEventListener("click", () => {
        const reportDetails = button.getAttribute("data-report");
        fullReportContent.textContent = reportDetails;
        viewFullModal.style.display = "flex";
    });
});

// Close View Full Modal
closeViewModal.addEventListener("click", () => {
    viewFullModal.style.display = "none";
});

// Close View Full Modal when clicking outside
window.addEventListener("click", (e) => {
    if (e.target === viewFullModal) {
        viewFullModal.style.display = "none";
    }
});

// Open Add Report Modal
addReportBtn.addEventListener("click", () => {
    addReportModal.style.display = "flex";
});

// Close Add Report Modal
closeAddModal.addEventListener("click", () => {
    addReportModal.style.display = "none";
});

// Close Add Report Modal when clicking outside
window.addEventListener("click", (e) => {
    if (e.target === addReportModal) {
        addReportModal.style.display = "none";
    }
});

// Submit Add Report Form
addReportForm.addEventListener("submit", (e) => {
    e.preventDefault(); // Prevent form submission
    alert("Report submitted successfully!");
    addReportModal.style.display = "none"; // Close the modal
    window.location.href = "report.html"; // Navigate back to report.html
});

// Navigation Function
function navigateTo(page) {
    window.location.href = page;
}


