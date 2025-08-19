import sqlite3

def crear_bd():
    conn = sqlite3.connect("gimnasio.db")
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('admin', 'socio')) NOT NULL
        )
    """)

    # Usuarios de prueba
    cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)", ("admin1", "adminpass", "admin"))
    cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)", ("socio1", "sociopass", "socio"))

    conn.commit()
    conn.close()

def crear_tabla_clases():
    conn = sqlite3.connect("gimnasio.db")
    cursor = conn.cursor()

    # Tabla de clases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            instructor TEXT NOT NULL,
            horario TEXT NOT NULL,
            capacidad INTEGER NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def crear_tabla_reservas():
    conn = sqlite3.connect("gimnasio.db")
    cursor = conn.cursor()

    # Tabla de reservas con columna 'fecha'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            clase_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (clase_id) REFERENCES clases(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_bd()
    crear_tabla_clases()
    crear_tabla_reservas()