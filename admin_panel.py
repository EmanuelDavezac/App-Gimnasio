import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox
from datetime import datetime

class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Administrador")
        self.geometry("700x600")

        ctk.CTkLabel(self, text="Agregar nueva clase", font=("Arial", 18)).pack(pady=10)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre de la clase")
        self.entry_nombre.pack(pady=5)

        self.entry_instructor = ctk.CTkEntry(self, placeholder_text="Instructor")
        self.entry_instructor.pack(pady=5)

        self.entry_horario = ctk.CTkEntry(self, placeholder_text="Horario (ej: 18:00)")
        self.entry_horario.pack(pady=5)

        self.entry_capacidad = ctk.CTkEntry(self, placeholder_text="Capacidad")
        self.entry_capacidad.pack(pady=5)

        ctk.CTkLabel(self, text="Fecha de la clase").pack(pady=5)
        self.date_picker = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=5)

        self.boton_guardar = ctk.CTkButton(self, text="Guardar clase", command=self.guardar_clase)
        self.boton_guardar.pack(pady=10)

        ctk.CTkLabel(self, text="Clases existentes", font=("Arial", 16)).pack(pady=10)
        self.frame_clases = ctk.CTkScrollableFrame(self, width=650, height=300)
        self.frame_clases.pack(pady=10)

        self.mostrar_clases()

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
            frame = ctk.CTkFrame(self.frame_clases)
            frame.pack(pady=5, fill="x", padx=10)

            texto = f"{clase[1]} - {clase[2]} - {clase[3]} - Capacidad: {clase[4]} - Fecha: {clase[5]}"
            ctk.CTkLabel(frame, text=texto).pack(side="left", padx=10)

            ctk.CTkButton(frame, text="Editar", command=lambda cid=clase[0]: self.editar_clase(cid)).pack(side="right", padx=5)
            ctk.CTkButton(frame, text="Eliminar", fg_color="red", command=lambda cid=clase[0]: self.eliminar_clase(cid)).pack(side="right", padx=5)

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

        self.boton_guardar.configure(text="Actualizar clase", command=lambda: self.actualizar_clase(clase_id))

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
        self.boton_guardar.configure(text="Guardar clase", command=self.guardar_clase)
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