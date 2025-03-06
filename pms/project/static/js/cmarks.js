// Predefined student data
const students = [
    { name: "Alice Johnson", roll: "101", branch: "CSE", mentor: "Dr. Smith" },
    { name: "Bob Williams", roll: "102", branch: "ECE", mentor: "Dr. Brown" },
    { name: "Charlie Davis", roll: "103", branch: "ME", mentor: "Dr. Clark" }
];

// Function to load students into the table
function loadStudents() {
    let table = document.getElementById("marksTable").getElementsByTagName('tbody')[0];

    students.forEach(student => {
        let row = table.insertRow();

        row.insertCell(0).textContent = student.name;
        row.insertCell(1).textContent = student.roll;
        row.insertCell(2).textContent = student.branch;
        row.insertCell(3).textContent = student.mentor;

        // Create input fields for marks
        ["ia1", "ia2", "external"].forEach(() => {
            let cell = row.insertCell();
            let input = document.createElement("input");
            input.type = "number";
            input.min = "0";
            input.max = "100";
            input.placeholder = "Enter Marks";
            cell.appendChild(input);
        });

        // Add Save button
        let actionCell = row.insertCell();
        let saveBtn = document.createElement("button");
        saveBtn.textContent = "Save";
        saveBtn.onclick = function () {
            saveMarks(row);
        };
        actionCell.appendChild(saveBtn);
    });
}

// Function to save marks
function saveMarks(row) {
    let inputs = row.querySelectorAll("input");
    let marks = {
        ia1: inputs[0].value,
        ia2: inputs[1].value,
        external: inputs[2].value
    };
    
    console.log("Marks Saved:", marks);
    alert("Marks saved successfully!");
}

// Load students on page load
window.onload = loadStudents;
