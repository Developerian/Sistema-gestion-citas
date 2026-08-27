document.addEventListener('DOMContentLoaded', function () {
    // Usamos delegación de eventos en el documento para garantizar que siempre funcione
    document.addEventListener('change', function (event) {
        
        // 1. Si el usuario hace clic en el checkbox principal ("Seleccionar todo")
        if (event.target && event.target.id === 'select-all') {
            const selectAll = event.target;
            const rowCheckboxes = document.querySelectorAll('.row-checkbox');
            
            rowCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAll.checked;
            });
        }

        // 2. Si el usuario desmarca manualmente un checkbox individual
        if (event.target && event.target.classList.contains('row-checkbox')) {
            const selectAll = document.getElementById('select-all');
            if (selectAll) {
                const rowCheckboxes = document.querySelectorAll('.row-checkbox');
                // Verificar si todos están marcados
                const total = rowCheckboxes.length;
                const checkedCount = document.querySelectorAll('.row-checkbox:checked').length;
                
                // Marca 'select-all' solo si todos están activos
                selectAll.checked = (total === checkedCount);
            }
        }
    });
});