document.addEventListener("DOMContentLoaded", () => {

    const botonesEliminar = document.querySelectorAll(".btn-open-delete");
    const modal = document.getElementById("modalEliminar");
    const cerrar = document.getElementById("cerrarModal");
    const formulario = document.getElementById("formEliminar");


    botonesEliminar.forEach(boton => {

        boton.addEventListener("click", () => {

            const id = boton.dataset.id;

            formulario.action = boton.dataset.url;

            modal.classList.remove("oculto");

        });

    });


    cerrar.addEventListener("click", () => {

        modal.classList.add("oculto");

    });

});