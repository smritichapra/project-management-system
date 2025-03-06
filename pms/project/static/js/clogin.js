// Function to navigate to the dashboard page


// Add event listener for the Sign-up link


// Form submission event
// Function to navigate to the dashboard page
function navigateTo(page) {
    window.location.href = page;
}

// Add event listener for the Sign-up link
document.getElementById("signup-link").addEventListener("click", function(event) {
    event.preventDefault();  // Prevent default anchor behavior
    navigateTo("signup.html");
});

// Form submission event
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email && password) {
        window.location.href = cdashboardURL
    } else {
        alert("Please enter valid credentials.");
    }
});

