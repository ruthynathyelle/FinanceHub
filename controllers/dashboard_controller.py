import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def get_dashboard_metrics():
    """Busca as métricas principais do banco de dados para os cards."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Soma as receitas
    cursor.execute("SELECT SUM(valor) FROM receitas")
    total_receitas = cursor.fetchone()[0]
    total_receitas = total_receitas if total_receitas else 0.0
    
    # Soma as despesas
    cursor.execute("SELECT SUM(valor) FROM despesas")
    total_despesas = cursor.fetchone()[0]
    total_despesas = total_despesas if total_despesas else 0.0
    
    conn.close()
    
    saldo = total_receitas - total_despesas
    
    # Calcula a porcentagem de economia
    economia = 0.0
    if total_receitas > 0:
        economia = ((total_receitas - total_despesas) / total_receitas) * 100
        
    return {
        "receitas": total_receitas,
        "despesas": total_despesas,
        "saldo": saldo,
        "economia": economia
    }

# ... código anterior continua igual ...

def get_recent_transactions(limit=10):
    """Busca os últimos lançamentos (receitas e despesas) e junta em uma lista."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Busca as últimas receitas (Tipo, Descrição, Valor, Data)
    cursor.execute("SELECT 'Receita', descricao, valor, data FROM receitas ORDER BY id DESC LIMIT ?", (limit,))
    receitas = cursor.fetchall()
    
    # Busca as últimas despesas
    cursor.execute("SELECT 'Despesa', descricao, valor, data FROM despesas ORDER BY id DESC LIMIT ?", (limit,))
    despesas = cursor.fetchall()
    
    conn.close()
    
    # Junta as duas listas
    todos_lancamentos = receitas + despesas
    # Retorna apenas a quantidade do limite (para não sobrecarregar a tela inicial)
    return todos_lancamentos[:limit]

# ... código anterior continua igual ...

def get_expenses_by_category():
    """Busca o total de despesas agrupado por categoria para o gráfico."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT categoria, SUM(valor) 
        FROM despesas 
        GROUP BY categoria 
        HAVING SUM(valor) > 0
    ''')
    dados = cursor.fetchall()
    
    conn.close()
    return dados # Retorna uma lista como: [('Alimentação', 350.0), ('Internet', 100.0)]