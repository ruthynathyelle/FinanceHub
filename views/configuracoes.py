import customtkinter as ctk
from tkinter import messagebox, filedialog
from controllers.configuracoes_controller import backup_database, restore_database

class ConfiguracoesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.label_title = ctk.CTkLabel(self, text="Configurações", font=("Roboto", 28, "bold"))
        self.label_title.pack(anchor="w", pady=(0, 20))

        # --- SEÇÃO DE TEMA ---
        self.frame_tema = ctk.CTkFrame(self, fg_color=("gray85", "gray17"), corner_radius=10)
        self.frame_tema.pack(fill="x", pady=10)
        
        self.lbl_tema = ctk.CTkLabel(self.frame_tema, text="Aparência do Sistema", font=("Roboto", 18, "bold"))
        self.lbl_tema.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Botão segmentado para escolher o tema
        self.opcoes_tema = ctk.CTkSegmentedButton(self.frame_tema, values=["Claro", "Escuro", "Sistema"], command=self.mudar_tema)
        self.opcoes_tema.pack(anchor="w", padx=20, pady=(0, 20))
        self.opcoes_tema.set("Sistema") # Valor padrão ao abrir a tela

        # --- SEÇÃO DE BACKUP E RESTAURAÇÃO ---
        self.frame_backup = ctk.CTkFrame(self, fg_color=("gray85", "gray17"), corner_radius=10)
        self.frame_backup.pack(fill="x", pady=10)

        self.lbl_backup = ctk.CTkLabel(self.frame_backup, text="Backup e Segurança", font=("Roboto", 18, "bold"))
        self.lbl_backup.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.lbl_backup_desc = ctk.CTkLabel(self.frame_backup, text="Crie uma cópia de segurança dos seus dados em um pendrive ou restaure um backup antigo.", text_color="gray50", font=("Roboto", 14))
        self.lbl_backup_desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        self.btn_frame = ctk.CTkFrame(self.frame_backup, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Botões
        self.btn_fazer_backup = ctk.CTkButton(self.btn_frame, text="💾 Fazer Backup", command=self.fazer_backup, 
                                              fg_color="#2980b9", hover_color="#3498db", font=("Roboto", 14, "bold"))
        self.btn_fazer_backup.pack(side="left", padx=(0, 10))

        self.btn_restaurar = ctk.CTkButton(self.btn_frame, text="🔄 Restaurar Backup", command=self.restaurar_backup, 
                                           fg_color="#d35400", hover_color="#e67e22", font=("Roboto", 14, "bold"))
        self.btn_restaurar.pack(side="left")

    def mudar_tema(self, valor):
        """Altera o tema visual do aplicativo instantaneamente."""
        if valor == "Claro":
            ctk.set_appearance_mode("Light")
        elif valor == "Escuro":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System")

    def fazer_backup(self):
        """Abre janela para salvar o arquivo .db"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Arquivo de Banco de Dados", "*.db")],
            title="Salvar Backup do Banco de Dados",
            initialfile="finance_backup.db"
        )
        if filepath:
            sucesso, msg = backup_database(filepath)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def restaurar_backup(self):
        """Abre janela para carregar o arquivo .db e sobrepor o atual"""
        # Aviso de segurança importante
        resposta = messagebox.askyesno("Atenção", "A restauração vai apagar e substituir todos os dados atuais do seu sistema.\n\nDeseja realmente continuar?")
        if not resposta:
            return

        filepath = filedialog.askopenfilename(
            filetypes=[("Arquivo de Banco de Dados", "*.db")],
            title="Selecione o arquivo de Backup"
        )
        if filepath:
            sucesso, msg = restore_database(filepath)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)