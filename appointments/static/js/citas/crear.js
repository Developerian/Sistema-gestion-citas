const abrir = document.getElementById("btn-abrir-crear");
const modal = document.getElementById("modal-crear");
const cerrar = document.getElementById("cerrar-modal-crear");

abrir.addEventListener("click", () => {
    modal.classList.remove("oculto");
});

cerrar.addEventListener("click", () => {
    modal.classList.add("oculto");
});