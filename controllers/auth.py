import sqlite3
import os

def get_db_connection():
    """Localiza o banco de dados e cria a conexão."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def register_user(username, password):
    """Registra um novo usuário no banco de dados."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True, "Usuário criado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este nome de usuário já existe!"
    except Exception as e:
        return False, f"Erro ao criar conta: {e}"

def verify_login(username, password):
    """Verifica se o usuário e a senha existem e batem com o banco."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, "Login realizado com sucesso!"
    return False, "Usuário ou senha incorretos!"