import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class LoginApp(ctk.CTk):
    def __init__(self, rol):
        super().__init__()
        self.rol = rol
        self.title(f"Login - {rol.capitalize()}")
        self.geometry("900x500")

        # Ruta de imagen y temporizador
        self.bg_image_path = "assets/fondo_login.jpg"
        self.redimensionando = False
        self.tamaño_anterior = (self.winfo_width(), self.winfo_height())

        # Layout dividido
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Imagen de fondo
        fondo = Image.open(self.bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(450, 500))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.grid(row=0, column=0, sticky="nsew")

        # Formulario
        self.form_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

        self.titulo = ctk.CTkLabel(self.form_frame, text=f"Login para {rol}", font=("Arial", 20, "bold"), text_color="#333")
        self.titulo.pack(pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Usuario")
        self.username_entry.pack(pady=10, ipadx=10, ipady=5)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10, ipadx=10, ipady=5)

        self.ingresar_btn = ctk.CTkButton(self.form_frame, text="Ingresar", fg_color="#0077cc", hover_color="#005fa3", command=self.login)
        self.ingresar_btn.pack(pady=20, ipadx=10)

        self.volver_btn = ctk.CTkButton(self.form_frame, text="⬅ Volver", fg_color="gray", hover_color="#666", command=self.volver)
        self.volver_btn.pack(pady=10, ipadx=10)

        # Evento de redimensionamiento
        self.bind("<Configure>", self.redimensionar_dinamico)

    def redimensionar_dinamico(self, event=None):
        if not self.redimensionando:
            self.redimensionando = True
            self.after(150, self.actualizar_layout)

    def actualizar_layout(self):
        ancho_actual = self.winfo_width()
        alto_actual = self.winfo_height()

        if (ancho_actual, alto_actual) != self.tamaño_anterior:
            # Redimensionar imagen
            ancho_img = int(ancho_actual * 0.5)
            alto_img = alto_actual
            fondo = Image.open(self.bg_image_path).resize((ancho_img, alto_img))
            self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(ancho_img, alto_img))
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.image = self.bg_image

            # Redimensionar formulario
            ancho_form = int(ancho_actual * 0.35)
            alto_form = int(alto_actual * 0.6)
            self.form_frame.configure(width=ancho_form, height=alto_form)

            # Guardar nuevo tamaño
            self.tamaño_anterior = (ancho_actual, alto_actual)

        self.redimensionando = False

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

if __name__ == "__main__":
    app = LoginApp(rol="socio")
    app.mainloop()