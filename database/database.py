import sqlite3
import os

def create_connection():
    """Cria e retorna a conexão com o banco de dados SQLite."""
    # Garante que o banco será criado dentro da pasta 'database'
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, "finance.db")
    
    conn = sqlite3.connect(db_path)
    return conn

def setup_database():
    """Cria as tabelas necessárias para o FinanceHub."""
    conn = create_connection()
    cursor = conn.cursor()

    # Tabela de Usuários (Para a tela de login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Tabela de Receitas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            conta TEXT NOT NULL,
            observacao TEXT
        )
    ''')

    # Tabela de Despesas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            conta TEXT NOT NULL,
            pagamento TEXT,
            parcelas INTEGER,
            observacao TEXT
        )
    ''')

    # Tabela de Metas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_meta REAL NOT NULL,
            valor_atual REAL DEFAULT 0,
            data_limite TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Banco de dados 'finance.db' e tabelas criados com sucesso!")

# Executa a criação do banco ao rodar este arquivo diretamente
if __name__ == "__main__":
    setup_database()