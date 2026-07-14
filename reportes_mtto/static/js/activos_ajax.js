// ─── CARGA DINÁMICA DE SISTEMAS Y COMPONENTES ───
// Actualiza los selects de sistema y componente mediante AJAX
// cuando el usuario selecciona un activo o sistema en los formularios
// ─── CARGA DINÁMICA DE SISTEMAS Y COMPONENTES ───
document.addEventListener("DOMContentLoaded", function () {

    const config     = document.getElementById("ajax-config");
    const activo     = document.getElementById("id_activo");
    const sistema    = document.getElementById("id_sistema");
    const componente = document.getElementById("id_componente");

    // Si no existen los selects salir sin hacer nada
    if (!sistema || !componente) return;

    const urlSistemas    = config?.dataset.urlSistemas    || "/activos/ajax/sistemas/";
    const urlComponentes = config?.dataset.urlComponentes || "/activos/ajax/componentes/";
    const activoIdTecnico = config?.dataset.activoId || null;

    // ── Función reutilizable para cargar sistemas ──
    function cargarSistemas(activoId) {
        if (!activoId) return;
        fetch(`${urlSistemas}?activo_id=${activoId}`)
            .then(r => r.json())
            .then(data => {
                sistema.innerHTML = "<option value=''>Seleccione sistema</option>";
                componente.innerHTML = "<option value=''>Seleccione componente</option>";
                data.forEach(item => {
                    sistema.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
                });
            })
            .catch(err => console.warn("Error cargando sistemas:", err));
    }

    // ── Función reutilizable para cargar componentes ──
    function cargarComponentes(sistemaId) {
        if (!sistemaId) return;
        fetch(`${urlComponentes}?sistema_id=${sistemaId}`)
            .then(r => r.json())
            .then(data => {
                componente.innerHTML = "<option value=''>Seleccione componente</option>";
                data.forEach(item => {
                    componente.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
                });
            })
            .catch(err => console.warn("Error cargando componentes:", err));
    }

    // ── Si es técnico cargar sistemas automáticamente al abrir el form ──
    if (activoIdTecnico) {
        cargarSistemas(activoIdTecnico);
    }

    // ── Al cambiar el activo cargar sus sistemas ──
    if (activo) {
        activo.addEventListener("change", function () {
            cargarSistemas(this.value);
        });
    }

    // ── Al cambiar el sistema cargar sus componentes ──
    sistema.addEventListener("change", function () {
        cargarComponentes(this.value);
    });

});