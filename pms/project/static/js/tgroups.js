document.addEventListener("DOMContentLoaded", () => {
    console.log("Groups Dashboard Loaded Successfully!");
});

// Logout functionality
document.querySelector('.logout-btn').addEventListener('click', () => {
    alert('You have logged out!');
    // Navigate to login page
    window.location.href = "tlogin.html";
});


