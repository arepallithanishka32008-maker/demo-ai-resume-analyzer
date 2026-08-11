function getStarted() {
    alert("Welcome! Please login to continue.");
}

function loginSuccess() {
    alert("Login Successful!");
    window.location.href = "upload.html";
}

function registerSuccess() {
    alert("Registration Successful!");
    window.location.href = "login.html";
}

function uploadSuccess() {
    alert("Resume Uploaded Successfully!");
    window.location.href = "result.html";
}

function messageSent() {
    alert("Thank you! Your message has been sent.");
}