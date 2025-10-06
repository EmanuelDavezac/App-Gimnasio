import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox
import datetime
import os
from PIL import Image


class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Administrador")
        self.geometry("800x650")

        # =============== Fondo con imagen =================
        ruta_base = os.path.dirname(__file__)
        fondo_path = os.path.join(ruta_base, "assets", "fondo_azul.jpg")

        if os.path.exists(fondo_path):
            bg_image = ctk.CTkImage(
                light_image=Image.open(fondo_path),
                size=(800, 650)
            )
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Capa semitransparente sobre el fondo
            overlay = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
            overlay.place(x=0, y=0, relwidth=1, relheight=1)

        # =============== Título =================
        ctk.CTkLabel(
            self,
            text="🧩 Panel de Administración",
            font=("Segoe UI", 24, "bold"),
            text_color="#2C3E50"
        ).pack(pady=(15, 10))

        # =============== Botón Volver =================
        ctk.CTkButton(
            self,
            text="⬅ Volver",
            fg_color="#4A90E2",
            hover_color="#357ABD",
            text_color="white",
            corner_radius=20,
            width=100,
            command=self.volver
        ).pack(pady=(0, 15))

        # =============== Marco del formulario =================
        form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        form_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(form_frame, text="Agregar nueva clase",
                     font=("Segoe UI", 18, "bold"), text_color="#34495E").pack(pady=(15, 10))

        # Entradas
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre de la clase", height=35)
        self.entry_nombre.pack(pady=5, padx=20)

        self.entry_instructor = ctk.CTkEntry(form_frame, placeholder_text="Instructor", height=35)
        self.entry_instructor.pack(pady=5, padx=20)

        self.entry_horario = ctk.CTkEntry(form_frame, placeholder_text="Horario (ej: 18:00)", height=35)
        self.entry_horario.pack(pady=5, padx=20)

        self.entry_capacidad = ctk.CTkEntry(form_frame, placeholder_text="Capacidad", height=35)
        self.entry_capacidad.pack(pady=5, padx=20)

        ctk.CTkLabel(form_frame, text="Fecha de la clase", font=("Segoe UI", 14)).pack(pady=(10, 5))
        self.date_picker = DateEntry(form_frame, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=(0, 10))

        self.boton_guardar = ctk.CTkButton(
            form_frame,
            text="💾 Guardar clase",
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=35,
            corner_radius=10,
            command=self.guardar_clase
        )
        self.boton_guardar.pack(pady=(10, 20))

        # =============== Línea divisoria =================
        ctk.CTkFrame(self, height=2, fg_color="#BDC3C7").pack(fill="x", padx=30, pady=10)

        # =============== Sección de clases existentes =================
        ctk.CTkLabel(
            self,
            text="📚 Clases existentes",
            font=("Segoe UI", 18, "bold"),
            text_color="#2C3E50"
        ).pack(pady=5)

        self.frame_clases = ctk.CTkScrollableFrame(self, width=740, height=300, fg_color="#F7F9F9")
        self.frame_clases.pack(pady=10, padx=30, fill="both", expand=True)

        self.mostrar_clases()

    # =============== CRUD =================
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

    def mostrar_clases(self):
        for widget in self.frame_clases.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, instructor, horario, capacidad, fecha FROM clases")
        clases = cursor.fetchall()
        conn.close()

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
        self.boton_guardar.configure(text="💾 Guardar clase", fg_color="#27AE60",
                                     hover_color="#1E8449",
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
