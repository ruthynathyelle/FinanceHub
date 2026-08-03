import sqlite3
import os

def get_connection():
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "database", "finance.db")
    return sqlite3.connect(db_path)

class UserModel:
    @staticmethod
    def create_user(username, password):
        """Cadastra um novo usuário no banco."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return True, "Conta criada com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Usuário já existe!"
        except Exception as e:
            return False, f"Erro ao criar conta: {e}"
        finally:
            conn.close()

    @staticmethod
    def authenticate(username, password):
        """Verifica se o usuário e senha correspondem ao banco."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None