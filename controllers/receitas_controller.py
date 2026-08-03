import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def add_receita(descricao, valor, categoria, data, conta, observacao):
    """Insere uma nova receita no banco de dados."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO receitas (descricao, valor, categoria, data, conta, observacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (descricao, valor, categoria, data, conta, observacao))
        
        conn.commit()
        conn.close()
        return True, "Receita cadastrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {e}"