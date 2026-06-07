document.addEventListener("DOMContentLoaded", function () {

    // Variables globales del módulo de usuarios
    let activosData = [];      // Almacena la lista de activos cargada desde el servidor
    let usuarioIdActual = null; // ID del técnico seleccionado actualmente

    // ─── MODAL ASIGNAR ACTIVO ───
    // Al hacer clic en el botón de asignar activo de un técnico:
    // carga los activos disponibles y configura el modal
    document.querySelectorAll('.btn-asignar-activo').forEach(btn => {
        btn.addEventListener('click', function() {
            usuarioIdActual = this.dataset.id;

            // Mostrar el nombre del técnico en el encabezado del modal
            document.getElementById('modal-nombre-tecnico').textContent = this.dataset.nombre;

            // Configurar la URL de los formularios de asignar y desasignar
            const url = `/usuarios/${usuarioIdActual}/asignar-activo/`;
            document.getElementById('form-asignar-activo').action = url;
            document.getElementById('form-desasignar').action = url;

            // Limpiar el estado del modal antes de abrirlo
            document.getElementById('input-buscar-activo').value = '';
            document.getElementById('activo-seleccionado-info').style.display = 'none';
            document.getElementById('btn-confirmar-asignar').disabled = true;
            document.getElementById('input-activo-id').value = '';

            // Cargar la lista de activos desde el servidor via AJAX
            fetch(url)
                .then(r => r.json())
                .then(data => {
                    activosData = data.activos;
                    renderActivos(activosData);
                });
        });
    });

    // Renderiza la lista de activos en el modal
    // Muestra activos disponibles como seleccionables y ocupados como deshabilitados
    window.renderActivos = function(activos) {
        const lista = document.getElementById('lista-activos-modal');
        if (!lista) return;
        lista.innerHTML = '';

        activos.forEach(activo => {
            const div = document.createElement('div');
            div.style.cssText = 'padding: 10px 12px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between;';

            if (!activo.ocupado) {
                // Activo disponible: permite selección y cambia color al hacer hover
                div.style.cursor = 'pointer';
                div.onclick = () => seleccionarActivo(activo.id, activo.nombre);
                div.onmouseover = () => div.style.background = '#1e293b';
                div.onmouseout = () => div.style.background = 'transparent';
            } else {
                // Activo ocupado: se muestra semitransparente y no es seleccionable
                div.style.opacity = '0.5';
            }

            // Construir el HTML de cada fila con nombre, código y badge de estado
            div.innerHTML = `
                <div>
                    <p style="font-size: 13px; font-weight: 600; color: #e2e8f0; margin: 0;">${activo.nombre}</p>
                    <small style="color: #64748b;">${activo.codigo}${activo.tecnico ? ' · Asignado a: ' + activo.tecnico : ''}</small>
                </div>
                <span class="badge" style="font-size: 11px; ${activo.ocupado ?
                    'background:rgba(239,68,68,0.15); color:#f87171;' :
                    'background:rgba(34,197,94,0.15); color:#4ade80;'}">
                    ${activo.ocupado ? 'Ocupado' : 'Disponible'}
                </span>`;
            lista.appendChild(div);
        });
    }

    // Filtra la lista de activos en tiempo real según el texto ingresado en el buscador
    window.filtrarActivos = function(val) {
        const filtrados = activosData.filter(a =>
            a.nombre.toLowerCase().includes(val.toLowerCase())
        );
        renderActivos(filtrados);
    }

    // Marca un activo como seleccionado y habilita el botón de confirmar asignación
    window.seleccionarActivo = function(id, nombre) {
        document.getElementById('input-activo-id').value = id;
        document.getElementById('nombre-activo-seleccionado').textContent = nombre;
        document.getElementById('activo-seleccionado-info').style.display = 'block';
        document.getElementById('btn-confirmar-asignar').disabled = false;
    }

    // ─── MODAL CAMBIAR CONTRASEÑA ───
    // Al hacer clic en el botón de cambiar contraseña de un usuario:
    // configura el modal con el nombre del usuario y la URL del formulario
    document.querySelectorAll('.btn-cambiar-contrasena').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = document.getElementById('modal-nombre-contrasena');
            const form = document.getElementById('form-cambiar-contrasena');
            if (modal) modal.textContent = this.dataset.nombre;
            if (form) form.action = `/usuarios/${this.dataset.id}/cambiar-contrasena/`;
        });
    });

});