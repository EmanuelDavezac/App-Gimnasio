from tkcalendar import Calendar
import sqlite3
from tkinter import messagebox
import customtkinter as ctk


class SocioPanel(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"Panel de Socio - {usuario}")
        self.geometry("700x950")

        self.label_titulo = ctk.CTkLabel(self, text="Seleccioná un día para ver clases", font=("Arial", 20))
        self.label_titulo.pack(pady=10)

        self.calendario = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.pack(pady=10)

        self.boton_ver_clases = ctk.CTkButton(self, text="Ver clases ese día", command=self.mostrar_clases_por_fecha)
        self.boton_ver_clases.pack(pady=10)

        self.frame_clases = ctk.CTkScrollableFrame(self, width=600, height=250)
        self.frame_clases.pack(pady=10)

        self.label_titulo_historial = ctk.CTkLabel(self, text="Ver mis reservas", font=("Arial", 20))
        self.label_titulo_historial.pack(pady=10) # Agregado el título para el historial
        

        self.historial = ctk.CTkTextbox(self, width=600, height=150)
        self.historial.pack(pady=10)

        self.ver_reservas()

    def mostrar_clases_por_fecha(self):
        fecha = self.calendario.get_date()
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.nombre, c.instructor, c.horario, c.capacidad,
                   (SELECT COUNT(*) FROM reservas r WHERE r.clase_id = c.id AND r.fecha = ?) AS ocupados
            FROM clases c
            WHERE c.fecha = ?
        """, (fecha, fecha))
        clases = cursor.fetchall()
        conn.close()

        for widget in self.frame_clases.winfo_children():
            widget.destroy()

        if clases:
            for clase in clases:
                disponibles = clase[4] - clase[5]
                texto = f"{clase[1]} - {clase[2]} - {clase[3]} | Cupos: {disponibles}"
                btn = ctk.CTkButton(self.frame_clases, text=texto, command=lambda cid=clase[0]: self.reservar_clase(cid, fecha))
                btn.pack(pady=5)
        else:
            lbl = ctk.CTkLabel(self.frame_clases, text="No hay clases ese día")
            lbl.pack()

    def reservar_clase(self, clase_id, fecha):
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()

        # Verificar si la clase existe
        cursor.execute("SELECT capacidad FROM clases WHERE id=?", (clase_id,))
        clase = cursor.fetchone()
        if not clase:
            messagebox.showerror("Error", "Clase no encontrada.")
            conn.close()
            return

        capacidad = clase[0]

        # Verificar si el usuario ya reservó esa clase en esa fecha
        cursor.execute("""
            SELECT id FROM reservas 
            WHERE usuario=? AND clase_id=? AND fecha=?
        """, (self.usuario, clase_id, fecha))
        existe = cursor.fetchone()

        if existe:
            messagebox.showerror("Error", "Ya reservaste esta clase en esa fecha.")
            conn.close()
            return

        # Verificar si hay cupos disponibles
        cursor.execute("SELECT COUNT(*) FROM reservas WHERE clase_id=? AND fecha=?", (clase_id, fecha))
        ocupados = cursor.fetchone()[0]

        if ocupados >= capacidad:
            messagebox.showerror("Error", "Clase sin cupos disponibles.")
        else:
            cursor.execute("INSERT INTO reservas (usuario, clase_id, fecha) VALUES (?, ?, ?)", (self.usuario, clase_id, fecha))
            conn.commit()
            messagebox.showinfo("Éxito", f"Reserva realizada para el {fecha}")
            self.mostrar_clases_por_fecha()

        conn.close()


    def ver_reservas(self):
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, c.instructor, c.horario, r.fecha
            FROM reservas r
            JOIN clases c ON r.clase_id = c.id
            WHERE r.usuario = ?
            ORDER BY r.fecha
        """, (self.usuario,))
        reservas = cursor.fetchall()
        conn.close()

        self.historial.delete("1.0", "end")
        if not reservas:
            self.historial.insert("end", "No tenés reservas.\n")
        else:
            for r in reservas:
                self.historial.insert("end", f"{r[0]} - {r[1]} - {r[2]} - {r[3]}\n")
        self.historial.configure(state="disabled")