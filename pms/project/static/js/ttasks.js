// Sidebar navigation highlighting
const menuItems = document.querySelectorAll('.sidebar nav ul li');
menuItems.forEach((item) => {
    item.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default navigation
        menuItems.forEach((menu) => menu.classList.remove('active'));
        item.classList.add('active');

        // Navigate to the corresponding page
        const targetPage = item.querySelector('a').getAttribute('href');
        window.location.href = targetPage;
    });
});

// Logout functionality
function logout() {
    alert('You have logged out!');
    window.location.href = "tlogin.html"; // Redirect to the login page
}

// Status change functionality for Tasks
document.querySelectorAll('select').forEach((select) => {
    select.addEventListener('change', (event) => {
        const status = event.target.value;
        alert(`Status changed to: ${status}`);
    });
});




