import customtkinter as ctk
from tkinter import messagebox
from controllers.auth import verify_login, register_user

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        
        self.on_login_success = on_login_success 
        
        # Título
        self.label_title = ctk.CTkLabel(self, text="FinanceHub", font=("Roboto", 28, "bold"))
        self.label_title.pack(pady=(40, 20))

        # Campo Usuário
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Usuário", width=250, height=40)
        self.entry_username.pack(pady=10)

        # Campo Senha
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=250, height=40)
        self.entry_password.pack(pady=10)

        # Botão Entrar
        self.btn_login = ctk.CTkButton(self, text="Entrar", width=250, height=40, command=self.handle_login)
        self.btn_login.pack(pady=(20, 10))

        # Botão Criar Conta
        self.btn_register = ctk.CTkButton(self, text="Criar Conta", width=250, height=40, 
                                          fg_color="transparent", border_width=1, 
                                          text_color=("gray10", "#DCE4EE"), 
                                          command=self.handle_register)
        self.btn_register.pack(pady=5)

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
            
        success, message = verify_login(username, password)
        if success:
            # Espera 100ms para a animação do botão terminar antes de mudar de tela
            self.after(100, self.on_login_success)
        else:
            messagebox.showerror("Erro", message)

    def handle_register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos para criar a conta!")
            return
            
        success, message = register_user(username, password)
        if success:
            messagebox.showinfo("Sucesso", message)
        else:
            messagebox.showerror("Erro", message)