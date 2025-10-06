import customtkinter as ctk
from PIL import Image
from login import LoginApp

class RolSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Seleccionar Rol")
        self.geometry("500x400")

        self.bg_image = ctk.CTkImage(
            light_image=Image.open("assets/fondo_azul.jpg"),
            dark_image=Image.open("assets/fondo_azul.jpg"),
            size=(500, 400)
        )
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)


        # Panel central con bordes redondeados
        self.panel = ctk.CTkFrame(self, corner_radius=20, fg_color="white", width=350, height=1000)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.panel, text="¿Cómo querés ingresar?", font=("Montserrat", 18, "bold"), text_color="#333").pack(pady=(40, 10))

        admin_icon = ctk.CTkImage(Image.open("assets/icon_admin.jpg"), size=(24, 24))
        ctk.CTkButton(self.panel, text="Administrador", image=admin_icon, compound="left",
                      command=self.ingresar_admin, fg_color="#0077cc", hover_color="#005fa3").pack(pady=10, ipadx=10)

        socio_icon = ctk.CTkImage(Image.open("assets/icon_socio.jpg"), size=(24, 24))
        ctk.CTkButton(self.panel, text="Socio", image=socio_icon, compound="left",
                      command=self.ingresar_socio, fg_color="#0077cc", hover_color="#005fa3").pack(pady=10, ipadx=10)

    def ingresar_admin(self):
        self.destroy()
        LoginApp(rol="admin").mainloop()

    def ingresar_socio(self):
        self.destroy()
        LoginApp(rol="socio").mainloop()

if __name__ == "__main__":
    app = RolSelector()
    app.mainloop()