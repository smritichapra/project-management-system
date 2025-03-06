// Sidebar navigation highlighting
const menuItems = document.querySelectorAll('.sidebar nav ul li a');
menuItems.forEach((link) => {
    link.addEventListener('click', () => {
        menuItems.forEach((menu) => menu.parentElement.classList.remove('active'));
        link.parentElement.classList.add('active');
    });
});

// Navigate to Project Page when profile icon is clicked


// Logout functionality
function logout() {
    window.location.href = "tlogin.html";
}

function navigateToProject(url) {
        window.location.href = url;
    }
function navigateTo(page) {
        window.location.href = page;
    }
// Add a new editable row to the table
function createNewRow() {
    const table = document.getElementById("teamTable").querySelector("tbody");
    const newRow = document.createElement("tr");

    // Generate the new row with editable cells
    newRow.innerHTML = `
        <td>${table.rows.length + 1}</td>
        <td contenteditable="true">Enter Name</td>
        <td contenteditable="true">Enter Class</td>
        <td contenteditable="true">Enter Branch</td>
        <td contenteditable="true">Enter Stu ID</td>
        <td contenteditable="true">Enter Email</td>
        <td contenteditable="true">Enter Phone No.</td>
        <td contenteditable="true">Enter Semester</td>
        <td contenteditable="true">Enter Roll No.</td>
        <td>
            <button onclick="saveRow(this)">Save</button>
            <button onclick="deleteRow(this)">Delete</button>
        </td>
    `;

    table.appendChild(newRow);
}

// Save the content of the editable row
function saveRow(button) {
    const row = button.parentElement.parentElement;
    const cells = row.querySelectorAll("td[contenteditable='true']");

    cells.forEach((cell) => {
        cell.contentEditable = "false";
    });

    alert("Row saved successfully!");
}

// Delete a row from the table
function deleteRow(button) {
    const row = button.parentElement.parentElement;
    row.remove();

    // Reorder row numbers
    const rows = document.querySelectorAll("#teamTable tbody tr");
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}




