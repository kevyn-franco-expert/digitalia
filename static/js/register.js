document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    if (!validateEmail(email)) {
        // alert('Please enter a valid email.');
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please enter a valid email.'
        });
        return;
    }
    if (!validatePassword(password)) {
        // alert('The password must be at least 8 characters.');
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'The password must be at least 8 characters.'
        });
        return;
    }

    fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.detail === 'Registration successful') {
                window.location.href = '/';
            } else {
                alert('Error: ' + data.detail);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

function validateEmail(email) {
    var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}
