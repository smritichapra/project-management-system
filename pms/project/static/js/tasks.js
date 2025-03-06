// Sidebar navigation highlighting
const menuItems = document.querySelectorAll('.sidebar nav ul li');
menuItems.forEach((item) => {
    item.addEventListener('click', () => {
        menuItems.forEach((menu) => menu.classList.remove('active'));
        item.classList.add('active');
    });
});

// Logout functionality
document.querySelector('.logout-btn').addEventListener('click', () => {
    alert('You have logged out!');
});

// Navigation Function
function navigateTo(page) {
    window.location.href = page;
}

// Open Add Task Form Modal
function openAddTaskForm() {
    document.getElementById('add-task-modal').style.display = 'flex';
}

// Close Add Task Form Modal
function closeAddTaskForm() {
    document.getElementById('add-task-modal').style.display = 'none';
}

// Add Task Functionality
function addTask(event) {
    event.preventDefault();

    const title = document.getElementById('document-title').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];

    // Add new task to table
    const table = document.getElementById('tasks-list');
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${title}</td>
        <td>${startDate}</td>
        <td>${endDate}</td>
        <td>
            ${file ? `<a href="#" class="view-file-link" onclick="viewFile('${file.name}')">View File</a>` : ''}
        </td>
        <td>
            <button class="view-submissions-btn" onclick="openSubmissionsModal()">View Submissions</button>
        </td>
    `;
    table.appendChild(row);

    // Reset form and close modal
    document.getElementById('add-task-form').reset();
    closeAddTaskForm();
}

// View Attached File
function viewFile(fileName) {
    alert(`Viewing file: ${fileName}`);
}

// Open Submissions Modal
function openSubmissionsModal() {
    document.getElementById('submissions-modal').style.display = 'flex';
}

// Close Submissions Modal
function closeSubmissionsModal() {
    document.getElementById('submissions-modal').style.display = 'none';
}