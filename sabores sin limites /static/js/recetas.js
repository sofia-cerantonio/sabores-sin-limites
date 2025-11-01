document.addEventListener("DOMContentLoaded", () => {
    // Referencias a elementos del DOM
    const searchInput = document.getElementById("q");
    const searchButton = document.getElementById("searchBtn");
    // Seleccionamos todos los botones dentro del grupo de filtros
    const filterButtons = document.querySelectorAll(".btn-group .btn"); 
    // Seleccionamos todas las tarjetas de receta (las filas)
    const cards = document.querySelectorAll("#recipesList > .row"); 

    // Estado actual de la búsqueda y el filtro
    let currentSearchQuery = '';
    let currentDietFilter = 'all'; 

    /**
     * Función principal para aplicar el filtro de dieta y la búsqueda.
     */
    const applyFiltersAndSearch = () => {
        // Normalizar la consulta de búsqueda
        const searchQuery = currentSearchQuery.toLowerCase().trim();
        const activeDiet = currentDietFilter;

        cards.forEach(card => {
            // Obtiene 'sin-lactosa,diabetes,...' del atributo data-type
            const cardType = card.dataset.type || ''; 
            
            // Obtener el contenido de texto (Título y Descripción)
            const contentContainer = card.children[1]; 
            const cardTitle = contentContainer ? contentContainer.querySelector('h3').textContent.toLowerCase() : '';
            const cardDescription = contentContainer ? contentContainer.querySelector('p').textContent.toLowerCase() : '';

            // ----------------------------------------------------
            // Criterio 1: Coincidencia de Filtros de Dieta (Botones)
            // ----------------------------------------------------
            let matchesDiet = (activeDiet === 'all') || cardType.includes(activeDiet);

            // ----------------------------------------------------
            // Criterio 2: Coincidencia de Búsqueda (Input)
            // ----------------------------------------------------
            const matchesSearch = !searchQuery ||
                                  cardTitle.includes(searchQuery) ||
                                  cardDescription.includes(searchQuery);

            // ----------------------------------------------------
            // Mostrar/Ocultar
            // ----------------------------------------------------
            if (matchesDiet && matchesSearch) {
                card.style.display = "flex"; 
            } else {
                card.style.display = "none";
            }
        });
    };

    // --- Event Listeners para la Búsqueda ---
    searchInput.addEventListener("input", (event) => {
        // Actualiza la búsqueda en tiempo real
        currentSearchQuery = event.target.value;
        applyFiltersAndSearch();
    });
    
    // Evento para el botón Buscar (si lo mantuviste)
    if (searchButton) {
        searchButton.addEventListener("click", applyFiltersAndSearch);
    }


    // --- Event Listeners para el Filtrado de Dieta (Botones) ---
    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Normalizar el texto del botón al formato de la DB (sin-lactosa, diabetes, etc.)
            let newFilterValue = button.textContent.toLowerCase().trim();
            
            if (newFilterValue === 'todos') {
                newFilterValue = 'all';
            } else if (newFilterValue.includes('sin lactosa')) {
                newFilterValue = 'sin-lactosa';
            } else if (newFilterValue.includes('diabetes')) {
                newFilterValue = 'diabetes';
            } else if (newFilterValue.includes('hipertensión')) {
                newFilterValue = 'hipertensión';
            } else if (newFilterValue.includes('sin tacc')) {
                newFilterValue = 'sin-tacc';
            }
            
            // 1. Actualizar el filtro activo
            currentDietFilter = newFilterValue;

            // 2. Actualizar la clase 'active'
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // 3. Aplicar filtros y búsqueda
            applyFiltersAndSearch();
        });
    });

    // Ejecutar al cargar para mostrar todas las recetas inicialmente
    applyFiltersAndSearch();
});