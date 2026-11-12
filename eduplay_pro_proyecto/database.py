"""
Módulo de Base de Datos (database.py)
--------------------------------------------------------------------------
Gestiona la conexión a SQLite y la persistencia de usuarios, estados de 
suscripción y logs de pago conforme a los requerimientos de la plataforma 
de juegos educativos.
"""

import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "edugames.db"

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos SQLite.
    Configura row_factory para permitir acceso a las columnas por nombre.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias si no existen:
    - users: Almacena información de perfil, hash de contraseña y estado de suscripción.
    - payments: Almacena los soportes de pago y referencias enviadas por los usuarios.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de usuarios con control de estados de suscripción
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            sub_status TEXT DEFAULT 'inactive', -- Estados: 'inactive', 'pending', 'active', 'cancelled'
            sub_end_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de pagos / soportes enviados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount_usd REAL DEFAULT 5.00,
            reference_code TEXT NOT NULL,
            status TEXT DEFAULT 'pending', -- Estados: 'pending', 'verified'
            payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, email, password):
    """
    Registra un nuevo usuario aplicando hashing seguro de contraseña.
    Retorna True si el registro es exitoso, False en caso de duplicidad.
    """
    conn = get_db_connection()
    try:
        pw_hash = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, pw_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    """
    Verifica las credenciales de acceso de un usuario mediante su correo y contraseña.
    Retorna un diccionario con los datos del usuario si coincide, o None en caso contrario.
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    """
    Obtiene la información de un usuario por su ID y valida automáticamente 
    si la fecha de vencimiento de su suscripción activa ha expirado.
    """
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return None
        
    user_dict = dict(user)
    
    # Validación automática de caducidad de la suscripción (30 días)
    if user_dict['sub_status'] == 'active' and user_dict['sub_end_date']:
        end_date = datetime.strptime(user_dict['sub_end_date'], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > end_date:
            conn = get_db_connection()
            conn.execute("UPDATE users SET sub_status = 'inactive', sub_end_date = NULL WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            user_dict['sub_status'] = 'inactive'
            user_dict['sub_end_date'] = None
            
    return user_dict

def register_payment_support(user_id, reference_code):
    """
    Registra el soporte de pago enviado por el usuario ($5 USD equivalentes en Bolívares 
    a la tasa del BCV) y cambia el estado de su cuenta a 'pending' para revisión.
    """
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO payments (user_id, reference_code, status) VALUES (?, ?, 'pending')",
        (user_id, reference_code)
    )
    conn.execute("UPDATE users SET sub_status = 'pending' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_user_payments(user_id):
    """Retorna el historial de reportes de pago de un usuario."""
    conn = get_db_connection()
    payments = conn.execute(
        "SELECT * FROM payments WHERE user_id = ? ORDER BY payment_date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(p) for p in payments]

def approve_payment(user_id):
    """
    Acción administrativa: Aprueba el pago pendiente y activa la suscripción 
    por un período de 30 días naturales.
    """
    conn = get_db_connection()
    new_end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "UPDATE users SET sub_status = 'active', sub_end_date = ? WHERE id = ?",
        (new_end_date, user_id)
    )
    conn.execute("UPDATE payments SET status = 'verified' WHERE user_id = ? AND status = 'pending'", (user_id,))
    conn.commit()
    conn.close()

def update_subscription_status(user_id, status):
    """
    Permite al usuario cancelar su suscripción desde el perfil en cualquier momento,
    revocando el acceso a los módulos de juego.
    """
    conn = get_db_connection()
    if status == 'cancelled':
        conn.execute("UPDATE users SET sub_status = 'cancelled', sub_end_date = NULL WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """Retorna todos los usuarios registrados para la gestión del administrador."""
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(u) for u in users]
