import customtkinter as ctk
from PIL import Image
from login import LoginApp

class RolSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Seleccionar Rol")
        self.geometry("500x400")
        self.resizable(False, False)

        # Fondo con imagen de login
        fondo = Image.open("assets/fondo_login.jpg")
        self.bg_image = ctk.CTkImage(light_image=fondo, dark_image=fondo, size=(500, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Título de la ventana con fondo celeste
        self.titulo = ctk.CTkLabel(self, text="¿Cómo querés ingresar?",
                                   font=("Montserrat", 20, "bold"),
                                   text_color="#333333",
                                   fg_color="#B2EBF2",
                                   corner_radius=0)
        self.titulo.place(relx=0.5, rely=0.1, anchor="center")

        # Botón para ingresar como administrador
        admin_icon = ctk.CTkImage(Image.open("assets/icon_admin.jpg"), size=(24, 24))
        self.admin_btn = ctk.CTkButton(self, text="Administrador", image=admin_icon, compound="left",
                                       command=self.ingresar_admin,
                                       fg_color="#FFEB3B",
                                       hover_color="#FDD835",
                                       text_color="#333333",
                                       corner_radius=0,
                                       width=160)
        self.admin_btn.place(relx=0.25, rely=0.85, anchor="center")

        # Botón para ingresar como socio
        socio_icon = ctk.CTkImage(Image.open("assets/icon_socio.jpg"), size=(24, 24))
        self.socio_btn = ctk.CTkButton(self, text="Socio", image=socio_icon, compound="left",
                                       command=self.ingresar_socio,
                                       fg_color="#FFEB3B",
                                       hover_color="#FDD835",
                                       text_color="#333333",
                                       corner_radius=0,
                                       width=160)
        self.socio_btn.place(relx=0.75, rely=0.85, anchor="center")

    # Función para ingresar como administrador y abrir el login correspondiente
    def ingresar_admin(self):
        self.destroy()
        LoginApp(rol="admin").mainloop()

    # Función para ingresar como socio y abrir el login correspondiente
    def ingresar_socio(self):
        self.destroy()
        LoginApp(rol="socio").mainloop()

if __name__ == "__main__":
    app = RolSelector()
    app.mainloop()
