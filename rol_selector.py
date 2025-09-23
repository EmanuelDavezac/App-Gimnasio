import customtkinter as ctk
from login import LoginApp

class RolSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Seleccionar Rol")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="¿Cómo querés ingresar?", font=("Arial", 16)).pack(pady=20)

        ctk.CTkButton(self, text="Administrador", command=self.ingresar_admin).pack(pady=10)
        ctk.CTkButton(self, text="Socio", command=self.ingresar_socio).pack(pady=10)

    def ingresar_admin(self):
        self.destroy()
        LoginApp(rol="admin").mainloop()

    def ingresar_socio(self):
        self.destroy()
        LoginApp(rol="socio").mainloop()

if __name__ == "__main__":
    app = RolSelector()
    app.mainloop()