document.getElementById("login-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email && password) {
        // Simulate successful login
        alert("Login Successful!");
        window.location.href = dashboardURL;
    } else {
        alert("Please enter both email and password!");
    }
});
