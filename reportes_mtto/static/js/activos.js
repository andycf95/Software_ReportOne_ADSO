document.addEventListener("DOMContentLoaded", function() {

    const items = document.querySelectorAll(".item-clickable");
    const placeholder = document.getElementById("detalle-placeholder");
    const panel = document.getElementById("detalle-panel");

    items.forEach(item => {
        item.addEventListener("click", function() {
            placeholder.style.display = "none";
            panel.style.display = "block";
            const id = this.dataset.id;
            const tipo = this.dataset.tipo.toLowerCase();

            fetch(`/activos/${tipo}/${id}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("det-nombre").textContent =
                        data.nombre || "-";

                    document.getElementById("det-tipo").textContent =
                        data.tipo || "-";

                    document.getElementById("det-codigo").textContent =
                        data.codigo || "-";

                    document.getElementById("det-padre").textContent =
                        data.activo_padre || "-";

                    document.getElementById("det-sistema-padre").textContent =
                        data.sistema_padre || "-";

                    document.getElementById("det-marca").textContent =
                        data.marca || "-";

                    document.getElementById("det-modelo").textContent =
                        data.modelo || "-";

                    document.getElementById("det-fecha").textContent =
                        data.fecha || "-";

                    document.getElementById("det-icono").className =
                        `bi ${data.icono} fs-2 text-secondary`;

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

});

document.addEventListener("DOMContentLoaded", function () {

    const activo = document.getElementById("id_activo");
    const sistema = document.getElementById("id_sistema");
    const componente = document.getElementById("id_componente");

    if (!activo) return;

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