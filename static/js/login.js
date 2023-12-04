document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.detail === 'Login successful') {
                window.location.href = '/room/';
            } else {
                // alert('Invalid credentials');
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Invalid credentials.'
                });
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});