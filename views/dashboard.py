import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.dashboard_controller import get_dashboard_metrics, get_recent_transactions, get_expenses_by_category

class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.metrics = get_dashboard_metrics()
        
        self.label_title = ctk.CTkLabel(self, text="Visão Geral", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 20))
        
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=(0, 10))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.create_card(self.cards_frame, 0, "Receitas", f"R$ {self.metrics['receitas']:,.2f}", "#2ecc71")
        self.create_card(self.cards_frame, 1, "Despesas", f"R$ {self.metrics['despesas']:,.2f}", "#e74c3c")
        self.create_card(self.cards_frame, 2, "Saldo Atual", f"R$ {self.metrics['saldo']:,.2f}", "#3498db")
        self.create_card(self.cards_frame, 3, "Economia", f"{self.metrics['economia']:.1f}%", "#9b59b6")

        # --- NOVA SEÇÃO: DIVISÃO EM DUAS COLUNAS ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="both", expand=True, pady=(10, 0))
        self.bottom_frame.grid_columnconfigure(0, weight=1) # Coluna do Gráfico
        self.bottom_frame.grid_columnconfigure(1, weight=1) # Coluna da Lista

        # COLUNA 1: Gráfico de Pizza
        self.chart_frame = ctk.CTkFrame(self.bottom_frame, fg_color=("gray85", "gray17"), corner_radius=10)
        self.chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.lbl_chart = ctk.CTkLabel(self.chart_frame, text="Despesas por Categoria", font=("Roboto", 18, "bold"))
        self.lbl_chart.pack(pady=15)
        
        self.desenhar_grafico(self.chart_frame)

        # COLUNA 2: Lista de Lançamentos
        self.list_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.label_sub = ctk.CTkLabel(self.list_frame, text="Últimos Lançamentos", font=("Roboto", 18, "bold"))
        self.label_sub.pack(anchor="w", pady=(0, 10))
        
        self.scroll_list = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True)
        
        lancamentos = get_recent_transactions()
        if not lancamentos:
            ctk.CTkLabel(self.scroll_list, text="Nenhum lançamento.", text_color="gray50").pack(pady=20)
        else:
            for tipo, desc, valor, data in lancamentos:
                self.create_list_item(tipo, desc, valor, data)

    def desenhar_grafico(self, parent):
        """Busca os dados e desenha o gráfico de pizza."""
        dados = get_expenses_by_category()
        
        if not dados:
            ctk.CTkLabel(parent, text="Nenhuma despesa cadastrada.", text_color="gray50").pack(expand=True)
            return

        labels = [item[0] for item in dados]
        valores = [item[1] for item in dados]

        # Define a cor de fundo exata do frame escuro do CustomTkinter
        cor_fundo = "#2b2b2b" 
        
        # Pinta a figura inteira com a cor escura
        fig = Figure(figsize=(5, 4), dpi=100, facecolor=cor_fundo)
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(cor_fundo) # Pinta a área interna também
        
        cores = ['#e74c3c', '#3498db', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c']
        
        wedges, texts, autotexts = ax.pie(
            valores, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=cores,
            textprops={'color': 'white'} # Garante que os nomes das categorias fiquem brancos
        )
        
        # Deixa a porcentagem em negrito e branca
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('white')

        ax.axis('equal') 
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def create_card(self, parent, col, title, value, color):
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=0, column=col, padx=10, sticky="ew")
        ctk.CTkLabel(card, text=title, font=("Roboto", 14), text_color="gray60").pack(pady=(15, 5))
        ctk.CTkLabel(card, text=value, font=("Roboto", 22, "bold"), text_color=color).pack(pady=(0, 15))
        
    def create_list_item(self, tipo, desc, valor, data):
        item_frame = ctk.CTkFrame(self.scroll_list, fg_color=("gray85", "gray17"), corner_radius=5)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        cor_valor = "#2ecc71" if tipo == "Receita" else "#e74c3c"
        sinal = "+ " if tipo == "Receita" else "- "
        
        ctk.CTkLabel(item_frame, text=desc, font=("Roboto", 16)).pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(item_frame, text=data, font=("Roboto", 14), text_color="gray50").pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(item_frame, text=f"{sinal}R$ {valor:,.2f}", font=("Roboto", 16, "bold"), text_color=cor_valor).pack(side="right", padx=15, pady=10)