function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true,
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
    
    const timeElements = document.querySelectorAll('#current-time');
    timeElements.forEach(el => {
        el.textContent = timeString;
    });
}

setInterval(updateTime, 1000);
updateTime();

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});