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
    (
        "Tostadas Mexicanas de Tinga (Sin Lactosa)",
        "Crujientes tostadas originarias de Puebla, México, con pollo deshebrado y una salsa de chipotle ahumada. Adaptada para ser completamente libre de lácteos, usando cremas vegetales.",
        "tostadas_tinga.jpg",
        "sin-lactosa",
        "Proteínas 25g, Carbohidratos 35g, Grasas 12g",
        "Tortillas de maíz tostadas, pechuga de pollo, tomate, cebolla, chile chipotle, caldo de pollo, crema de almendras (sustituto de lácteo), aguacate, lechuga.",
        "Cocer y deshebrar el pollo. \nSofreír cebolla y cocinar con la salsa de chipotle y tomate. \nMezclar el pollo con la tinga. \nMontar la tostada con una base de crema de almendras, la tinga, lechuga y aguacate."
    ),
    (
        "Arroz Frito Cantonés (Bajo en Sodio)",
        "Un clásico plato de la cocina china, equilibrado y delicioso. Utilizamos arroz integral y salsa de soya reducida en sodio para hacerlo apto para hipertensión.",
        "arroz_cantones.jpg",
        "hipertensión",
        "Proteínas 18g, Carbohidratos 45g, Grasas 8g",
        "Arroz integral cocido, huevo, camarones o pollo, guisantes, zanahoria, cebolla de verdeo, aceite de sésamo, salsa de soya baja en sodio.",
        "Batir y cocinar el huevo revuelto. \nSaltear las proteínas y las verduras. \nAñadir el arroz integral y la salsa de soya. \nServir caliente, decorado con cebolla de verdeo."
    ),
    (
        "Pizza Margherita Napolitana (Sin TACC)",
        "La esencia de Italia, simple y perfecta. Recreamos la masa tradicional napolitana usando una mezcla de harinas sin gluten para celíacos. Un tributo a Nápoles.",
        "pizza_margherita.jpg",
        "sin-tacc",
        "Proteínas 18g, Carbohidratos 30g, Grasas 15g",
        "Mezcla de harinas sin gluten, levadura, agua, tomate San Marzano (para salsa), mozzarella vegana o de búfala sin lactosa, albahaca fresca, aceite de oliva virgen extra.",
        "Preparar la masa sin gluten y darle un reposo de 2 horas. \nEstirar la masa y cubrir con salsa de tomate y mozzarella. \nHornear a alta temperatura hasta que los bordes estén dorados."
    ),
    (
        "Curry Korma Hindú (Para Diabéticos)",
        "Un cremoso curry indio, típicamente dulce, adaptado. Usamos edulcorantes naturales y leche de coco para un bajo índice glucémico sin sacrificar la riqueza de sabor.",
        "curry_korma.jpg",
        "diabetes",
        "Proteínas 24g, Carbohidratos 30g, Grasas 18g",
        "Pollo o paneer, leche de coco, pasta de curry Korma (sin azúcar añadido), cebolla, ajo, jengibre, yogur natural sin azúcar, especias (cardamomo, cúrcuma).",
        "Marinar el pollo. \nSofreír la cebolla, el ajo y el jengibre. \nIncorporar el pollo y la pasta de curry. \nCocinar a fuego lento con la leche de coco hasta que espese."
    ),
    (
        "Falafel y Hummus Libanés (Sin TACC)",
        "Los populares bocados de garbanzos fritos y su acompañamiento cremoso, básicos de la cocina de Oriente Medio. Naturalmente libre de gluten y cargado de proteínas vegetales.",
        "falafel_hummus.jpg",
        "sin-tacc",
        "Proteínas 16g, Carbohidratos 35g, Grasas 10g",
        "Garbanzos, tahini, jugo de limón, ajo, perejil, comino, harina de garbanzo (para aglutinar), aceite de oliva.",
        "Preparar el hummus licuando garbanzos, tahini y especias. \nMezclar los garbanzos para el falafel, formar bolitas y freír u hornear. \nServir con verduras frescas."
    ),
    (
        "Sopa Pho Vietnamita (Sin Lactosa)",
        "Un caldo aromático de Vietnam, reconfortante y lleno de sabor. Naturalmente libre de lácteos, nos centramos en la intensidad del caldo tradicional.",
        "pho.jpg",
        "sin-lactosa",
        "Proteínas 30g, Carbohidratos 40g, Grasas 7g",
        "Fideos de arroz, carne de res magra, jengibre, cebolla, anís estrellado, canela, brotes de soja, lima, albahaca tailandesa, salsa de pescado.",
        "Preparar un caldo de res muy aromático con especias. \nCocer los fideos de arroz. \nServir el caldo caliente sobre los fideos, carne cruda en rodajas finas, y hierbas frescas."
    ),
    (
        "Arepas Venezolanas con Relleno Bajo en Sal",
        "El pan nacional de Venezuela, crujiente por fuera y suave por dentro. Relleno con pollo deshebrado y aguacate, sin salsas altas en sodio, ideal para hipertensión.",
        "arepas_rellenas.jpg",
        "hipertensión",
        "Proteínas 20g, Carbohidratos 35g, Grasas 8g",
        "Harina de maíz precocida, agua, sal marina (moderada), aceite, relleno de pollo deshebrado (sin sal), aguacate, cilantro.",
        "Amasar la harina de maíz con agua y sal. \nFormar discos y cocinar en sartén o plancha. \nAbrir las arepas y rellenar con pollo y aguacate triturado."
    ),
    (
        "Pastel de Choclo Chileno (Para Diabéticos)",
        "Un guiso tradicional de Chile, típicamente dulce, adaptado. Reemplazamos el azúcar refinado del 'pino' (guiso de carne) y de la cubierta de maíz por edulcorantes naturales.",
        "pastel_choclo.jpg",
        "diabetes",
        "Proteínas 22g, Carbohidratos 32g, Grasas 14g",
        "Carne magra molida, cebolla, edulcorante (estevia o monk fruit), albahaca, maíz fresco (choclo), leche vegetal, huevo duro (opcional).",
        "Preparar el pino de carne. \nLicuar el maíz con leche vegetal. \nColocar el pino en una fuente, cubrir con la pasta de choclo. \nHornear hasta dorar."
    ),
    (
        "Alfajores de Maicena (Sin TACC)",
        "El postre icónico de Argentina. Galletas suaves de maicena rellenas de dulce de leche, adaptadas con harina sin gluten para ser aptas para celíacos.",
        "alfajores_maicena_singluten.jpg",
        "sin-tacc",
        "Proteínas 8g, Carbohidratos 45g, Grasas 15g",
        "Almidón de maíz (Maicena), harina de arroz, mantequilla, huevos, ralladura de limón, dulce de leche (sin gluten), coco rallado.",
        "Preparar la masa de maicena. \nCortar círculos y hornear. \nUna vez fríos, rellenar con dulce de leche y espolvorear con coco rallado."
    ),
    (
        "Milanesa Napolitana Vegana (Sin Lactosa)",
        "Un clásico argentino, la milanesa a la napolitana, reinterpretada con proteína vegetal y queso vegano para ser completamente libre de lácteos y carne.",
        "milanesa_vegana_sinlactosa.jpg",
        "sin-lactosa",
        "Proteínas 20g, Carbohidratos 30g, Grasas 10g",
        "Filete de proteína vegetal (seitan o soja), pan rallado sin lactosa, huevo (o sustituto vegano), salsa de tomate, queso mozzarella vegano, orégano.",
        "Empanar el filete vegetal. \nFreír u hornear. \nCubrir con salsa de tomate y queso vegano. \nGratinar en el horno hasta que el queso se derrita."
    ),
    (
        "Locro Patrio (Bajo en Sodio)",
        "Tradicional guiso criollo argentino, perfecto para el invierno. Reducimos la sal y usamos cortes magros para mantenerlo bajo en sodio.",
        "locro_bajosodio.jpg",
        "hipertensión",
        "Proteínas 25g, Carbohidratos 40g, Grasas 15g",
        "Maíz blanco (hervido), porotos (judías), carne de ternera magra, calabaza, cebolla, pimiento rojo, comino, pimentón (sin sal agregada).",
        "Cocer el maíz y los porotos. \nSofreír verduras y carne. \nMezclar todos los ingredientes con agua y cocinar a fuego lento hasta que espese."
    ),

    (
        "Tortilla Española de Patatas (Para Diabéticos)",
        "Un ícono de la gastronomía española, la tortilla de patatas. Sustituimos la patata tradicional por boniato (batata) para un índice glucémico más bajo.",
        "tortilla_boniato_diabetico.jpg",
        "diabetes",
        "Proteínas 15g, Carbohidratos 25g, Grasas 18g",
        "Boniato (batata), huevos, cebolla, aceite de oliva virgen extra, pimienta negra.",
        "Pelar y cortar el boniato y la cebolla. \nFreír el boniato y la cebolla en aceite de oliva a fuego bajo. \nBatir los huevos y mezclar con el boniato. \nCuajar la tortilla en una sartén."
    ),
    (
        "Crema Catalana (Sin Lactosa)",
        "El postre más famoso de Cataluña, con un toque de limón y canela. Utilizamos bebida vegetal para lograr la misma cremosidad sin ningún derivado lácteo.",
        "crema_catalana_sinlactosa.jpg",
        "sin-lactosa",
        "Proteínas 6g, Carbohidratos 35g, Grasas 10g",
        "Bebida vegetal (almendra o avena), yemas de huevo, azúcar (o edulcorante), almidón de maíz, canela en rama, piel de limón.",
        "Calentar la bebida vegetal con canela y limón. \nMezclar las yemas con azúcar y almidón. \nIncorporar la mezcla caliente y cocinar hasta que espese. \nEnfriar y caramelizar el azúcar antes de servir."
    ),

    (
        "Ajiaco Santafereño (Bajo en Sodio)",
        "La sopa emblemática de Bogotá, Colombia, rica en papa y hierbas. Adaptamos el caldo y el pollo para mantener el sabor tradicional con un bajo contenido de sal.",
        "ajiaco_bajosodio.jpg",
        "hipertensión",
        "Proteínas 28g, Carbohidratos 45g, Grasas 7g",
        "Papas criollas y sabaneras, pollo deshebrado, mazorca (choclo), guascas (hierba esencial), alcaparras (lavadas para reducir sal), crema agria (sin sal) o aguacate.",
        "Cocer el pollo con las papas, mazorcas y guascas. \nRetirar el pollo y deshebrar. \nServir el caldo espeso con el pollo, crema agria (o aguacate) y alcaparras."
    ),
    (
        "Arroz con Leche (Para Diabéticos)",
        "Un postre casero muy popular en Colombia y toda Latinoamérica. Sustituimos el azúcar por edulcorante natural y usamos arroz integral para reducir el impacto glucémico.",
        "arroz_leche_diabetico.jpg",
        "diabetes",
        "Proteínas 10g, Carbohidratos 35g, Grasas 8g",
        "Arroz integral, leche vegetal o descremada, edulcorante natural (stevia o monk fruit), canela en rama, cáscara de naranja.",
        "Cocer el arroz integral. \nAgregar la leche, edulcorante, canela y cáscara de naranja. \nCocinar a fuego lento y remover hasta alcanzar una consistencia cremosa. \nServir frío con canela en polvo."
    )
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
    tipo_dieta TEXT,
    category TEXT,
    price INT
)
""")

products = [
    (
        "Tostadas de Tinga (Pack 2 unid.)", 
        "Tostadas mexicanas listas para consumir. Pollo en salsa chipotle, sin lactosa.", 
        "tostadas_tinga.jpg", 
        "sin-lactosa", 
        "plato_preparado", 
        6500
    ),
    (
        "Curry Korma Hindú Congelado", 
        "Curry indio cremoso con vegetales. Listo en 5 minutos, bajo índice glucémico.", 
        "curry_korma.jpg", 
        "diabetes", 
        "plato_preparado", 
        7800
    ),
    (
        "Milanesa Napolitana Vegana (2 unid.)", 
        "Milanesas de proteína vegetal con salsa y queso vegano. Congeladas, sin lácteos.", 
        "milanesa_vegana_sinlactosa.jpg", 
        "sin-lactosa", 
        "plato_preparado", 
        8500
    ),
    (
        "Porción de Alfajores de Maicena (x3)", 
        "Clásico argentino sin gluten. Rellenos con dulce de leche sin TACC.", 
        "alfajores_maicena_singluten.jpg", 
        "sin-tacc", 
        "plato_preparado", 
        5900
    ),
    (
        "Arroz Frito Cantonés Ración", 
        "Arroz integral y vegetales, bajo en sodio. Calentar y servir, ideal para hipertensión.", 
        "arroz_cantones.jpg", 
        "hipertensión", 
        "plato_preparado", 
        6200
    ),
    
    (
        "Mix sin gluten Pan y Pizza", 
        "Harina especial sin TACC para pizzas y panes. Alto rendimiento y textura.", 
        "mix_pan_pizza.jpg", 
        "sin-tacc", 
        "harina_mix", 
        3500
    ),
    (
        "Harina de Garbanzo Pura", 
        "Harina ideal para rebozar falafel o espesar guisos. Naturalmente sin gluten.", 
        "harina_garbanzo.jpg", 
        "sin-tacc", 
        "harina_mix", 
        2900
    ),
    
    (
        "Salsa de Tomate Orgánica", 
        "Salsa de tomate casera, orgánica y sin sodio añadido. Bote 500g.", 
        "salsa_sin_sal.jpg", 
        "hipertensión", 
        "salsas_condimentos", 
        2800
    ),
    (
        "Paquete de Especias Mediterráneas", 
        "Mezcla artesanal de hierbas y especias para salmón y pollo, sin sal.", 
        "especias_pack.jpg", 
        "hipertensión", 
        "salsas_condimentos", 
        1800
    ),
    (
        "Curry en Polvo Keto/Diabético", 
        "Mezcla de especias para curry, sin azúcar ni harinas añadidas. Apto diabéticos.", 
        "curry_especias.jpg", 
        "diabetes", 
        "salsas_condimentos", 
        4200
    ),
    
    (
        "Yogur de Almendras Natural", 
        "Yogur 100% vegetal, sin lactosa ni azúcares añadidos.", 
        "yogur_almendra.jpg", 
        "sin-lactosa", 
        "lacteos_vegetales", 
        2700
    ),
    (
        "Postre de Coco y Chía", 
        "Alternativa cremosa sin lactosa con sabor tropical y semillas de chía.", 
        "postre_coco.jpg", 
        "sin-lactosa", 
        "lacteos_vegetales", 
        3200
    ),
    (
        "Chips de Manzana Deshidratada", 
        "Snack crujiente y natural sin azúcar añadida. Bolsa grande.", 
        "snack_manzana.jpg", 
        "diabetes", 
        "snacks_pan", 
        2500
    ),
    (
        "Pan Integral para Diabéticos", 
        "Pan de molde integral con bajo índice glucémico y edulcorantes naturales.", 
        "pan_integral.jpg", 
        "diabetes", 
        "snacks_pan", 
        3000
    ),
]

cursor.executemany("""
INSERT INTO products (name, description, image, tipo_dieta, category, price)
VALUES (?, ?, ?, ?, ?, ?)
""", products)

conn.commit()
conn.close()

print(f"✅ Base de datos creada correctamente en: {DB_PATH}")
