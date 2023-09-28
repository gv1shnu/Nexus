
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const msgContainer = document.getElementById('wait-message');
    const gifContainer = document.getElementById('wait-gif');
    form.addEventListener('submit', function() {
        setTimeout(function() {
            msgContainer.style.display = 'block';
        }, 1000);
        setTimeout(function() {
            gifContainer.style.display = 'block';
        }, 6000);
    });
});

function show(){
    const optionsContainer = document.querySelector('.options-container');
    const filterContainer = document.querySelector('.filter-container');

    optionsContainer.style.display = optionsContainer.style.display === 'none' || optionsContainer.style.display === '' ? 'block' : 'none';
    filterContainer.style.display = filterContainer.style.display === 'none' || filterContainer.style.display === '' ? 'block' : 'none';
}