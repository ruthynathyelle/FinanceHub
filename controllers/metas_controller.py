import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def add_meta(nome, valor_meta, valor_atual, data_limite):
    """Insere uma nova meta financeira no banco."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO metas (nome, valor_meta, valor_atual, data_limite)
            VALUES (?, ?, ?, ?)
        ''', (nome, valor_meta, valor_atual, data_limite))
        conn.commit()
        conn.close()
        return True, "Meta cadastrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar meta: {e}"

def get_metas():
    """Busca todas as metas para exibir na tela."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, valor_meta, valor_atual, data_limite FROM metas")
    metas = cursor.fetchall()
    conn.close()
    return metas