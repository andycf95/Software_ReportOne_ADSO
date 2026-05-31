document.addEventListener("DOMContentLoaded", function() {

    const items = document.querySelectorAll(".item-clickable");
    const placeholder = document.getElementById("detalle-placeholder");
    const panel = document.getElementById("detalle-panel");

    items.forEach(item => {
        item.addEventListener("click", function(e) {
            placeholder.style.display = "none";
            panel.style.display = "block";
            
            const id = this.dataset.id;
            const tipo = this.dataset.tipo.toLowerCase();

            fetch(`/activos/${tipo}/${id}/detalle/`)
                .then(response => response.json())
                .then(data => {
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

                    const estadoEl = document.getElementById("det-estado");
                        if (data.estado === "Activo") {
                            estadoEl.textContent = "Operativo";
                            estadoEl.className = "badge bg-success-subtle text-success fw-semibold border border-success-subtle rounded-2";
                        } else if(data.estado==="Fuera de servicio"){
                            estadoEl.textContent = "Fuera de servicio";
                            estadoEl.className = "badge bg-danger-subtle text-danger fw-semibold border border-danger-subtle rounded-2";
                        }                   
                        else {
                            
                            estadoEl.textContent = "-";
                        }

                    const btnSistema = document.getElementById("btn-agregar-sistema");
                    const btnComponente = document.getElementById("btn-agregar-componente");
                    // Botón eliminar - siempre visible al seleccionar cualquier elemento
                    const btnEliminar = document.getElementById("btn-eliminar");
                    const formEliminar = document.getElementById("form-eliminar");
                    //Boton para editaar
                    const btnEditar = document.getElementById("btn-editar");
                    btnEditar.classList.remove("d-none");
                    btnEditar.href = `/activos/${data.tipo.toLowerCase()}/${data.id}/editar/`;

                    btnEliminar.classList.remove("d-none");
                    formEliminar.action = `/activos/${data.tipo.toLowerCase()}/${data.id}/eliminar/`;
                    // Ocultar ambos primero
                    btnSistema.classList.add("d-none");
                    btnComponente.classList.add("d-none");

                    // Mostrar el que corresponde
                    if (data.tipo === "Activo") {
                        btnSistema.href = `/activos/sistema/${data.id}/nuevo/`;
                        btnSistema.classList.remove("d-none");
                    }

                    if (data.tipo === "Sistema") {
                        btnComponente.href = `/activos/componente/${data.id}/nuevo/`;
                        btnComponente.classList.remove("d-none");
                    }

                    const badge = document.getElementById("det-badge");
                    badge.textContent = data.tipo;
                    badge.style.backgroundColor = data.color;
                    badge.style.color = data.texto;
                })
                .catch(error => {
                    console.error(error);
                });
        });
    });
    // Confirmar eliminación desde el modal
        document.getElementById("btn-confirmar-eliminar").addEventListener("click", function() {
            document.getElementById("form-eliminar").submit();
});
});

// Hacer que al cambiar el activo, se actualicen los sistemas disponibles y al cambiar el sistema, se actualicen los componentes disponibles en los formularios de creación de sistema y componente respectivamente

document.addEventListener("DOMContentLoaded", function () {

    const activo = document.getElementById("id_activo");
    const sistema = document.getElementById("id_sistema");
    const componente = document.getElementById("id_componente");

    if (!activo) return;
    // Al cambiar el activo, actualizar los sistemas disponibles
    activo.addEventListener("change", function () {

        fetch(`/activos/ajax/sistemas/?activo_id=${this.value}`)
            .then(r => r.json())
            .then(data => {

                sistema.innerHTML = "<option value=''>Seleccione sistema</option>";
                componente.innerHTML = "<option value=''>Seleccione componente</option>";

                data.forEach(item => {
                    sistema.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
                });

            });
    });
    // Al cambiar el sistema, actualizar los componentes disponibles
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

