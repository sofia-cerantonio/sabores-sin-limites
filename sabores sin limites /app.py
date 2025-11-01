from flask import Flask, render_template, g, session, redirect, url_for, request, abort, flash # Importé 'flash'
import json
import sqlite3
import os

app = Flask(__name__)
# Es crucial que la clave secreta esté definida para usar sesiones (carrito)
app.secret_key = "clave_super_secreta" 

# --- Configuración de la base de datos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

# --- Conexión a la base de datos ---
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Configurar el factory para que devuelva diccionarios (objetos Row)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
    

# -------------------------------------------------------------------------
# FUNCIONES DE OBTENCIÓN DE DESTACADOS (NUEVAS FUNCIONES)
# -------------------------------------------------------------------------

def get_featured_recipes():
    """Obtiene una lista limitada de recetas destacadas (ej. 2)"""
    db = get_db()
    # Usamos ORDER BY RANDOM() para obtener 2 recetas aleatorias,
    # aunque en producción se usaría un campo 'is_featured'.
    # LIMIT 2 asegura que solo se tomen 2.
    recipes = db.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 2").fetchall() 
    return recipes

def get_featured_products():
    """Obtiene una lista limitada de productos destacados (ej. 2)"""
    db = get_db()
    # Obtenemos 2 productos aleatorios para la sección destacada
    products = db.execute("SELECT * FROM products ORDER BY RANDOM() LIMIT 2").fetchall()
    return products


# -------------------------------------------------------------------------
# RUTAS DE NAVEGACIÓN
# -------------------------------------------------------------------------

@app.route("/")
def index():
    """Muestra 2 recetas y 2 productos aleatorios en la página de inicio."""
    db = get_db()
    
    # 1. Obtener 2 recetas aleatorias
    recipes = db.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 2").fetchall() 
    
    # 2. Obtener 2 productos aleatorios
    featured_products = db.execute("SELECT * FROM products ORDER BY RANDOM() LIMIT 2").fetchall()
    
    return render_template(
        "index.html", 
        recipes=recipes, 
        featured_products=featured_products
    )


# =========================================================================
# RUTAS DE RECETAS (Optimizadas para usar solo la base de datos)
# =========================================================================

@app.route("/recipes")
def recipes():
    """Muestra la lista completa de recetas desde la base de datos."""
    db = get_db()
    recipes = db.execute("SELECT * FROM recipes").fetchall() 
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipes/<int:recipe_id>")
def recipe_detail(recipe_id):
    """Muestra el detalle de una receta específica (recuperada de la DB)."""
    db = get_db()
    # Recupera la receta de la base de datos usando el ID
    recipe_row = db.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()

    if recipe_row is None:
        abort(404) 

    # Convertir a diccionario (si no es necesario, puedes pasar recipe_row directamente)
    recipe = dict(recipe_row)

    # Ya no pasamos ninguna configuración de Firebase
    return render_template(
        "recipe_detail.html",
        recipe=recipe
    )


@app.route("/shop")
def shop():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("shop.html", products=products)

@app.route("/community")
def community():
    # Nota: Si no estás usando Firebase, esta ruta solo renderiza el template vacío
    return render_template("community.html")


# =========================================================================
# RUTAS DEL CARRITO (Lógica de Agregar/Quitar)
# =========================================================================

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    db = get_db()
    product_row = db.execute("SELECT id, name, price FROM products WHERE id = ?", (product_id,)).fetchone()

    if product_row:
        product = dict(product_row) 
        cart = session.get("cart", [])
        
        # CRÍTICO: Asegurarse de que el precio sea float al guardarlo
        product_price = float(product["price"])
        
        for item in cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                break
        else:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product_price, # Usar el precio como float
                "quantity": 1
            })
        session["cart"] = cart
    
    return redirect(url_for("shop"))


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    new_cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = new_cart
    return redirect(url_for("cart"))


@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    session.pop("cart_total", None) # Limpiar también el total
    return redirect(url_for("cart"))


# =========================================================================
# RUTAS DE CARRITO Y CHECKOUT (FINALES, con cálculo del total en Python)
# =========================================================================

# Esta ruta calcula el total, lo guarda en la sesión y renderiza el carrito
@app.route("/cart")
def cart():
    cart_items = session.get('cart', [])
    total_py = 0.0  # Inicializar el total en Python como float
    
    for item in cart_items:
        # CRÍTICO: Forzar la conversión de precio y cantidad a float/int antes de sumar
        try:
            # Usamos .get() con valor por defecto 0 para evitar errores si falta la clave
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 0))
            total_py += (price * quantity)
        except (ValueError, TypeError):
            # Si hay un error de tipo (ej. 'price' no es un número), ignora ese item
            print(f"Error al convertir tipos para el item: {item}. Asegúrate que los precios son números.")
            pass
            
    # Guardar el total calculado en la sesión para que otras rutas lo usen
    session['cart_total'] = total_py
    
    # También pasamos el total al template de cart.html
    return render_template("cart.html", cart=cart_items, total=total_py)


# Esta ruta muestra el formulario de datos
@app.route("/checkout")
def checkout():
    # Debe tener la variable 'total' en el template
    if not session.get('cart'):
        flash('Tu carrito está vacío. ¡Añade productos antes de finalizar la compra!', 'danger')
        return redirect(url_for('shop'))
        
    # Obtener el total que ya fue calculado en la ruta /cart
    total_py = session.get('cart_total', 0.0)
    
    # Renderiza el formulario, pasando el total
    return render_template("checkout.html", total=total_py)


# Esta ruta maneja el envío del formulario de checkout (SIMULACIÓN EDUCATIVA)
@app.route("/purchase_mockup", methods=["POST"])
def purchase_mockup():
    # 1. Vaciar el carrito
    session['cart'] = []
    session['cart_total'] = 0.0
    
    # 2. Informar al usuario
    flash('¡Compra simulada exitosa! Tu pedido ha sido procesado con éxito (Proyecto Educativo).', 'success')
    
    # 3. Redirigir a la página principal
    return redirect(url_for('index'))


# --- Ejecutar servidor ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

