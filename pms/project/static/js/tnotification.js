// Highlight active navigation link
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        navLinks.forEach(nav => nav.classList.remove('active'));
        link.classList.add('active');
    });
});

// Handle form submission for sending notifications
document.querySelector('#notification-form').addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
    const title = document.querySelector('#title').value;
    const description = document.querySelector('#description').value;

    if (title && description) {
        alert(`Notification Sent!\n\nTitle: ${title}\nDescription: ${description}`);
        document.querySelector('#notification-form').reset();
    } else {
        alert('Please fill out all fields!');
    }
});

// Logout functionality
document.querySelector('.logout-btn').addEventListener('click', () => {
    alert('You have logged out!');
});
function navigateTo(page) {
    window.location.href = page;
}

