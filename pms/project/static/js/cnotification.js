function sendNotification() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const fileInput = document.getElementById("file-input").files[0];

    if (title === "" || description === "") {
        alert("Please fill in both title and description.");
        return;
    }

    alert(`Notification sent!\n\nTitle: ${title}\nDescription: ${description}\nFile: ${fileInput ? fileInput.name : "No file uploaded"}`);
}

function goBack() {
    window.location.href = "cgroups.html";
}

function viewProposals() {
    window.location.href = "cproposals.html";
}
