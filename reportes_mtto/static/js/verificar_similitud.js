// =====================================================
// FIXLY — Formulario de Solicitud
// Verificación de similitud antes de guardar
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const form    = document.getElementById("form-solicitud");
    const config  = document.getElementById("ajax-config");

    if (!form || !config) return;

    const esEdicion    = config.dataset.esEdicion === "true";
    const urlSimilitud = config.dataset.urlSimilitud;

    let similitudVerificada = false;

    // ── INTERCEPTAR SUBMIT ────────────────────────────────────────
    form.addEventListener("submit", function (e) {

        // Si es edición o ya se verificó similitud, dejar pasar
        if (esEdicion || similitudVerificada) return;

        e.preventDefault();

        const titulo       = document.getElementById("id_titulo")?.value.trim() || "";
        const descripcion  = document.getElementById("id_descripcion")?.value.trim() || "";
        const activoId     = document.getElementById("id_activo")?.value
                          || document.querySelector("input[name='activo']")?.value
                          || null;
        const sistemaId    = document.getElementById("id_sistema")?.value    || null;
        const componenteId = document.getElementById("id_componente")?.value || null;

        // Si el título es muy corto enviar sin verificar
        if (titulo.length < 5) {
            similitudVerificada = true;
            form.submit();
            return;
        }

        // Enviar al endpoint de verificación
        fetch(urlSimilitud, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify({
                titulo,
                descripcion,
                activo_id:     activoId,
                sistema_id:    sistemaId,
                componente_id: componenteId
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.similares && data.similares.length > 0) {
                renderSimilares(data.similares);
                new bootstrap.Modal(document.getElementById("modalSimilitud")).show();
            } else {
                similitudVerificada = true;
                form.submit();
            }
        })
        .catch(() => {
            similitudVerificada = true;
            form.submit();
        });
    });

    // ── BOTÓN CONTINUAR DE TODAS FORMAS ──────────────────────────
    const btnContinuar = document.getElementById("btn-continuar-de-todas-formas");
    if (btnContinuar) {
        btnContinuar.addEventListener("click", function () {
            const modal = bootstrap.Modal.getInstance(
                document.getElementById("modalSimilitud")
            );
            if (modal) modal.hide();
            similitudVerificada = true;
            form.submit();
        });
    }

    // ── RENDERIZAR TABLA DE SIMILARES ─────────────────────────────
    function renderSimilares(similares) {
        const tbody = document.getElementById("tabla-similares");
        if (!tbody) return;
        tbody.innerHTML = "";

        similares.forEach(s => {
            const color = s.nivel === "duplicado" ? "#f87171"
                        : s.nivel === "alto"      ? "#f97316"
                        : "#fbbf24";

            const fila = `
                <tr style="cursor:pointer;"
                    onclick="window.open('/solicitudes/solicitud/${s.id}/', '_blank')">
                    <td class="fw-semibold" style="color:var(--accent);">${s.codigo}</td>
                    <td>${s.titulo}</td>
                    <td><small class="text-muted">${s.activo}</small></td>
                    <td>
                        <span class="badge"
                              style="background-color:rgba(148,163,184,0.15);
                                     color:#94a3b8;
                                     border:1px solid rgba(148,163,184,0.3);">
                            ${s.estado}
                        </span>
                    </td>
                    <td>
                        <div class="d-flex align-items-center gap-2">
                            <span class="fw-bold"
                                  style="color:${color}; min-width:36px;">
                                ${s.score}%
                            </span>
                            <small style="color:${color};">${s.etiqueta}</small>
                        </div>
                    </td>
                </tr>`;
            tbody.insertAdjacentHTML("beforeend", fila);
        });
    }

});