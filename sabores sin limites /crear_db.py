import sqlite3
import os

# 🔹 Obtener la ruta absoluta al archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# 🔹 Conectar o crear la base de datos SIEMPRE en la misma ruta
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🔹 Crear tabla de recetas
cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    type TEXT NOT NULL,
    nutrition TEXT,
    ingredients TEXT,
    instructions TEXT 
)
""")

# 🔹 Datos de recetas
recipes = [
    ("Tacos sin lactosa",
     "Versión mexicana adaptada a intolerancia a la lactosa.",
     "tacos.jpg",
     "sin-lactosa",
     "Proteínas 25g, Carbohidratos 30g, Grasas 10g",
     "Tortillas de maíz, carne de pollo, lechuga, tomate, aguacate, especias mexicanas",
     "Cocinar el pollo con especias. \nPicar verduras. \nArmar los tacos con tortillas, pollo y verduras."),
     
    ("Paella para diabéticos",
     "Paella tradicional con arroz integral y bajo índice glucémico.",
     "paella.jpg",
     "diabetes",
     "Proteínas 20g, Carbohidratos 40g, Grasas 15g",
     "Arroz integral, pollo, mariscos, pimiento, cebolla, ajo, azafrán, caldo bajo en sal",
     "Sofreír pollo y mariscos. \nAgregar verduras y arroz. \nCocinar con caldo hasta que el arroz esté listo."),
     
    ("Pizza sin gluten",
     "Masa italiana a base de harina de almendras y salsa natural.",
     "pizza.jpg",
     "sin-tacc",
     "Proteínas 18g, Carbohidratos 22g, Grasas 12g",
     "Harina de almendras, levadura, tomate, mozzarella vegana, albahaca, aceite de oliva",
     "Preparar la masa y dejar reposar. \nCubrir con salsa y toppings. \nHornear 15-20 minutos."),
     
    ("Sushi bajo en sodio",
     "Rolls japoneses con algas frescas, sal reducida y arroz integral.",
     "sushi.jpg",
     "hipertensión",
     "Proteínas 15g, Carbohidratos 35g, Grasas 5g",
     "Arroz integral, algas nori, pescado fresco, pepino, zanahoria, vinagre de arroz bajo en sodio",
     "Cocer el arroz con vinagre. \nCortar verduras y pescado. \nEnrollar en alga nori y cortar en piezas."),
     
    ("Falafel sin gluten",
     "Bocados de garbanzos típicos de Medio Oriente, aptos celíacos.",
     "falafel.jpg",
     "sin-tacc",
     "Proteínas 12g, Carbohidratos 25g, Grasas 8g",
     "Garbanzos, cebolla, ajo, cilantro, comino, harina de garbanzo, aceite para freír",
     "Moler garbanzos y mezclar con especias. \nFormar bolitas. \nFreír hasta dorar."),
     
    ("Curry de coco sin lactosa",
     "Curry tailandés con leche de coco, sin derivados lácteos.",
     "curry.jpg",
     "sin-lactosa",
     "Proteínas 22g, Carbohidratos 28g, Grasas 14g",
     "Pollo, leche de coco, curry en polvo, cebolla, ajo, jengibre, pimiento, aceite de coco",
     "Saltear cebolla, ajo y jengibre. \nAñadir pollo y curry. \nAgregar leche de coco y cocinar 15 minutos."),
     
    ("Empanadas integrales para diabéticos",
     "Versión argentina con harina integral y relleno sin azúcares añadidos.",
     "empanadas.jpg",
     "diabetes",
     "Proteínas 19g, Carbohidratos 27g, Grasas 10g",
     "Harina integral, carne magra, cebolla, huevo, aceite, especias",
     "Preparar la masa. \nCocinar el relleno de carne y cebolla. \nArmar empanadas y hornear 20 minutos."),
     
    ("Gazpacho bajo en sodio",
     "Sopa fría española con tomates frescos y sin exceso de sal.",
     "gazpacho.jpg",
     "hipertensión",
     "Proteínas 5g, Carbohidratos 15g, Grasas 4g",
     "Tomate, pepino, pimiento, ajo, aceite de oliva, vinagre, agua",
     "Licuar todos los ingredientes. \nRefrigerar 1 hora. \nServir frío."),
     
    ("Panqueques sin lactosa",
     "Deliciosos panqueques con bebida vegetal y frutas frescas.",
     "panqueques.jpg",
     "sin-lactosa",
     "Proteínas 8g, Carbohidratos 20g, Grasas 6g",
     "Harina, bebida vegetal, huevo, polvo de hornear, fruta fresca, aceite",
     "Mezclar harina, huevo y bebida vegetal. \nCocinar en sartén. \nServir con frutas."),
     
    ("Ratatouille para hipertensos",
     "Clásico francés de vegetales asados sin sal agregada.",
     "ratatouille.jpg",
     "hipertensión",
     "Proteínas 6g, Carbohidratos 18g, Grasas 5g",
     "Berenjena, calabacín, pimiento, tomate, ajo, aceite de oliva, hierbas provenzales",
     "Cortar verduras en rodajas. \nHornear con aceite y hierbas. \nServir caliente o frío."),
     
    ("Arepas sin gluten",
     "Versión venezolana hecha con harina de maíz blanco precocido.",
     "arepas.jpg",
     "sin-tacc",
     "Proteínas 9g, Carbohidratos 26g, Grasas 7g",
     "Harina de maíz precocida, agua, sal, aceite, relleno opcional (queso vegano, pollo)",
     "Mezclar harina y agua. \nFormar discos. \nCocinar en sartén y rellenar a gusto."),
     
    ("Budín de avena para diabéticos",
     "Postre saludable con edulcorante natural y sin azúcar refinada.",
     "budin.jpg",
     "diabetes",
     "Proteínas 10g, Carbohidratos 30g, Grasas 8g",
     "Avena, huevo, leche vegetal, edulcorante, esencia de vainilla, fruta seca",
     "Mezclar todos los ingredientes. \nVerter en molde. \nHornear 25-30 minutos.")
]


cursor.executemany("""
INSERT INTO recipes (title, description, image, type, nutrition, ingredients, instructions)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", recipes)

# 🔹 Crear tabla de productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image TEXT,
    category TEXT,
    price REAL
)
""")

# 🔹 Datos de productos
products = [
    ("Mix sin gluten", "Harina especial sin TACC para pizzas y panes.", "mix.jpg", "sin-tacc", 3500),
    ("Salsa natural sin sal", "Salsa de tomate orgánica sin sodio añadido.", "salsa.jpg", "hipertensión", 2800),
    ("Postre vegetal de coco", "Alternativa sin lactosa con sabor tropical.", "postre.jpg", "sin-lactosa", 3200),
    ("Snack para diabéticos", "Chips de manzana sin azúcar añadida.", "snack.jpg", "diabetes", 2500),
    ("Curry saludable", "Preparación lista sin gluten ni lácteos.", "curry.jpg", "sin-tacc", 4200),
    ("Paquete de especias", "Mezcla artesanal sin sal.", "especias.jpg", "hipertensión", 1800),
    ("Pan integral sin azúcar", "Pan especial apto para diabéticos.", "pan.jpg", "diabetes", 3000),
    ("Yogur vegetal", "Yogur sin lactosa a base de almendras.", "yogur.jpg", "sin-lactosa", 2700),
]

cursor.executemany("""
INSERT INTO products (name, description, image, category, price)
VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()
conn.close()

print(f"✅ Base de datos creada correctamente en: {DB_PATH}")
