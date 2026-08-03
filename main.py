import customtkinter as ctk
from views.login import LoginView
from views.dashboard import DashboardView
from views.receitas import ReceitasView
from views.despesas import DespesasView
from database.database import setup_database
from views.metas import MetasView
from views.contas_cartoes import ContasCartoesView
from views.relatorios import RelatoriosView
from views.configuracoes import ConfiguracoesView

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FinanceHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração base da janela
        self.title("FinanceHub - Login")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Container principal (Invisível) que vai segurar todas as telas
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        self.show_login_screen()

    def show_login_screen(self):
        self.geometry("400x500")
        self.resizable(False, False)
        self.title("FinanceHub - Login")
        
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Chama a view de login e aplica o posicionamento
        self.login_view = LoginView(self.main_container, on_login_success=self.show_main_app)
        self.login_view.pack(pady=20, padx=20, fill="both", expand=True)
        
    def show_main_app(self):
        self.geometry("1000x600")
        self.resizable(True, True)
        self.title("FinanceHub")
        
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Menu Lateral (Sidebar)
        self.sidebar = ctk.CTkFrame(self.main_container, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="FinanceHub", font=("Roboto", 24, "bold"))
        self.logo_label.pack(pady=(30, 30))
        
        btn_config = {"anchor": "w", "fg_color": "transparent", "hover_color": ("gray70", "gray30"), "text_color": ("gray10", "gray90")}
        
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="🏠  Dashboard", command=self.load_dashboard, **btn_config)
        self.btn_dashboard.pack(pady=5, padx=10, fill="x")
        
        self.btn_receitas = ctk.CTkButton(self.sidebar, text="💰  Receitas", command=self.load_receitas, **btn_config)
        self.btn_receitas.pack(pady=5, padx=10, fill="x")
        
        self.btn_despesas = ctk.CTkButton(self.sidebar, text="💸  Despesas", command=self.load_despesas, **btn_config)
        self.btn_despesas.pack(pady=5, padx=10, fill="x")

        self.btn_contas = ctk.CTkButton(self.sidebar, text="🏦  Contas/Cartões", command=self.load_contas, **btn_config)
        self.btn_contas.pack(pady=5, padx=10, fill="x")

        self.btn_metas = ctk.CTkButton(self.sidebar, text="🎯  Metas", command=self.load_metas, **btn_config)
        self.btn_metas.pack(pady=5, padx=10, fill="x")

        self.btn_relatorios = ctk.CTkButton(self.sidebar, text="📊  Relatórios", command=self.load_relatorios, **btn_config)
        self.btn_relatorios.pack(pady=5, padx=10, fill="x")

        self.btn_config = ctk.CTkButton(self.sidebar, text="⚙️  Configurações", command=self.load_configuracoes, **btn_config)
        self.btn_config.pack(pady=5, padx=10, fill="x")
        
        self.btn_logout = ctk.CTkButton(self.sidebar, text="Sair", fg_color="#c0392b", hover_color="#e74c3c", command=self.show_login_screen)
        self.btn_logout.pack(side="bottom", pady=20, padx=20)

        # Área de Conteúdo
        self.content_area = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True)

        self.load_dashboard()
        
    def load_dashboard(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.dashboard_view = DashboardView(self.content_area)
        
    def load_receitas(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.receitas_view = ReceitasView(self.content_area)
        
    def load_despesas(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.despesas_view = DespesasView(self.content_area)

    def load_metas(self):
     for widget in self.content_area.winfo_children():
         widget.destroy()
     self.metas_view = MetasView(self.content_area)

    def load_contas(self):
     for widget in self.content_area.winfo_children():
         widget.destroy()
     self.contas_view = ContasCartoesView(self.content_area)

    def load_relatorios(self):
     for widget in self.content_area.winfo_children():
         widget.destroy()
     self.relatorios_view = RelatoriosView(self.content_area)

    def load_configuracoes(self):
     for widget in self.content_area.winfo_children():
         widget.destroy()
     self.configuracoes_view = ConfiguracoesView(self.content_area)

if __name__ == "__main__":
    setup_database()
    app = FinanceHubApp()
    app.mainloop()