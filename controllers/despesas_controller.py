import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def add_despesa(descricao, valor, categoria, data, conta, pagamento, parcelas, observacao):
    """Insere uma nova despesa no banco de dados."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO despesas (descricao, valor, categoria, data, conta, pagamento, parcelas, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (descricao, valor, categoria, data, conta, pagamento, parcelas, observacao))
        
        conn.commit()
        conn.close()
        return True, "Despesa cadastrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar despesa: {e}"