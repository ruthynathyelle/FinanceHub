import customtkinter as ctk
from tkinter import messagebox, filedialog
from controllers.relatorios_controller import export_to_excel, export_to_pdf

class RelatoriosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título e Descrição
        self.label_title = ctk.CTkLabel(self, text="Relatórios", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(self, text="Exporte todos os seus lançamentos (Receitas e Despesas) consolidados.", font=("Roboto", 16), text_color="gray60")
        self.info_label.pack(anchor="w", pady=(0, 40))
        
        # Container centralizado para os botões
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=10)
        
        # Botão Excel (Verde)
        self.btn_excel = ctk.CTkButton(self.btn_frame, text="📊 Exportar para Excel", command=self.gerar_excel, 
                                       width=250, height=60, font=("Roboto", 16, "bold"), 
                                       fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_excel.grid(row=0, column=0, padx=20, pady=20)
        
        # Botão PDF (Vermelho)
        self.btn_pdf = ctk.CTkButton(self.btn_frame, text="📄 Exportar para PDF", command=self.gerar_pdf, 
                                     width=250, height=60, font=("Roboto", 16, "bold"), 
                                     fg_color="#c0392b", hover_color="#e74c3c")
        self.btn_pdf.grid(row=0, column=1, padx=20, pady=20)

    def gerar_excel(self):
        # Abre a janela do Windows perguntando onde salvar o arquivo
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Salvar Relatório Excel",
            initialfile="Relatorio_FinanceHub.xlsx"
        )
        
        # Se o usuário escolheu uma pasta e clicou em Salvar (Não cancelou)
        if filepath:
            sucesso, msg = export_to_excel(filepath)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def gerar_pdf(self):
        # Abre a janela do Windows perguntando onde salvar o arquivo
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar Relatório PDF",
            initialfile="Relatorio_FinanceHub.pdf"
        )
        
        if filepath:
            sucesso, msg = export_to_pdf(filepath)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)