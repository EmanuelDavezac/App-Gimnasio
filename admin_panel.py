import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox
import datetime
from PIL import Image


class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Administrador")
        self.geometry("800x800")
        self.configure(fg_color="#5b8fd6")

        # ==== Fondo con imagen ====
        try:
            bg_image = ctk.CTkImage(Image.open("assets/fondo_gym.jpg"), size=(800, 800))
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(relwidth=1, relheight=1)
        except Exception:
            pass

        # ==== Contenedor principal ====
        main_frame = ctk.CTkFrame(self, fg_color="#fff7b2")
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # ==== Columna izquierda: Formulario ====
        left_frame = ctk.CTkFrame(main_frame, fg_color="#e3f6fc", corner_radius=20, border_width=3, border_color="#b2cfff")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        ctk.CTkButton(left_frame, text="⬅ Volver", fg_color="#7ea6e0",
                      hover_color="#5b8fd6", text_color="#fff", command=self.volver,
                      height=30, width=100).pack(pady=(10, 5))

        ctk.CTkLabel(left_frame, text="🧩 Agregar nueva clase",
                     font=("Arial Rounded MT Bold", 18), text_color="#5b8fd6").pack(pady=5)

        self.entry_nombre = ctk.CTkEntry(left_frame, placeholder_text="Nombre de la clase", height=35)
        self.entry_nombre.pack(pady=5, padx=20)

        self.entry_instructor = ctk.CTkEntry(left_frame, placeholder_text="Instructor", height=35)
        self.entry_instructor.pack(pady=5, padx=20)

        self.entry_horario = ctk.CTkEntry(left_frame, placeholder_text="Horario (ej: 18:00)", height=35)
        self.entry_horario.pack(pady=5, padx=20)

        self.entry_capacidad = ctk.CTkEntry(left_frame, placeholder_text="Capacidad", height=35)
        self.entry_capacidad.pack(pady=5, padx=20)

        ctk.CTkLabel(left_frame, text="Fecha de la clase", font=("Arial", 14), text_color="#5b8fd6").pack(pady=(10, 5))
        self.date_picker = DateEntry(left_frame, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=(0, 10))

        self.boton_guardar = ctk.CTkButton(left_frame, text="💾 Guardar clase",
                                   fg_color="#ffe066", hover_color="#ffe699",
                                   text_color="#5b8fd6",
                                   height=35, corner_radius=10,
                                   command=self.guardar_clase)
        self.boton_guardar.pack(pady=(10, 20))

        # ==== Columna derecha: Clases existentes + filtro ====
        right_frame = ctk.CTkFrame(main_frame, fg_color="#fff7b2", corner_radius=20,
                                   border_width=3, border_color="#ffe066")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

        ctk.CTkLabel(right_frame, text="📚 Clases existentes",
                     font=("Arial Rounded MT Bold", 18), text_color="#5b8fd6").pack(pady=(10, 5))

        filtro_frame = ctk.CTkFrame(right_frame, fg_color="#fff7b2")
        filtro_frame.pack(pady=(5, 0), padx=10, fill="x")

        self.entry_busqueda = ctk.CTkEntry(filtro_frame, placeholder_text="Buscar por nombre, instructor o fecha", height=30)
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(filtro_frame, text="🔍 Buscar", width=80, height=30,
                      fg_color="#5b8fd6", hover_color="#7ea6e0", text_color="#fff7b2",
                      command=self.buscar_clases).pack(side="right")

        self.frame_clases = ctk.CTkScrollableFrame(right_frame, width=350, height=600,
                                                   fg_color="#fff7b2", scrollbar_button_color="#fff7b2",
                                                   scrollbar_fg_color="#fff7b2")
        self.frame_clases.pack(pady=(10, 20), padx=10, fill="both", expand=True)

        self.mostrar_clases()

    def buscar_clases(self):
        termino = self.entry_busqueda.get().strip()
        self.mostrar_clases(filtro=termino)

    def mostrar_clases(self, filtro=""):
        for widget in self.frame_clases.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()

        if filtro:
            cursor.execute("""
                SELECT id, nombre, instructor, horario, capacidad, fecha
                FROM clases
                WHERE nombre LIKE ? OR instructor LIKE ? OR fecha LIKE ?
            """, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute("SELECT id, nombre, instructor, horario, capacidad, fecha FROM clases")

        clases = cursor.fetchall()
        conn.close()

        if not clases:
            ctk.CTkLabel(self.frame_clases, text="No se encontraron clases.",
                         text_color="gray").pack(pady=10)
            return

        for clase in clases:
            frame = ctk.CTkFrame(self.frame_clases, fg_color="white", corner_radius=10)
            frame.pack(pady=5, fill="x", padx=10)

            texto = f"{clase[1]} - {clase[2]} - {clase[3]} - Capacidad: {clase[4]} - Fecha: {clase[5]}"
            ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 13), text_color="#2C3E50").pack(side="left", padx=10)

            ctk.CTkButton(frame, text="✏ Editar", width=70, height=30,
                          fg_color="#3498DB", hover_color="#2980B9",
                          command=lambda cid=clase[0]: self.editar_clase(cid)).pack(side="right", padx=5)

            ctk.CTkButton(frame, text="🗑 Eliminar", width=80, height=30,
                          fg_color="#E74C3C", hover_color="#C0392B",
                          command=lambda cid=clase[0]: self.eliminar_clase(cid)).pack(side="right", padx=5)

    def guardar_clase(self):
        nombre = self.entry_nombre.get()
        instructor = self.entry_instructor.get()
        horario = self.entry_horario.get()
        capacidad = self.entry_capacidad.get()
        fecha = self.date_picker.get_date().strftime('%Y-%m-%d')

        if not (nombre and instructor and horario and capacidad.isdigit()):
            messagebox.showerror("Error", "Completa todos los campos correctamente")
            return

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clases (nombre, instructor, horario, capacidad, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, instructor, horario, int(capacidad), fecha))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Clase agregada correctamente")
        self.limpiar_formulario()
        self.mostrar_clases()

    def editar_clase(self, clase_id):
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, instructor, horario, capacidad, fecha FROM clases WHERE id=?", (clase_id,))
        clase = cursor.fetchone()
        conn.close()

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, clase[0])
        self.entry_instructor.delete(0, "end")
        self.entry_instructor.insert(0, clase[1])
        self.entry_horario.delete(0, "end")
        self.entry_horario.insert(0, clase[2])
        self.entry_capacidad.delete(0, "end")
        self.entry_capacidad.insert(0, str(clase[3]))
        self.date_picker.set_date(clase[4])

        self.boton_guardar.configure(text="Actualizar clase", fg_color="#F39C12",
                                     hover_color="#D68910",
                                     command=lambda: self.actualizar_clase(clase_id))
    def actualizar_clase(self, clase_id):
        nombre = self.entry_nombre.get()
        instructor = self.entry_instructor.get()
        horario = self.entry_horario.get()
        capacidad = self.entry_capacidad.get()
        fecha = self.date_picker.get_date().strftime('%Y-%m-%d')

        if not (nombre and instructor and horario and capacidad.isdigit()):
            messagebox.showerror("Error", "Completa todos los campos correctamente")
            return

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clases
            SET nombre=?, instructor=?, horario=?, capacidad=?, fecha=?
            WHERE id=?
        """, (nombre, instructor, horario, int(capacidad), fecha, clase_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Clase actualizada correctamente")
        self.limpiar_formulario()
        self.boton_guardar.configure(text="💾 Guardar clase", fg_color="#ffe066",
                                     hover_color="#D68910",
                                     command=self.guardar_clase)
        self.mostrar_clases()
    def eliminar_clase(self, clase_id):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta clase?")
        if respuesta:
            conn = sqlite3.connect("gimnasio.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clases WHERE id=?", (clase_id,))
            conn.commit()
            conn.close()
            self.mostrar_clases()
    def limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_instructor.delete(0, "end")
        self.entry_horario.delete(0, "end")
        self.entry_capacidad.delete(0, "end")
        self.date_picker.set_date(datetime.date.today())
    def volver(self):
        self.destroy()
        from rol_selector import RolSelector
        RolSelector().mainloop()
if __name__ == "__main__":
    app = AdminPanel()
    app.mainloop()