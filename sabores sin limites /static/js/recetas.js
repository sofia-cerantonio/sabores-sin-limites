document.addEventListener("DOMContentLoaded", () => {
    // Referencias a elementos del DOM
    const searchInput = document.getElementById("q");
    const searchButton = document.getElementById("searchBtn");
    const filters = document.querySelectorAll(".filter-cb");
    
    // 🎯 CAMBIO CRÍTICO 1: Seleccionar las nuevas estructuras de receta (div.row)
    // Asumimos que están en un contenedor con ID, o seleccionamos todas las .row que tienen data-type
    // Si usaste <div id="recipesList">, selecciona sus hijos directos:
    const cards = document.querySelectorAll("#recipesList > .row"); 

    /**
     * Función principal para aplicar el filtro y la búsqueda.
     * Se llama cada vez que cambia un filtro o se realiza una búsqueda.
     */
    const applyFiltersAndSearch = () => {
        // 1. Obtener filtros activos (Checkbox)
        const activeFilters = Array.from(filters)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // 2. Obtener el valor de la búsqueda (Input)
        const searchQuery = searchInput.value.toLowerCase().trim();

        // 3. Iterar sobre todas las "tarjetas" (ahora filas de Bootstrap)
        cards.forEach(card => {
            // Obtiene 'sin lactosa,diabetes,...' (Funciona igual con data-type en el div.row)
            const cardType = card.dataset.type || ''; 
            
            // 🎯 OBTENCIÓN DE CONTENIDO: Buscar el contenido dentro de la columna de texto (col-md-8).
            // Asumimos que el contenido de texto está en el SEGUNDO hijo de .row (índice 1)
            const contentContainer = card.children[1]; 
            
            // Si el contenedor de contenido es válido, extraemos título y descripción
            if (contentContainer) {
                const cardTitle = contentContainer.querySelector('h3').textContent.toLowerCase();
                const cardDescription = contentContainer.querySelector('p').textContent.toLowerCase();
                
                // ----------------------------------------------------
                // Criterio 1: Coincidencia de Filtros (Checkbox)
                // ----------------------------------------------------
                const matchesFilters = activeFilters.every(filter => 
                    // Nota: Asegúrate que 'cardType' en la DB use comas o espacios si hay múltiples valores.
                    cardType.includes(filter)
                );

                // ----------------------------------------------------
                // Criterio 2: Coincidencia de Búsqueda (Input)
                // ----------------------------------------------------
                const matchesSearch = !searchQuery || 
                                    cardTitle.includes(searchQuery) ||
                                    cardDescription.includes(searchQuery);

                // ----------------------------------------------------
                // Mostrar/Ocultar
                // ----------------------------------------------------
                // La tarjeta se muestra si cumple AMBOS criterios
                if (matchesFilters && matchesSearch) {
                    // 🎯 CAMBIO CRÍTICO 2: Las filas de Bootstrap usan display: flex
                    card.style.display = "flex"; 
                } else {
                    card.style.display = "none";
                }
            } else {
                // Si la estructura no es la esperada, por seguridad, ocultar
                card.style.display = "none";
            }
        });
    };

    // --- Event Listeners (SIN CAMBIOS) ---

    // 1. Eventos para los Checkboxes (Cambio)
    filters.forEach(filter => {
      filter.addEventListener("change", applyFiltersAndSearch);
    });

    // 2. Evento para el Botón Buscar (Click)
    searchButton.addEventListener("click", applyFiltersAndSearch);

    // 3. Evento para el campo de Búsqueda (Tecla Enter)
    searchInput.addEventListener("keyup", (event) => {
        if (event.key === 'Enter') {
            applyFiltersAndSearch();
        }
    });

    // Ejecutar al cargar para asegurar que los filtros iniciales se apliquen (si es necesario)
    // applyFiltersAndSearch(); 
});