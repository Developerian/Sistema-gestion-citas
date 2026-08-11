document.body.addEventListener('click', (evento) => {

    const abrir = evento.target.closest('[data-abrir-modal]');

    if (abrir) {

        const modal = document.getElementById(
            abrir.dataset.abrirModal
        );

        if (!modal) {
            console.error(
                `No existe el modal: ${abrir.dataset.abrirModal}`
            );
            return;
        }

        // Si el botón tiene una URL de acción
        const url = abrir.dataset.url;

        if (url) {
            const formulario = modal.querySelector('form');

            if (formulario) {
                formulario.action = url;
            }
        }

        modal.classList.remove('oculto');
    }


    const cerrar = evento.target.closest('[data-cerrar-modal]');

    if (cerrar) {
        cerrar.closest('.modal').classList.add('oculto');
    }

});