document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById('taskInput');

    const autoResize = () => {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    };

    textarea.addEventListener('input', autoResize);
    autoResize();  // Trigger resize saat halaman dimuat
});