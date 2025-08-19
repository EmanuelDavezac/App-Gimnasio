import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from admin_panel import AdminPanel
from socio_panel import SocioPanel

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol
        self.title(f"Login - {rol.capitalize()}")
        self.geometry("400x350")

        # Usuario
        self.label_usuario = ctk.CTkLabel(self, text="Usuario")
        self.label_usuario.pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(self)
        self.entry_usuario.pack()

        # Contraseña
        self.label_contraseña = ctk.CTkLabel(self, text="Contraseña")
        self.label_contraseña.pack(pady=10)
        self.entry_contraseña = ctk.CTkEntry(self, show="*")
        self.entry_contraseña.pack()

        # Botón de login
        self.boton_login = ctk.CTkButton(self, text="Ingresar", command=self.validar_login)
        self.boton_login.pack(pady=10)

        # Botón de registro
        self.boton_registrar = ctk.CTkButton(self, text="Registrarse", command=self.ventana_registro)
        self.boton_registrar.pack(pady=5)

    def validar_login(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE nombre=? AND contraseña=?", (usuario, contraseña))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            rol = resultado[0]
            messagebox.showinfo("Login exitoso", f"Bienvenido {usuario} ({rol})")
            self.destroy()
            if rol == "admin":
                AdminPanel().mainloop()
            elif rol == "socio":
                SocioPanel(usuario).mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def ventana_registro(self):
        reg_win = ctk.CTkToplevel(self)
        reg_win.title("Registro de Usuario")
        reg_win.geometry("300x250")

        # Título
        ctk.CTkLabel(reg_win, text="Nuevo Usuario", font=("Arial", 16)).pack(pady=5)

        # Campo usuario
        entry_usuario = ctk.CTkEntry(reg_win, placeholder_text="Usuario")
        entry_usuario.pack(pady=5)

        # Campo contraseña
        entry_contraseña = ctk.CTkEntry(reg_win, placeholder_text="Contraseña", show="*")
        entry_contraseña.pack(pady=5)

        # Botón registrar
        def registrar():
            usuario = entry_usuario.get()
            contraseña = entry_contraseña.get()

            if not usuario or not contraseña:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            conn = sqlite3.connect("gimnasio.db")
            cursor = conn.cursor()

            # Verificar si ya existe
            cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (usuario,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El usuario ya existe")
                conn.close()
                return

            # Registrar como socio
            cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)",
                           (usuario, contraseña, self.rol))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            reg_win.destroy()

        ctk.CTkButton(reg_win, text="Registrar", command=registrar).pack(pady=10)

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
