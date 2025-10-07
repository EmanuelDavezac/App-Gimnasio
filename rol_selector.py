import customtkinter as ctk
from PIL import Image
from login import LoginApp

class RolSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Seleccionar Rol")
        self.geometry("500x400")

        # Ruta de imagen y control de redimensionamiento
        self.bg_image_path = "assets/fondo_azul.jpg"
        self.redimensionando = False
        self.tamaño_anterior = (self.winfo_width(), self.winfo_height())

        # Imagen de fondo
        fondo = Image.open(self.bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(500, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Panel central con altura proporcional y ancho fijo
        self.panel = ctk.CTkFrame(self, corner_radius=20, fg_color="white", width=360, height=420)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        # Contenido del panel
        self.titulo = ctk.CTkLabel(self.panel, text="¿Cómo querés ingresar?", font=("Montserrat", 18, "bold"), text_color="#333")
        self.titulo.pack(pady=(30, 20))

        admin_icon = ctk.CTkImage(Image.open("assets/icon_admin.jpg"), size=(24, 24))
        self.admin_btn = ctk.CTkButton(self.panel, text="Administrador", image=admin_icon, compound="left",
                                       command=self.ingresar_admin, fg_color="#0077cc", hover_color="#005fa3")
        self.admin_btn.pack(pady=10, ipadx=10)

        socio_icon = ctk.CTkImage(Image.open("assets/icon_socio.jpg"), size=(24, 24))
        self.socio_btn = ctk.CTkButton(self.panel, text="Socio", image=socio_icon, compound="left",
                                       command=self.ingresar_socio, fg_color="#0077cc", hover_color="#005fa3")
        self.socio_btn.pack(pady=10, ipadx=10)

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
            fondo = Image.open(self.bg_image_path).resize((ancho_actual, alto_actual))
            self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(ancho_actual, alto_actual))
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.image = self.bg_image

            # Calcular nueva altura del panel (más alto y vertical)
            nueva_altura = max(420, int(alto_actual * 0.7))
            self.panel.configure(height=nueva_altura)

            # Reubicar el panel centrado
            self.panel.place(relx=0.5, rely=0.5, anchor="center")

            self.tamaño_anterior = (ancho_actual, alto_actual)

        self.redimensionando = False

    def ingresar_admin(self):
        self.destroy()
        LoginApp(rol="admin").mainloop()

    def ingresar_socio(self):
        self.destroy()
        LoginApp(rol="socio").mainloop()

if __name__ == "__main__":
    app = RolSelector()
    app.mainloop()