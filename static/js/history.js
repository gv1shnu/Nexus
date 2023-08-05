function clearBrowsingData() {
    // AJAX request to trigger the file deletion
    fetch('/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(() => {
        // Redirect to /history page
        window.location.href = '/history';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}