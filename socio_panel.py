import customtkinter as ctk
from tkcalendar import Calendar
import sqlite3
from tkinter import messagebox
from PIL import Image
from datetime import datetime

class SocioPanel(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"Panel de Socio - {usuario}")
        self.geometry("800x800")
        self.configure(fg_color="#f0f0f5")

        # ==== Fondo con imagen ====
        try:
            bg_image = ctk.CTkImage(Image.open("assets/fondo_gym.jpg"), size=(800, 800))
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(relwidth=1, relheight=1)
        except Exception:
            pass

        # ==== Contenedor principal ====
        contenedor = ctk.CTkFrame(self, fg_color="white")
        contenedor.pack(pady=20, padx=30, fill="both", expand=True)

        # ==== Botón volver ====
        ctk.CTkButton(contenedor, text="⬅ Volver", fg_color="gray",
                      hover_color="#4a4a4a", command=self.volver,
                      height=30, width=100).pack(pady=(10, 5))

        # ==== Título ====
        ctk.CTkLabel(contenedor, text="📅 Seleccioná un día para ver clases",
                     font=("Arial Rounded MT Bold", 18)).pack(pady=5)

        # ==== Calendario ====
        self.calendario = Calendar(contenedor, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.pack(pady=5)

        # 🔵 Pintar días con clases
        fechas_con_clases = self.obtener_fechas_con_clases()
        for fecha in fechas_con_clases:
            self.calendario.calevent_create(fecha, "Clase disponible", "clase")
        self.calendario.tag_config("clase", background="#b60000", foreground="white")

        # ==== Botón ver clases ====
        ctk.CTkButton(contenedor, text="Ver clases disponibles",
                      fg_color="#0077b6", hover_color="#005f8f",
                      height=35, command=self.mostrar_clases_por_fecha).pack(pady=5)

        # ==== Clases del día ====
        self.frame_clases = ctk.CTkScrollableFrame(contenedor, width=600, height=200)
        self.frame_clases.pack(pady=5)

        # ==== Título reservas ====
        ctk.CTkLabel(contenedor, text="🧾 Mis reservas",
                     font=("Arial Rounded MT Bold", 18)).pack(pady=(10, 5))

        # ==== Historial de reservas ====
        self.frame_reservas = ctk.CTkScrollableFrame(contenedor, width=600, height=200)
        self.frame_reservas.pack(pady=5)

        self.ver_reservas()

    def obtener_fechas_con_clases(self):
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT fecha FROM clases")
        fechas_raw = [row[0] for row in cursor.fetchall()]
        conn.close()

        fechas_convertidas = []
        for f in fechas_raw:
            try:
                fecha_obj = datetime.strptime(f, "%Y-%m-%d").date()
                fechas_convertidas.append(fecha_obj)
            except ValueError:
                pass

        return fechas_convertidas


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
                texto = f"🏋️ {clase[1]} | {clase[2]} | {clase[3]} | Cupos: {disponibles}"
                color = "#0077b6" if disponibles > 0 else "gray"
                btn = ctk.CTkButton(self.frame_clases, text=texto,
                                    fg_color=color, hover_color="#005f8f",
                                    height=35,
                                    state="normal" if disponibles > 0 else "disabled",
                                    command=lambda cid=clase[0]: self.reservar_clase(cid, fecha))
                btn.pack(pady=3, padx=8, fill="x")
        else:
            lbl = ctk.CTkLabel(self.frame_clases, text="No hay clases ese día 🙁", text_color="gray")
            lbl.pack(pady=10)

    def reservar_clase(self, clase_id, fecha):
        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT capacidad FROM clases WHERE id=?", (clase_id,))
        clase = cursor.fetchone()

        if not clase:
            messagebox.showerror("Error", "Clase no encontrada.")
            conn.close()
            return

        capacidad = clase[0]
        cursor.execute("SELECT id FROM reservas WHERE usuario=? AND clase_id=? AND fecha=?",
                       (self.usuario, clase_id, fecha))
        existe = cursor.fetchone()

        if existe:
            messagebox.showerror("Error", "Ya reservaste esta clase en esa fecha.")
            conn.close()
            return

        cursor.execute("SELECT COUNT(*) FROM reservas WHERE clase_id=? AND fecha=?", (clase_id, fecha))
        ocupados = cursor.fetchone()[0]

        if ocupados >= capacidad:
            messagebox.showerror("Error", "Clase sin cupos disponibles.")
        else:
            cursor.execute("INSERT INTO reservas (usuario, clase_id, fecha) VALUES (?, ?, ?)",
                           (self.usuario, clase_id, fecha))
            conn.commit()
            messagebox.showinfo("Éxito", f"Reserva realizada para el {fecha}")
            self.mostrar_clases_por_fecha()

        conn.close()
        self.ver_reservas()

    def ver_reservas(self):
        for widget in self.frame_reservas.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("gimnasio.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, c.nombre, c.instructor, c.horario, r.fecha
            FROM reservas r
            JOIN clases c ON r.clase_id = c.id
            WHERE r.usuario = ?
            ORDER BY r.fecha
        """, (self.usuario,))
        reservas = cursor.fetchall()
        conn.close()

        if not reservas:
            ctk.CTkLabel(self.frame_reservas, text="No tenés reservas.",
                         text_color="gray").pack(pady=10)
        else:
            for r in reservas:
                frame = ctk.CTkFrame(self.frame_reservas)
                frame.pack(pady=5, fill="x", padx=10)

                texto = f"• {r[1]} - {r[2]} - {r[3]} - {r[4]}"
                ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 13),
                             text_color="#2C3E50").pack(side="left", padx=10)

                ctk.CTkButton(frame, text="🗑 Cancelar", width=100, height=30,
                              fg_color="#E74C3C", hover_color="#C0392B",
                              text_color="white",
                              command=lambda rid=r[0]: self.cancelar_reserva(rid)).pack(side="right", padx=5)

    def cancelar_reserva(self, reserva_id):
        respuesta = messagebox.askyesno("Confirmar", "¿Querés cancelar esta reserva?")
        if respuesta:
            conn = sqlite3.connect("gimnasio.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservas WHERE id=?", (reserva_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Cancelado", "Reserva eliminada correctamente.")
            self.ver_reservas()
            self.mostrar_clases_por_fecha()

    def volver(self):
        self.destroy()
        from rol_selector import RolSelector
        RolSelector().mainloop()