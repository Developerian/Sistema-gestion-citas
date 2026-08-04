document.addEventListener("DOMContentLoaded", () => {

    const botonesEliminar = document.querySelectorAll(".btn-open-delete");
    const modal = document.getElementById("modalEliminar");
    const cerrar = document.getElementById("cerrarModal");

    botonesEliminar.forEach(boton => {

        boton.addEventListener("click", () => {

            const id = boton.dataset.id;

            modal.classList.remove("oculto");

        });

    });


    cerrar.addEventListener("click", () => {

        modal.classList.add("oculto");

    });

});