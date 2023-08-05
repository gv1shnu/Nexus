document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function() {
        document.getElementById('wait-message').style.display = 'block';
    });
});