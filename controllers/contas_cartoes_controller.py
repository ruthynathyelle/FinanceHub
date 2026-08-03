import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def setup_novas_tabelas():
    """Garante que as tabelas de contas e cartões existam no banco atual."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            limite REAL NOT NULL,
            fechamento INTEGER NOT NULL,
            vencimento INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Roda essa função assim que o arquivo é importado
setup_novas_tabelas()

def add_conta(nome):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contas (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        return True, "Conta cadastrada com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Esta conta já está cadastrada!"
    except Exception as e:
        return False, f"Erro: {e}"

def get_contas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM contas")
    contas = cursor.fetchall()
    conn.close()
    return contas

def add_cartao(nome, limite, fechamento, vencimento):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cartoes (nome, limite, fechamento, vencimento)
            VALUES (?, ?, ?, ?)
        ''', (nome, limite, fechamento, vencimento))
        conn.commit()
        conn.close()
        return True, "Cartão cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este cartão já está cadastrado!"
    except Exception as e:
        return False, f"Erro: {e}"

def get_cartoes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, limite, fechamento, vencimento FROM cartoes")
    cartoes = cursor.fetchall()
    
    dados_completos = []
    for c_id, nome, limite, fec, ven in cartoes:
        # Busca todas as despesas vinculadas a este cartão
        cursor.execute("SELECT SUM(valor) FROM despesas WHERE conta = ? AND pagamento = 'Cartão de Crédito'", (nome,))
        gasto = cursor.fetchone()[0]
        gasto = gasto if gasto else 0.0
        
        disponivel = limite - gasto
        dados_completos.append((c_id, nome, limite, gasto, disponivel, fec, ven))
        
    conn.close()
    return dados_completos