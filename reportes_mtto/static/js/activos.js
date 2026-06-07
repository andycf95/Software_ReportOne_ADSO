document.addEventListener("DOMContentLoaded", function() {

    // ─── PANEL DE DETALLES DEL ÁRBOL DE ACTIVOS ───
    // Agrega evento de clic a cada elemento del árbol (activo, sistema, componente)
    // para mostrar su información detallada en el panel lateral derecho
    const items = document.querySelectorAll(".item-clickable");
    const placeholder = document.getElementById("detalle-placeholder");
    const panel = document.getElementById("detalle-panel");

    items.forEach(item => {
        item.addEventListener("click", function(e) {

            // Ocultar placeholder y mostrar panel de detalles
            placeholder.style.display = "none";
            panel.style.display = "block";
            
            const id = this.dataset.id;
            const tipo = this.dataset.tipo.toLowerCase();

            // Solicitar los datos del elemento seleccionado al servidor
            fetch(`/activos/${tipo}/${id}/detalle/`)
                .then(response => response.json())
                .then(data => {

                    // Rellenar los campos del panel con los datos recibidos
                    document.getElementById("det-nombre").textContent = data.nombre || "-";
                    document.getElementById("det-tipo").textContent = data.tipo || "-";
                    document.getElementById("det-codigo").textContent = data.codigo || "-";
                    document.getElementById("det-padre").textContent = data.activo_padre || "-";
                    document.getElementById("det-sistema-padre").textContent = data.sistema_padre || "-";
                    document.getElementById("det-marca").textContent = data.marca || "-";
                    document.getElementById("det-modelo").textContent = data.modelo || "-";
                    document.getElementById("det-fecha").textContent = data.fecha || "-";
                    document.getElementById("det-num-ordenes").textContent = data.total_solicitudes || 0;
                    document.getElementById("det-icono").className = `bi ${data.icono} fs-2 text-secondary`;

                    // Actualizar badge de estado operativo con color correspondiente
                    const estadoEl = document.getElementById("det-estado");
                    if (data.estado === "Activo") {
                        estadoEl.textContent = "Operativo";
                        estadoEl.className = "badge bg-success-subtle text-success fw-semibold border border-success-subtle rounded-2";
                    } else if (data.estado === "Fuera de servicio") {
                        estadoEl.textContent = "Fuera de servicio";
                        estadoEl.className = "badge bg-danger-subtle text-danger fw-semibold border border-danger-subtle rounded-2";
                    } else {
                        estadoEl.textContent = "-";
                    }

                    // ─── BOTONES DE ACCIÓN ───
                    const btnSistema = document.getElementById("btn-agregar-sistema");
                    const btnComponente = document.getElementById("btn-agregar-componente");
                    const btnEliminar = document.getElementById("btn-eliminar");
                    const formEliminar = document.getElementById("form-eliminar");
                    const btnEditar = document.getElementById("btn-editar");

                    // Configurar botón editar con la URL correspondiente al tipo seleccionado
                    btnEditar.classList.remove("d-none");
                    btnEditar.href = `/activos/${data.tipo.toLowerCase()}/${data.id}/editar/`;

                    // Configurar formulario de eliminación con la URL correspondiente
                    btnEliminar.classList.remove("d-none");
                    formEliminar.action = `/activos/${data.tipo.toLowerCase()}/${data.id}/eliminar/`;

                    // Ocultar ambos botones de agregar antes de decidir cuál mostrar
                    btnSistema.classList.add("d-none");
                    btnComponente.classList.add("d-none");

                    // Mostrar botón agregar sistema solo cuando se selecciona un activo
                    if (data.tipo === "Activo") {
                        btnSistema.href = `/activos/sistema/${data.id}/nuevo/`;
                        btnSistema.classList.remove("d-none");
                    }

                    // Mostrar botón agregar componente solo cuando se selecciona un sistema
                    if (data.tipo === "Sistema") {
                        btnComponente.href = `/activos/componente/${data.id}/nuevo/`;
                        btnComponente.classList.remove("d-none");
                    }

                    // Actualizar badge de tipo con los colores definidos por el servidor
                    const badge = document.getElementById("det-badge");
                    badge.textContent = data.tipo;
                    badge.style.backgroundColor = data.color;
                    badge.style.color = data.texto;
                })
                .catch(error => {
                    console.error("Error al cargar detalles del activo:", error);
                });
        });
    });

    // Confirmar eliminación al hacer clic en el botón del modal
    document.getElementById("btn-confirmar-eliminar").addEventListener("click", function() {
        document.getElementById("form-eliminar").submit();
    });
});


// ─── CARGA DINÁMICA DE SISTEMAS Y COMPONENTES ───
// Actualiza los selects de sistema y componente mediante AJAX
// cuando el usuario selecciona un activo o sistema en los formularios
document.addEventListener("DOMContentLoaded", function () {

    const activo = document.getElementById("id_activo");
    const sistema = document.getElementById("id_sistema");
    const componente = document.getElementById("id_componente");

    // Si no existen los selects de sistema y componente salir sin hacer nada
    if (!sistema || !componente) return;

    // Al cambiar el activo seleccionado cargar sus sistemas disponibles
    if (activo) {
        activo.addEventListener("change", function () {
            fetch(`/activos/ajax/sistemas/?activo_id=${this.value}`)
                .then(r => r.json())
                .then(data => {
                    // Reiniciar ambos selects antes de cargar los nuevos sistemas
                    sistema.innerHTML = "<option value=''>Seleccione sistema</option>";
                    componente.innerHTML = "<option value=''>Seleccione componente</option>";
                    data.forEach(item => {
                        sistema.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
                    });
                });
        });
    }

    // Al cambiar el sistema seleccionado cargar sus componentes disponibles
    sistema.addEventListener("change", function () {
        fetch(`/activos/ajax/componentes/?sistema_id=${this.value}`)
            .then(r => r.json())
            .then(data => {
                componente.innerHTML = "<option value=''>Seleccione componente</option>";
                data.forEach(item => {
                    componente.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
                });
            });
    });
});