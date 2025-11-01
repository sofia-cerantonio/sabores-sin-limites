// Datos de ejemplo (en producción cargar desde API/DB)
const RECIPES = [
    {
      id: "empanada-de-verduras",
      title: "Empanada de Verduras (versión sin lactosa / sin TACC)",
      image: "assets/images/empanada.jpg",
      tags: ["sin-lactosa","sin-tacc"],
      kcal: 280,
      ingredients: ["Harina sin TACC","Zanahoria","Cebolla","Aceite","Especias"],
      steps: ["Preparar relleno","Rellenar masa","Hornear 25 mins"],
      nutrition: { kcal:280, protein:6, fat:12, carbs:34, sodium:250 },
      adaptations: {
        "sin-lactosa": "Usá leche vegetal 1:1 o omití.",
        "diabetes": "Reducir porción y usar masa integral, reducir azúcares.",
        "hipertension": "Reducir sal y evitar fiambres."
      }
    },
    {
      id: "porridge-avena",
      title: "Porridge de Avena (opción para diabéticos)",
      image: "assets/images/porridge.jpg",
      tags: ["diabetes","sin-lactosa"],
      kcal: 190,
      ingredients: ["Avena","Leche vegetal","Canela","Semillas"],
      steps:["Cocinar avena","Agregar topping"],
      nutrition:{kcal:190,protein:5,fat:4,carbs:32,sodium:40},
      adaptations:{
        "diabetes":"Usar porciones controladas y endulzante apto."
      }
    }
  ];
  
  // Carga y render en recipes.html
  function renderRecipes(listElId="recipesGrid",recipes=RECIPES){
    const grid = document.getElementById(listElId);
    if(!grid) return;
    grid.innerHTML = "";
    recipes.forEach(r=>{
      const card = document.createElement("article");
      card.className="card";
      card.innerHTML = `
        <img src="${r.image}" alt="${r.title}">
        <div class="card-body">
          <h3>${r.title}</h3>
          <div style="font-size:13px;color:#6b5b4a">Kcal: ${r.kcal}</div>
          <div class="chips">${r.tags.map(t=>`<span class="chip">${t.replace(/-/g," ")}</span>`).join("")}</div>
          <div class="actions">
            <button class="btn btn-primary" data-id="${r.id}">Ver receta</button>
            <button class="btn btn-ghost" data-add="${r.id}">Añadir a carrito</button>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
    // listeners
    grid.querySelectorAll("[data-id]").forEach(b=>b.addEventListener("click",e=>{
      const id=e.currentTarget.dataset.id;
      location.href = `recipe.html?id=${id}`;
    }));
    grid.querySelectorAll("[data-add]").forEach(b=>b.addEventListener("click",e=>{
      addToCart(e.currentTarget.dataset.add);
    }));
  }
  
  // Buscador combinado
  function applySearch(){
    const q = (document.getElementById("q")?.value||"").toLowerCase();
    const checks = Array.from(document.querySelectorAll(".filter-cb:checked")).map(i=>i.value);
    let filtered = RECIPES.filter(r=>{
      const textMatch = r.title.toLowerCase().includes(q) || r.ingredients.join(" ").toLowerCase().includes(q);
      const filtersMatch = checks.every(f => r.tags.includes(f));
      return textMatch && filtersMatch;
    });
    renderRecipes("recipesGrid", filtered);
  }
  
  // CART simple
  function getCart(){ return JSON.parse(localStorage.getItem("cart")||"[]"); }
  function saveCart(c){ localStorage.setItem("cart", JSON.stringify(c)); renderCartCount(); }
  function addToCart(id){
    const cart = getCart();
    const item = cart.find(i=>i.id===id);
    if(item) item.qty++;
    else cart.push({id,qty:1});
    saveCart(cart);
    toast("Producto agregado al carrito");
  }
  function renderCartCount(){
    const cnt = getCart().reduce((s,i)=>s+i.qty,0);
    const el = document.getElementById("cartCount");
    if(el) el.textContent = cnt;
  }
  function toast(msg){
    const t = document.createElement("div");
    t.style.position="fixed"; t.style.right="20px"; t.style.bottom="20px";
    t.style.background="var(--marron)"; t.style.color="#fff"; t.style.padding="10px 14px"; t.style.borderRadius="8px";
    t.style.boxShadow="var(--shadow)"; t.textContent=msg;
    document.body.appendChild(t);
    setTimeout(()=>t.remove(),2200);
  }
  
  // Recipe page loader
  function loadRecipeFromQuery(){
    const params = new URLSearchParams(location.search);
    const id = params.get("id");
    if(!id) return;
    const r = RECIPES.find(x=>x.id===id);
    if(!r) return;
    document.getElementById("recipeTitle").textContent = r.title;
    document.getElementById("recipeImg").src = r.image;
    document.getElementById("ingredientsList").innerHTML = r.ingredients.map(i=>`<li>${i}</li>`).join("");
    document.getElementById("stepsList").innerHTML = r.steps.map(s=>`<li>${s}</li>`).join("");
    document.getElementById("nutritionTable").innerHTML = `
      <p>Kcal: ${r.nutrition.kcal}</p>
      <p>Proteína: ${r.nutrition.protein}g</p>
      <p>Grasas: ${r.nutrition.fat}g</p>
      <p>Carbohidratos: ${r.nutrition.carbs}g</p>
      <p>Sodio: ${r.nutrition.sodium}mg</p>
    `;
    // adaptations
    const adaptBox = document.getElementById("adaptations");
    adaptBox.innerHTML = Object.entries(r.adaptations).map(([k,v])=>`<div class="info-box"><strong>${k.replace(/-/g," ")}</strong><p>${v}</p></div>`).join("");
    // load comments
    renderComments(id);
  }
  
  // Comments (local)
  function commentsKey(id){ return `comments_${id}`; }
  function renderComments(recipeId){
    const list = document.getElementById("commentsList");
    const cdata = JSON.parse(localStorage.getItem(commentsKey(recipeId)) || "[]");
    list.innerHTML = cdata.map(c=>`<div class="comment"><strong>${escapeHtml(c.name)}</strong><div style="font-size:13px;color:#6b5b4a">${escapeHtml(c.text)}</div></div>`).join("") || "<em>Aún no hay comentarios</em>";
  }
  function postComment(recipeId){
    const name = document.getElementById("commentName").value.trim() || "Anónimo";
    const text = document.getElementById("commentText").value.trim();
    if(!text) return alert("Escribe un comentario");
    const arr = JSON.parse(localStorage.getItem(commentsKey(recipeId)) || "[]");
    arr.unshift({name,text,ts:Date.now()});
    localStorage.setItem(commentsKey(recipeId), JSON.stringify(arr));
    document.getElementById("commentText").value = "";
    renderComments(recipeId);
    toast("Comentario publicado");
  }
  function escapeHtml(s){ return s.replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])); }
  
  // init
  document.addEventListener("DOMContentLoaded", ()=> {
    renderCartCount();
    renderRecipes();
    const searchBtn = document.getElementById("searchBtn");
    if(searchBtn) searchBtn.addEventListener("click", applySearch);
    document.querySelectorAll(".filter-cb").forEach(cb=>cb.addEventListener("change", applySearch));
    // recipe page init
    if(document.getElementById("recipeTitle")){
      loadRecipeFromQuery();
      const params = new URLSearchParams(location.search);
      const id = params.get("id");
      document.getElementById("postCommentBtn").addEventListener("click", ()=>postComment(id));
    }
  });
  