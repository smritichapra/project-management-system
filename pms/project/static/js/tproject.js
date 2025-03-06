// Go back to the previous page
function goBack() {
    history.back();
}

// Form submission handling
// document.getElementById("projectForm").addEventListener("submit", function (event) {
//     event.preventDefault();

//     const projectName = document.getElementById("projectName").value;
//     const description = document.getElementById("description").value;
//     const techStack = document.getElementById("techStack").value;

//     if (projectName && description && techStack) {
//         alert(`Project Submitted!\n\nName: ${projectName}\nDescription: ${description}\nTech Stack: ${techStack}`);
        
//         // Redirect to the dashboard page after submission
//         window.location.href = "tdashboard.html";
//     } else {
//         alert("Please fill out all fields.");
//     }
// });
document.getElementById('projectForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("/add_project/", {  // URL from urls.py
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Project added successfully!");
            window.location.href = "/dashboard/";  // Redirect after success
        } else {
            alert("Error submitting project.");
        }
    })
    .catch(error => console.error("Error:", error));
});


