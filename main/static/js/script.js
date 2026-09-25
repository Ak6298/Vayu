function startWebsite() {
    window.location.href = '/login/';
}

function loginUser(event) {
    if (event) {
        event.preventDefault();
    }

    const username = document.getElementById('username')?.value.trim();
    const password = document.getElementById('password')?.value.trim();
    const message = document.getElementById('login-message');

    if (!username || !password) {
        if (message) {
            message.textContent = 'Please enter both username and password.';
        }
        return;
    }

    if (message) {
        message.textContent = 'Login successful! Redirecting...';
    }

    setTimeout(() => {
        window.location.href = '/home-page/';
    }, 500);
}

function guestLogin() {
    window.location.href = '/guest-home/';
}

function logout() {
    window.location.href = '/logout/';
}
