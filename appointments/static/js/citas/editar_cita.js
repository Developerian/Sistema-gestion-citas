document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("modal-editar");
    const contenido = document.getElementById("contenido-modal");
    const cerrar = document.getElementById("cerrar-modal");

    document.querySelectorAll(".btn-open-update").forEach(boton => {

        boton.addEventListener("click", () => {

            const id = boton.dataset.id;

            modal.classList.remove("oculto");

            contenido.innerHTML = "<p>Cargando...</p>";

            fetch(`/dashboard/citas/${id}/editar/`)
                .then(response => response.text())
                .then(html => {

                    contenido.innerHTML = html;

                });

        });

    });


    cerrar.addEventListener("click", () => {

        modal.classList.add("oculto");

    });

});