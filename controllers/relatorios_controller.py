import sqlite3
import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')
    return sqlite3.connect(db_path)

def get_all_transactions():
    """Busca receitas e despesas e une em um único DataFrame do Pandas."""
    conn = get_db_connection()
    
    query = '''
        SELECT 'Receita' as Tipo, data as Data, descricao as Descrição, categoria as Categoria, valor as Valor, conta as Conta
        FROM receitas
        UNION ALL
        SELECT 'Despesa' as Tipo, data as Data, descricao as Descrição, categoria as Categoria, valor as Valor, conta as Conta
        FROM despesas
        ORDER BY Data DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def export_to_excel(filepath):
    """Exporta os dados para um arquivo .xlsx."""
    try:
        df = get_all_transactions()
        # O engine 'openpyxl' garante compatibilidade com o Excel moderno
        df.to_excel(filepath, index=False, engine='openpyxl')
        return True, "Relatório Excel gerado com sucesso!"
    except Exception as e:
        return False, f"Erro ao gerar Excel: {e}"

def export_to_pdf(filepath):
    """Gera um PDF formatado com a tabela de lançamentos."""
    try:
        df = get_all_transactions()
        
        # Configura o documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título do PDF
        elements.append(Paragraph("Relatório Geral - FinanceHub", styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Constrói a lista de dados para a Tabela (Cabeçalho primeiro)
        data = [df.columns.tolist()]
        
        # Adiciona as linhas, formatando o valor como moeda
        for index, row in df.iterrows():
            tipo = row['Tipo']
            data_str = row['Data']
            desc = row['Descrição']
            cat = row['Categoria']
            val = f"R$ {row['Valor']:.2f}"
            conta = row['Conta']
            data.append([tipo, data_str, desc, cat, val, conta])
            
        # Desenha a Tabela com um estilo moderno
        table = Table(data, colWidths=[60, 70, 120, 100, 80, 80])
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")), # Fundo do cabeçalho azul escuro
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), # Texto do cabeçalho branco
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#ecf0f1")), # Fundo das linhas cinza claro
            ('GRID', (0,0), (-1,-1), 1, colors.black) # Bordas pretas
        ])
        table.setStyle(style)
        
        elements.append(table)
        
        # Constrói o arquivo
        doc.build(elements)
        return True, "Relatório PDF gerado com sucesso!"
    except Exception as e:
        return False, f"Erro ao gerar PDF: {e}"