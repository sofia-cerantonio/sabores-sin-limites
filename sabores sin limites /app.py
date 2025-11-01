from flask import Flask, render_template, g, session, redirect, url_for, request, abort
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
        # Esto soluciona el problema de serialización JSON que tenías antes.
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# --- Rutas de Navegación ---

@app.route("/")
def index():
    # Nota: Aquí puedes cargar recetas destacadas si es necesario
    return render_template("index.html")

# =========================================================================
# RUTAS DE RECETAS (Optimizadas para usar solo la base de datos)
# =========================================================================

@app.route("/recipes")
def recipes():
    """Muestra la lista completa de recetas desde la base de datos."""
    db = get_db()
    # Usamos "recipes" como nombre de la tabla
    recipes = db.execute("SELECT * FROM recipes").fetchall() 
    
    # IMPORTANTE: Asegúrate de que el ID sea numérico en tu tabla
    # y que los campos 'type' y 'image' existan.
    return render_template("recipes.html", recipes=recipes)

@app.route("/recipes/<int:recipe_id>")
def recipe_detail(recipe_id):
    """Muestra el detalle de una receta específica."""
    db = get_db()
    # Ejecutamos la consulta buscando por ID
    recipe = db.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()

    if recipe is None:
        # Si la receta no se encuentra en la DB, mostrar error 404
        abort(404) 

    # Como db.row_factory es sqlite3.Row, recipe es un objeto Row serializable a Jinja.
    return render_template('recipe_detail.html', recipe=recipe)


@app.route("/shop")
def shop():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("shop.html", products=products)

@app.route("/community")
def community():
    return render_template("community.html")


# =========================================================================
# RUTAS DEL CARRITO
# =========================================================================

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    db = get_db()
    # Buscar el producto usando su ID
    product_row = db.execute("SELECT id, name, price FROM products WHERE id = ?", (product_id,)).fetchone()

    if product_row:
        # Convertir la Row a un diccionario estándar si es necesario para el carrito, 
        # aunque como Row se comporta como dict, no es estrictamente necesario, pero es más seguro.
        product = dict(product_row) 
        cart = session.get("cart", [])
        
        for item in cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                break
        else:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1
            })
        session["cart"] = cart
    
    # Redirigir a la tienda después de añadir, o usar request.referrer para más flexibilidad
    return redirect(url_for("shop"))


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    # Filtrar la lista, manteniendo solo los items que NO coincidan con el ID
    new_cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = new_cart
    return redirect(url_for("cart"))


@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))


# --- Ejecutar servidor ---
if __name__ == "__main__":
    app.run(debug=True)
