function navigateTo(page) {
    window.location.href = page;
}

function validateForm() {
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;

    const emailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid Gmail address (example@gmail.com)");
        return false;
    }

    if (phone.length !== 10 || isNaN(phone)) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }

    alert("Team member added successfully!");
    return true;
}
