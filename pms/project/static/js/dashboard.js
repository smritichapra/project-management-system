// Highlight the active menu item
const menuItems = document.querySelectorAll('.menu ul li');
menuItems.forEach(item => {
    item.addEventListener('click', () => {
        menuItems.forEach(menu => menu.classList.remove('active'));
        item.classList.add('active');
    });
});

// Navigate to other pages
function navigateTo(page) {
    window.location.href = page;
}

// Logout button functionality
function logout() {
    alert('You have logged out!');
    window.location.href = 'Mlogin.html'; // Navigate to login page
}

