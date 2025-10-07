import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3

class LoginApp(ctk.CTk):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol
        self.title(f"Login - {rol.capitalize()}")
        self.geometry("700x500")
        self.configure(fg_color="#5b8fd6")  # Fondo principal azul claro suave

        # Imagen de fondo del login
        self.bg_image_path = "assets/fondo_login.jpg"
        self.redimensionando = False
        self.tamaño_anterior = (self.winfo_width(), self.winfo_height())

        fondo = Image.open(self.bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(450, 500))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.grid(row=0, column=0, sticky="nsew")

        # Formulario de login
        self.form_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#fff7b2", border_width=3, border_color="#ffe066")
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

        self.titulo = ctk.CTkLabel(self.form_frame, text=f"🔐 Login para {rol}",
                                   font=("Arial Rounded MT Bold", 20), text_color="#5b8fd6")
        self.titulo.pack(pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Usuario")
        self.username_entry.pack(pady=10, ipadx=10, ipady=5)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10, ipadx=10, ipady=5)

        # Botón para iniciar sesión
        self.ingresar_btn = ctk.CTkButton(self.form_frame, text="Ingresar",
                                          fg_color="#7ea6e0", hover_color="#5b8fd6",
                                          text_color="white", corner_radius=10,
                                          command=self.login)
        self.ingresar_btn.pack(pady=20, ipadx=10)

        # Botón para abrir ventana de registro
        self.registrar_btn = ctk.CTkButton(self.form_frame, text="📝 Registrarse",
                                           fg_color="#ffe066", hover_color="#ffe699",
                                           text_color="#5b8fd6", corner_radius=10,
                                           command=self.abrir_registro)
        self.registrar_btn.pack(pady=10, ipadx=10)

        # Botón para volver a selector de rol
        self.volver_btn = ctk.CTkButton(self.form_frame, text="⬅ Volver",
                                        fg_color="#bdbdbd", hover_color="#999999",
                                        text_color="white", corner_radius=10,
                                        command=self.volver)
        self.volver_btn.pack(pady=10, ipadx=10)

        # Redimensionamiento dinámico del formulario y la imagen
        self.bind("<Configure>", self.redimensionar_dinamico)

    # Controla el redimensionamiento para no ejecutarlo demasiado seguido
    def redimensionar_dinamico(self, event=None):
        if not self.redimensionando:
            self.redimensionando = True
            self.after(150, self.actualizar_layout)

    # Actualiza tamaño de la imagen de fondo y del formulario según ventana
    def actualizar_layout(self):
        ancho_actual = self.winfo_width()
        alto_actual = self.winfo_height()

        if (ancho_actual, alto_actual) != self.tamaño_anterior:
            ancho_img = int(ancho_actual * 0.5)
            alto_img = alto_actual
            fondo = Image.open(self.bg_image_path).resize((ancho_img, alto_img))
            self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(ancho_img, alto_img))
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.image = self.bg_image

            ancho_form = int(ancho_actual * 0.35)
            alto_form = int(alto_actual * 0.6)
            self.form_frame.configure(width=ancho_form, height=alto_form)

            self.tamaño_anterior = (ancho_actual, alto_actual)

        self.redimensionando = False

    # Lógica de inicio de sesión
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Completa ambos campos")
            return

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE nombre=? AND contraseña=?", (username, password))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            rol_en_bd = resultado[0]
            self.destroy()
            if rol_en_bd == "admin":
                from admin_panel import AdminPanel
                AdminPanel().mainloop()
            else:
                from socio_panel import SocioPanel
                SocioPanel(usuario=username).mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Vuelve al selector de rol
    def volver(self):
        self.destroy()
        from rol_selector import RolSelector
        RolSelector().mainloop()

    # Abre ventana para registrar un nuevo usuario
    def abrir_registro(self):
        registro = ctk.CTkToplevel(self)
        registro.title("Registrar")
        registro.geometry("400x300")
        registro.configure(fg_color="#fff7b2")

        # Centrar sobre la ventana de login
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 150
        registro.geometry(f"+{x}+{y}")

        # Bloquea interacción con ventana principal mientras registro está abierto
        registro.transient(self)
        registro.grab_set()
        registro.focus_force()

        ctk.CTkLabel(registro, text="Nuevo usuario", font=("Arial Rounded MT Bold", 18),
                     text_color="#5b8fd6").pack(pady=10)

        entry_usuario = ctk.CTkEntry(registro, placeholder_text="Nombre de usuario")
        entry_usuario.pack(pady=10)

        entry_contraseña = ctk.CTkEntry(registro, placeholder_text="Contraseña", show="*")
        entry_contraseña.pack(pady=10)

        # Lógica de registro de usuario
        def registrar():
            usuario = entry_usuario.get()
            contraseña = entry_contraseña.get()

            if not usuario or not contraseña:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            if len(contraseña) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                return

            conn = sqlite3.connect("gimnasio.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (usuario,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El usuario ya existe")
                conn.close()
                return

            cursor.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)",
                           (usuario, contraseña, self.rol))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            registro.destroy()

        ctk.CTkButton(registro, text="Registrar", fg_color="#5b8fd6", hover_color="#5b8fd6",
                      text_color="white", corner_radius=10, command=registrar).pack(pady=20)

if __name__ == "__main__":
    app = LoginApp(rol="socio")
    app.mainloop()
