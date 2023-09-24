
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
        }, 4000);
    });
});

function show(){
    console.log("Filter clicked");
    const optionsContainer = document.querySelector('.options-container');
    const filterContainer = document.querySelector('.filter-container');
    optionsContainer.style.display = optionsContainer.style.display === 'none' ? 'block' : 'none';
    filterContainer.style.display = filterContainer.style.display === 'none' ? 'block' : 'none';
}