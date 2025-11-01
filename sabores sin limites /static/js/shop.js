document.addEventListener("DOMContentLoaded", () => {
  // Referencias a elementos del DOM
  const searchInput = document.getElementById("searchShop");
  const filterButtons = document.querySelectorAll(".filter-category");
  const productCards = document.querySelectorAll(".product-card");

  // Estado actual de la búsqueda y el filtro
  let currentSearchQuery = '';
  let currentFilter = 'all'; // Por defecto, mostrar todos

  /**
   * Función principal para aplicar el filtro y la búsqueda.
   */
  const applyFiltersAndSearch = () => {
      // Normalizar la consulta de búsqueda
      const searchQuery = currentSearchQuery.toLowerCase().trim();

      productCards.forEach(card => {
          const cardCategory = card.dataset.category;
          const cardName = card.querySelector('.card-title').textContent.toLowerCase();
          const cardDescription = card.querySelector('.card-text.small').textContent.toLowerCase();

          // ----------------------------------------------------
          // Criterio 1: Coincidencia de Filtros (Botones)
          // ----------------------------------------------------
          let matchesCategory = false;

          if (currentFilter === 'all') {
              matchesCategory = true;
          } else if (currentFilter === 'plato_preparado') {
              matchesCategory = (cardCategory === 'plato_preparado');
          } else if (currentFilter === 'otros') {
              // 'Otros' incluye todo lo que NO es plato_preparado
              matchesCategory = (cardCategory !== 'plato_preparado');
          }

          // ----------------------------------------------------
          // Criterio 2: Coincidencia de Búsqueda (Input)
          // ----------------------------------------------------
          const matchesSearch = !searchQuery ||
                                cardName.includes(searchQuery) ||
                                cardDescription.includes(searchQuery);

          // ----------------------------------------------------
          // Mostrar/Ocultar
          // ----------------------------------------------------
          if (matchesCategory && matchesSearch) {
              card.style.display = "block"; // Usamos block porque el elemento es un .col
          } else {
              card.style.display = "none";
          }
      });
  };

  // --- Event Listeners para el Filtrado por Categoría ---
  filterButtons.forEach(button => {
      button.addEventListener("click", () => {
          const newFilter = button.dataset.filter;
          
          // 1. Actualizar el estado del filtro
          currentFilter = newFilter;

          // 2. Actualizar la clase 'active' de los botones
          filterButtons.forEach(btn => btn.classList.remove('active'));
          button.classList.add('active');

          // 3. Aplicar los filtros
          applyFiltersAndSearch();
      });
  });

  // --- Event Listeners para la Búsqueda ---
  searchInput.addEventListener("input", (event) => {
      // Actualizar el estado de la búsqueda en cada pulsación
      currentSearchQuery = event.target.value;
      applyFiltersAndSearch();
  });
  
  // Opcional: para forzar la búsqueda si se pulsa Enter
  searchInput.addEventListener("keyup", (event) => {
      if (event.key === 'Enter') {
          applyFiltersAndSearch();
      }
  });

  // Inicializar: Asegurarse de que el filtro 'all' se aplique al cargar
  applyFiltersAndSearch();
});