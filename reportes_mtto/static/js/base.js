document.addEventListener("DOMContentLoaded", function () {

    // Auto cerrar alertas
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            new bootstrap.Alert(alert).close();
        });
    }, 5000);

    // Sidebar responsive
    const btnToggle = document.getElementById("btn-sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.getElementById("sidebar-overlay");

    if (btnToggle) {
        btnToggle.addEventListener("click", function () {
            sidebar.classList.toggle("sidebar-open");
            overlay.classList.toggle("active");
        });

        overlay.addEventListener("click", function () {
            sidebar.classList.remove("sidebar-open");
            overlay.classList.remove("active");
        });

        document.querySelectorAll(".sidebar-nav a").forEach(link => {
            link.addEventListener("click", function () {
                sidebar.classList.remove("sidebar-open");
                overlay.classList.remove("active");
            });
        });
    }





});
