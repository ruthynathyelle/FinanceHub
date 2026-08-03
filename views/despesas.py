import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.despesas_controller import add_despesa

class DespesasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_title = ctk.CTkLabel(self, text="Nova Despesa", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 20))
        
        # Container do Formulário
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", pady=10)
        
        # --- Linha 1 ---
        self.entry_desc = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (ex: Mercado)", width=300, height=40)
        self.entry_desc.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_valor = ctk.CTkEntry(self.form_frame, placeholder_text="Valor (ex: 350.00)", width=200, height=40)
        self.entry_valor.grid(row=0, column=1, padx=10, pady=10)
        
        # Categorias da Despesa
        categorias = ["Alimentação", "Moradia", "Transporte", "Saúde", "Educação", "Lazer", "Internet", "Energia", "Água", "Cartão", "Outros"]
        self.combo_cat = ctk.CTkComboBox(self.form_frame, values=categorias, width=200, height=40)
        self.combo_cat.grid(row=0, column=2, padx=10, pady=10)
        self.combo_cat.set("Alimentação") 
        
        # --- Linha 2 ---
        self.entry_conta = ctk.CTkEntry(self.form_frame, placeholder_text="Conta/Cartão (ex: Nubank)", width=300, height=40)
        self.entry_conta.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        hoje = datetime.now().strftime("%d/%m/%Y")
        self.entry_data = ctk.CTkEntry(self.form_frame, placeholder_text="Data (DD/MM/AAAA)", width=200, height=40)
        self.entry_data.insert(0, hoje)
        self.entry_data.grid(row=1, column=1, padx=10, pady=10)
        
        # Forma de pagamento
        pagamentos = ["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro", "Boleto"]
        self.combo_pag = ctk.CTkComboBox(self.form_frame, values=pagamentos, width=200, height=40)
        self.combo_pag.grid(row=1, column=2, padx=10, pady=10)
        self.combo_pag.set("PIX")
        
        # --- Linha 3 ---
        self.entry_parcelas = ctk.CTkEntry(self.form_frame, placeholder_text="Qtd Parcelas", width=300, height=40)
        self.entry_parcelas.insert(0, "1") # Padrão é 1 parcela
        self.entry_parcelas.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_obs = ctk.CTkEntry(self.form_frame, placeholder_text="Observação (Opcional)", width=420, height=40)
        self.entry_obs.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self, text="Salvar Despesa", command=self.salvar, 
                                        width=200, height=45, fg_color="#e74c3c", hover_color="#c0392b",
                                        font=("Roboto", 16, "bold"))
        self.btn_salvar.pack(anchor="w", padx=10, pady=20)
        
    def salvar(self):
        desc = self.entry_desc.get()
        valor_str = self.entry_valor.get()
        cat = self.combo_cat.get()
        conta = self.entry_conta.get()
        data = self.entry_data.get()
        pag = self.combo_pag.get()
        parcelas_str = self.entry_parcelas.get()
        obs = self.entry_obs.get()
        
        # Validação
        if not desc or not valor_str or not conta or not data:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
            
        try:
            valor_float = float(valor_str.replace(",", "."))
            parcelas_int = int(parcelas_str)
        except ValueError:
            messagebox.showerror("Erro", "O campo Valor e Parcelas devem conter apenas números!")
            return
            
        # Envia para o controller
        success, msg = add_despesa(desc, valor_float, cat, data, conta, pag, parcelas_int, obs)
        
        if success:
            messagebox.showinfo("Sucesso", msg)
            self.entry_desc.delete(0, 'end')
            self.entry_valor.delete(0, 'end')
            self.entry_conta.delete(0, 'end')
            self.entry_parcelas.delete(0, 'end')
            self.entry_parcelas.insert(0, "1")
            self.entry_obs.delete(0, 'end')
        else:
            messagebox.showerror("Erro", msg)