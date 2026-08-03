import customtkinter as ctk
from tkinter import messagebox
from controllers.contas_cartoes_controller import add_conta, get_contas, add_cartao, get_cartoes

class ContasCartoesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.label_title = ctk.CTkLabel(self, text="Contas e Cartões", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 20))
        
        # Criação das Abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_contas = self.tabview.add("🏦 Contas")
        self.tab_cartoes = self.tabview.add("💳 Cartões")
        
        self.setup_tab_contas()
        self.setup_tab_cartoes()

    # ================= CONTAS =================
    def setup_tab_contas(self):
        form_frame = ctk.CTkFrame(self.tab_contas, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        self.entry_nome_conta = ctk.CTkEntry(form_frame, placeholder_text="Nome da Conta (ex: Sicoob, Dinheiro)", width=300, height=40)
        self.entry_nome_conta.grid(row=0, column=0, padx=10, pady=10)
        
        btn_salvar_conta = ctk.CTkButton(form_frame, text="Adicionar Conta", command=self.salvar_conta, width=150, height=40, font=("Roboto", 14, "bold"))
        btn_salvar_conta.grid(row=0, column=1, padx=10, pady=10)
        
        self.scroll_contas = ctk.CTkScrollableFrame(self.tab_contas, fg_color="transparent")
        self.scroll_contas.pack(fill="both", expand=True, pady=10)
        self.carregar_contas()

    def salvar_conta(self):
        nome = self.entry_nome_conta.get()
        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome da conta!")
            return
        
        sucesso, msg = add_conta(nome)
        if sucesso:
            self.entry_nome_conta.delete(0, 'end')
            self.carregar_contas()
        else:
            messagebox.showerror("Erro", msg)

    def carregar_contas(self):
        for widget in self.scroll_contas.winfo_children():
            widget.destroy()
        contas = get_contas()
        
        if not contas:
            ctk.CTkLabel(self.scroll_contas, text="Nenhuma conta cadastrada.", text_color="gray50").pack(pady=20)
            return
            
        for _, nome in contas:
            card = ctk.CTkFrame(self.scroll_contas, fg_color=("gray85", "gray17"), corner_radius=5)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=f"🏦  {nome}", font=("Roboto", 18, "bold")).pack(anchor="w", padx=20, pady=15)

    # ================= CARTÕES =================
    def setup_tab_cartoes(self):
        form_frame = ctk.CTkFrame(self.tab_cartoes, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        self.entry_nome_cartao = ctk.CTkEntry(form_frame, placeholder_text="Nome (ex: Nubank)", width=150, height=40)
        self.entry_nome_cartao.grid(row=0, column=0, padx=5, pady=10)
        
        self.entry_limite = ctk.CTkEntry(form_frame, placeholder_text="Limite (R$)", width=120, height=40)
        self.entry_limite.grid(row=0, column=1, padx=5, pady=10)
        
        self.entry_fec = ctk.CTkEntry(form_frame, placeholder_text="Dia Fechamento", width=120, height=40)
        self.entry_fec.grid(row=0, column=2, padx=5, pady=10)
        
        self.entry_ven = ctk.CTkEntry(form_frame, placeholder_text="Dia Venc.", width=100, height=40)
        self.entry_ven.grid(row=0, column=3, padx=5, pady=10)
        
        btn_salvar_cartao = ctk.CTkButton(form_frame, text="Adicionar", command=self.salvar_cartao, 
                                          width=100, height=40, font=("Roboto", 14, "bold"), 
                                          fg_color="#8e44ad", hover_color="#9b59b6")
        btn_salvar_cartao.grid(row=0, column=4, padx=5, pady=10)
        
        self.scroll_cartoes = ctk.CTkScrollableFrame(self.tab_cartoes, fg_color="transparent")
        self.scroll_cartoes.pack(fill="both", expand=True, pady=10)
        self.carregar_cartoes()

    def salvar_cartao(self):
        nome = self.entry_nome_cartao.get()
        limite_str = self.entry_limite.get()
        fec_str = self.entry_fec.get()
        ven_str = self.entry_ven.get()
        
        if not nome or not limite_str or not fec_str or not ven_str:
            messagebox.showwarning("Aviso", "Preencha todos os campos do cartão!")
            return
        
        try:
            limite = float(limite_str.replace(",", "."))
            fec = int(fec_str)
            ven = int(ven_str)
        except ValueError:
            messagebox.showerror("Erro", "Limite e Dias devem ser números!")
            return
            
        sucesso, msg = add_cartao(nome, limite, fec, ven)
        if sucesso:
            self.entry_nome_cartao.delete(0, 'end')
            self.entry_limite.delete(0, 'end')
            self.entry_fec.delete(0, 'end')
            self.entry_ven.delete(0, 'end')
            self.carregar_cartoes()
        else:
            messagebox.showerror("Erro", msg)

    def carregar_cartoes(self):
        for widget in self.scroll_cartoes.winfo_children():
            widget.destroy()
        cartoes = get_cartoes()
        
        if not cartoes:
            ctk.CTkLabel(self.scroll_cartoes, text="Nenhum cartão cadastrado.", text_color="gray50").pack(pady=20)
            return
            
        for _, nome, limite, gasto, disponivel, fec, ven in cartoes:
            card = ctk.CTkFrame(self.scroll_cartoes, fg_color=("gray85", "gray17"), corner_radius=10)
            card.pack(fill="x", pady=10, padx=5)
            
            top_frame = ctk.CTkFrame(card, fg_color="transparent")
            top_frame.pack(fill="x", padx=15, pady=(15, 5))
            
            ctk.CTkLabel(top_frame, text=f"💳 {nome}", font=("Roboto", 18, "bold")).pack(side="left")
            ctk.CTkLabel(top_frame, text=f"Fechamento: {fec} | Vencimento: {ven}", font=("Roboto", 12), text_color="gray50").pack(side="right")
            
            progresso = gasto / limite if limite > 0 else 0
            if progresso > 1: progresso = 1
            
            # Dinâmica de Cores: Verde (Folgado), Amarelo (Atenção), Vermelho (Estourando)
            cor_barra = "#e74c3c" if progresso > 0.8 else ("#f39c12" if progresso > 0.5 else "#2ecc71")
            
            bar = ctk.CTkProgressBar(card, height=12, progress_color=cor_barra)
            bar.pack(fill="x", padx=15, pady=10)
            bar.set(progresso)
            
            bot_frame = ctk.CTkFrame(card, fg_color="transparent")
            bot_frame.pack(fill="x", padx=15, pady=(5, 15))
            
            ctk.CTkLabel(bot_frame, text=f"Limite: R$ {limite:,.2f}", font=("Roboto", 14)).pack(side="left")
            ctk.CTkLabel(bot_frame, text=f"Usado: R$ {gasto:,.2f}  |  Disp: R$ {disponivel:,.2f}", font=("Roboto", 14, "bold"), text_color=cor_barra).pack(side="right")