document.addEventListener("DOMContentLoaded", () => {
  // Lógica del carrito (Mantenida)
  const cartCount = document.getElementById("cartCount");
  const addButtons = document.querySelectorAll(".btn-add");
  let count = 0;

  addButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      count++;
      cartCount.textContent = count;
      btn.textContent = "Agregado ✔";
      btn.disabled = true;
    });
  });

  // 🔍 Buscador modificado
  const searchInput = document.getElementById("searchShop");
  const searchBtn = document.getElementById("searchShopBtn");
  
  // 🎯 MODIFICACIÓN 1: Seleccionar el contenedor de columna (div.col)
  // El elemento visible que se debe ocultar/mostrar es el contenedor de columna,
  // que es el padre directo de la tarjeta (`div.card`).
  const cards = document.querySelectorAll("#productsGrid > .col"); 

  function filterProducts() {
      const query = searchInput.value.toLowerCase();
      
      cards.forEach(col => {
          // El elemento .card está dentro de .col
          const card = col.querySelector(".card");
          
          // 🎯 MODIFICACIÓN 2: Buscar el nombre dentro de la estructura de tarjeta horizontal
          // El nombre (h5) está dentro de .card-body, que a su vez está dentro del col-8 de Bootstrap.
          const nameElement = card.querySelector(".card-title");
          
          if (nameElement) {
              const name = nameElement.textContent.toLowerCase();
              
              // Si el nombre incluye la consulta, mostramos la columna como 'block'.
              // Usamos 'block' porque el `div.col` actúa como un bloque dentro de la fila principal.
              col.style.display = name.includes(query) ? "block" : "none";
          } else {
              // Si no se encuentra el título, por seguridad, lo ocultamos.
              col.style.display = "none";
          }
      });
  }

  searchBtn.addEventListener("click", filterProducts);
  searchInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") filterProducts();
    // Opcional: También puedes llamar a filterProducts sin presionar Enter para una búsqueda instantánea
    // filterProducts(); 
  });
});
  