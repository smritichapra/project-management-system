// Logout Functionality
function logout() {
    // Redirect to login page
    window.location.href = "tlogin.html";
}

// Handle Report Submission
document.getElementById('report-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const recipient = document.getElementById('recipient').value;
    const description = document.getElementById('description').value;

    if (recipient && description) {
        alert(`Report sent to: ${recipient}\nDescription: ${description}`);
        // Reset the form
        document.getElementById('report-form').reset();
    } else {
        alert('Please fill in all fields.');
    }
});
function navigateTo(page) {
    window.location.href = page;
}