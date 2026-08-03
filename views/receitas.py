import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from controllers.receitas_controller import add_receita

class ReceitasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_title = ctk.CTkLabel(self, text="Nova Receita", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 20))
        
        # Container do Formulário
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", pady=10)
        
        # --- Linha 1 ---
        self.entry_desc = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (ex: Salário)", width=300, height=40)
        self.entry_desc.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_valor = ctk.CTkEntry(self.form_frame, placeholder_text="Valor (ex: 5000.00)", width=200, height=40)
        self.entry_valor.grid(row=0, column=1, padx=10, pady=10)
        
        # Categorias pré-definidas
        categorias = ["Salário", "Freelance", "Investimento", "Venda", "Outros"]
        self.combo_cat = ctk.CTkComboBox(self.form_frame, values=categorias, width=200, height=40)
        self.combo_cat.grid(row=0, column=2, padx=10, pady=10)
        self.combo_cat.set("Salário") # Padrão
        
        # --- Linha 2 ---
        self.entry_conta = ctk.CTkEntry(self.form_frame, placeholder_text="Conta (ex: Nubank)", width=300, height=40)
        self.entry_conta.grid(row=1, column=0, padx=10, pady=10)
        
        # Preenche a data de hoje automaticamente
        hoje = datetime.now().strftime("%d/%m/%Y")
        self.entry_data = ctk.CTkEntry(self.form_frame, placeholder_text="Data (DD/MM/AAAA)", width=200, height=40)
        self.entry_data.insert(0, hoje)
        self.entry_data.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_obs = ctk.CTkEntry(self.form_frame, placeholder_text="Observação (Opcional)", width=200, height=40)
        self.entry_obs.grid(row=1, column=2, padx=10, pady=10)
        
        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self, text="Salvar Receita", command=self.salvar, 
                                        width=200, height=45, fg_color="#2ecc71", hover_color="#27ae60",
                                        font=("Roboto", 16, "bold"))
        self.btn_salvar.pack(anchor="w", padx=10, pady=20)
        
    def salvar(self):
        desc = self.entry_desc.get()
        valor_str = self.entry_valor.get()
        cat = self.combo_cat.get()
        conta = self.entry_conta.get()
        data = self.entry_data.get()
        obs = self.entry_obs.get()
        
        # Validação básica
        if not desc or not valor_str or not conta or not data:
            messagebox.showwarning("Aviso", "Preencha todos os campos principais!")
            return
            
        try:
            # Substitui vírgula por ponto para o banco de dados não reclamar
            valor_float = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "O campo Valor deve conter apenas números (ex: 1500.50)")
            return
            
        # Envia para o controller
        success, msg = add_receita(desc, valor_float, cat, data, conta, obs)
        
        if success:
            messagebox.showinfo("Sucesso", msg)
            # Limpa os campos após salvar
            self.entry_desc.delete(0, 'end')
            self.entry_valor.delete(0, 'end')
            self.entry_conta.delete(0, 'end')
            self.entry_obs.delete(0, 'end')
        else:
            messagebox.showerror("Erro", msg)