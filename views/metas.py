import customtkinter as ctk
from tkinter import messagebox
from controllers.metas_controller import add_meta, get_metas

class MetasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_title = ctk.CTkLabel(self, text="Metas Financeiras", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 10))
        
        # --- Formulário de Cadastro Rápido ---
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", pady=10)
        
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Nome da Meta (ex: Notebook)", width=250, height=40)
        self.entry_nome.grid(row=0, column=0, padx=5, pady=10)
        
        self.entry_meta = ctk.CTkEntry(self.form_frame, placeholder_text="Valor da Meta", width=150, height=40)
        self.entry_meta.grid(row=0, column=1, padx=5, pady=10)
        
        self.entry_atual = ctk.CTkEntry(self.form_frame, placeholder_text="Já guardado", width=150, height=40)
        self.entry_atual.grid(row=0, column=2, padx=5, pady=10)
        
        self.entry_data = ctk.CTkEntry(self.form_frame, placeholder_text="Data Limite", width=120, height=40)
        self.entry_data.grid(row=0, column=3, padx=5, pady=10)
        
        self.btn_salvar = ctk.CTkButton(self.form_frame, text="Adicionar Meta", command=self.salvar_meta, 
                                        width=150, height=40, fg_color="#f39c12", hover_color="#d35400",
                                        font=("Roboto", 14, "bold"))
        self.btn_salvar.grid(row=0, column=4, padx=10, pady=10)
        
        # --- Lista de Metas (Área Rolável) ---
        self.label_sub = ctk.CTkLabel(self, text="Minhas Metas", font=("Roboto", 20, "bold"))
        self.label_sub.pack(anchor="w", pady=(20, 10))
        
        self.scroll_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True)
        
        # Carrega as metas ao abrir a tela
        self.carregar_metas()

    def carregar_metas(self):
        """Limpa a lista atual e busca novamente no banco de dados."""
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
            
        metas = get_metas()
        if not metas:
            ctk.CTkLabel(self.scroll_list, text="Você ainda não tem metas cadastradas.", text_color="gray50").pack(pady=20)
            return
            
        for m_id, nome, valor_meta, valor_atual, data in metas:
            self.criar_card_meta(nome, valor_meta, valor_atual, data)
            
    def criar_card_meta(self, nome, valor_meta, valor_atual, data):
        """Desenha o card com a barra de progresso."""
        card = ctk.CTkFrame(self.scroll_list, fg_color=("gray85", "gray17"), corner_radius=10)
        card.pack(fill="x", pady=10, padx=5)
        
        # Cálculo da porcentagem (Evitando divisão por zero ou passar de 100%)
        progresso = valor_atual / valor_meta if valor_meta > 0 else 0
        if progresso > 1: progresso = 1
        
        # Topo: Nome e Data
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(top_frame, text=nome, font=("Roboto", 18, "bold")).pack(side="left")
        ctk.CTkLabel(top_frame, text=f"Prazo: {data}", font=("Roboto", 12), text_color="gray50").pack(side="right")
        
        # Meio: Barra de Progresso
        bar = ctk.CTkProgressBar(card, height=12, progress_color="#f39c12")
        bar.pack(fill="x", padx=15, pady=10)
        bar.set(progresso) # Define o preenchimento da barra (de 0.0 a 1.0)
        
        # Fundo: Valores
        bot_frame = ctk.CTkFrame(card, fg_color="transparent")
        bot_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(bot_frame, text=f"Guardado: R$ {valor_atual:,.2f}", font=("Roboto", 14)).pack(side="left")
        ctk.CTkLabel(bot_frame, text=f"Faltam: R$ {(valor_meta - valor_atual):,.2f}  ({int(progresso*100)}%)", font=("Roboto", 14, "bold"), text_color="#f39c12").pack(side="right")

    def salvar_meta(self):
        nome = self.entry_nome.get()
        meta_str = self.entry_meta.get()
        atual_str = self.entry_atual.get()
        data = self.entry_data.get()
        
        if not nome or not meta_str or not data:
            messagebox.showwarning("Aviso", "Preencha o Nome, Valor da Meta e Data Limite!")
            return
            
        try:
            valor_meta = float(meta_str.replace(",", "."))
            # Se não digitar nada no guardado, considera 0
            valor_atual = float(atual_str.replace(",", ".")) if atual_str else 0.0
        except ValueError:
            messagebox.showerror("Erro", "Os campos de valor devem conter apenas números!")
            return
            
        success, msg = add_meta(nome, valor_meta, valor_atual, data)
        if success:
            # Limpa os campos
            self.entry_nome.delete(0, 'end')
            self.entry_meta.delete(0, 'end')
            self.entry_atual.delete(0, 'end')
            self.entry_data.delete(0, 'end')
            # Atualiza a lista na mesma hora
            self.carregar_metas()
        else:
            messagebox.showerror("Erro", msg)