import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class LoginApp(ctk.CTk):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol
        self.title(f"Login - {rol.capitalize()}")
        self.geometry("400x300")


        # Carga imagen de fondo 
        fondo = Image.open("fondo_login.jpg").resize((900, 700))
        self.bg_image = ctk.CTkImage(light_image=fondo, size=(900, 700))  # CORRECTO
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self, text=f"Login para {rol}", font=("Arial", 16)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Ingresar", command=self.login).pack(pady=20)

        # Botón para volver al RolSelector
        ctk.CTkButton(self, text="⬅ Volver", fg_color="gray", command=self.volver).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.destroy()

            if self.rol == "admin":
                from admin_panel import AdminPanel
                AdminPanel().mainloop()
            else:
                from socio_panel import SocioPanel 
                SocioPanel(usuario=username).mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def volver(self):
        self.destroy()
        from rol_selector import RolSelector
        RolSelector().mainloop()
