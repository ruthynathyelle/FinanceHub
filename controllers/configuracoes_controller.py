import shutil
import os

def get_db_path():
    """Retorna o caminho exato onde o banco de dados atual está salvo."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finance.db')

def backup_database(destination_path):
    """Copia o banco de dados para a pasta escolhida pelo usuário."""
    try:
        db_path = get_db_path()
        shutil.copy2(db_path, destination_path)
        return True, "Backup realizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao fazer backup: {e}"

def restore_database(source_path):
    """Substitui o banco de dados atual pelo arquivo de backup escolhido."""
    try:
        db_path = get_db_path()
        shutil.copy2(source_path, db_path)
        return True, "Banco de dados restaurado com sucesso!\n\nPor favor, feche e abra o sistema novamente para carregar os novos dados."
    except Exception as e:
        return False, f"Erro ao restaurar banco de dados: {e}"