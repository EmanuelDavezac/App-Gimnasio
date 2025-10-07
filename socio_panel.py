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
        self.configure(fg_color="#5b8fd6")  # Configura el color de fondo principal

        # Fondo con imagen
        try:
            bg_image = ctk.CTkImage(Image.open("assets/fondo_gym.jpg"), size=(800, 800))
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(relwidth=1, relheight=1)  # Coloca la imagen de fondo cubriendo toda la ventana
        except Exception:
            pass

        # Contenedor principal
        main_frame = ctk.CTkFrame(self, fg_color="#fff7b2")
        main_frame.pack(pady=20, padx=30, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Columna izquierda
        left_frame = ctk.CTkFrame(main_frame, fg_color="#e3f6fc", corner_radius=20, border_width=3, border_color="#b2cfff")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        ctk.CTkButton(left_frame, text="⬅ Volver", fg_color="#7ea6e0",
                      hover_color="#5b8fd6", text_color="#fff", command=self.volver,
                      height=30, width=100).pack(pady=(10, 5))  # Boton para volver a rol selector

        ctk.CTkLabel(left_frame, text="📅 Seleccioná un día para ver clases",
                     font=("Arial Rounded MT Bold", 18), text_color="#5b8fd6").pack(pady=5)

        # Calendario
        self.calendario = Calendar(left_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                                   background="#fff7b2", disabledbackground="#fff7b2", bordercolor="#5b8fd6",
                                   headersbackground="#fff7b2", normalbackground="#fff7b2", foreground="#5b8fd6",
                                   weekendbackground="#fff7b2", weekendforeground="#5b8fd6",
                                   othermonthbackground="#f7e9a0", othermonthwebackground="#f7e9a0",
                                   selectbackground="#ffe066", selectforeground="#fff7b2")
        self.calendario.pack(pady=5)

        # Obtiene fechas de la base de datos que tienen clases y las marca en el calendario
        fechas_con_clases = self.obtener_fechas_con_clases()
        for fecha in fechas_con_clases:
            self.calendario.calevent_create(fecha, "Clase disponible", "clase")
        self.calendario.tag_config("clase", background="#5b8fd6", foreground="#fff7b2")

        ctk.CTkButton(left_frame, text="Ver clases disponibles",
                      fg_color="#5b8fd6", hover_color="#7ea6e0", text_color="#fff7b2",
                      height=35, command=self.mostrar_clases_por_fecha).pack(pady=5)  # Muestra clases para la fecha seleccionada

        # Botón Mis reservas
        ctk.CTkButton(left_frame, text="Mis reservas →", fg_color="#ffe066",
                      hover_color="#ffe699", text_color="#5b8fd6",
                      command=self.toggle_reservas, height=35, width=180).pack(pady=(5, 10))  # Muestra/oculta panel de reservas

        self.frame_clases = ctk.CTkScrollableFrame(left_frame, width=350, height=300,
                                                   fg_color="#e3f6fc", scrollbar_button_color="#e3f6fc",
                                                   scrollbar_fg_color="#e3f6fc")
        self.frame_clases.pack(pady=(10, 20), padx=10, fill="both", expand=True)  # Contenedor donde se listan las clases

        # Panel derecho ocultable
        self.right_frame = None
        self.reservas_visible = False

    # Mostrar u ocultar reservas
    def toggle_reservas(self):
        if self.reservas_visible:
            if self.right_frame:
                self.right_frame.destroy()
            self.reservas_visible = False
        else:
            self.right_frame = ctk.CTkFrame(self, fg_color="#fff7b2", corner_radius=20,
                                            border_width=3, border_color="#ffe066")
            self.right_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8)

            ctk.CTkLabel(self.right_frame, text="🧾 Mis reservas",
                         font=("Arial Rounded MT Bold", 18), text_color="#5b8fd6").pack(pady=(10, 5))

            self.frame_reservas = ctk.CTkScrollableFrame(self.right_frame, width=350, height=500,
                                                         fg_color="#fff7b2", scrollbar_button_color="#fff7b2",
                                                         scrollbar_fg_color="#fff7b2")
            self.frame_reservas.pack(pady=(10, 20), padx=10, fill="both", expand=True)

            self.ver_reservas()  # Carga las reservas del usuario
            self.reservas_visible = True

    # Obtiene todas las fechas que tienen clases en la BD
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

    # Muestra todas las clases disponibles para la fecha seleccionada
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

        # Limpia el frame antes de agregar nuevas clases
        for widget in self.frame_clases.winfo_children():
            widget.destroy()

        if clases:
            for clase in clases:
                disponibles = clase[4] - clase[5]
                texto = f"🏋️ {clase[1]} | {clase[2]} | {clase[3]} | Cupos: {disponibles}"
                color = "#5b8fd6" if disponibles > 0 else "#bdbdbd"
                btn = ctk.CTkButton(self.frame_clases, text=texto,
                                    fg_color=color, hover_color="#7ea6e0", text_color="#fff7b2",
                                    height=35,
                                    state="normal" if disponibles > 0 else "disabled",
                                    command=lambda cid=clase[0]: self.reservar_clase(cid, fecha))  # Boton para reservar
                btn.pack(pady=3, padx=8, fill="x")
        else:
            lbl = ctk.CTkLabel(self.frame_clases, text="No hay clases ese día 🙁", text_color="#5b8fd6")
            lbl.pack(pady=10)

    # Hace la reserva de una clase
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
        self.ver_reservas()  # Actualiza la lista de reservas después de reservar

    # Muestra las reservas del usuario
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
                frame = ctk.CTkFrame(self.frame_reservas, fg_color="#fff7b2")
                frame.pack(pady=5, fill="x", padx=10)

                texto = f"• {r[1]} - {r[2]} - {r[3]} - {r[4]}"
                ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 13),
                             text_color="#5b8fd6").pack(side="left", padx=10)

                ctk.CTkButton(frame, text="🗑 Cancelar", width=100, height=30,
                              fg_color="#ffe066", hover_color="#ffe699",
                              text_color="#5b8fd6",
                              command=lambda rid=r[0]: self.cancelar_reserva(rid)).pack(side="right", padx=5)  # Botón para cancelar reserva

    # Cancela una reserva
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
            self.mostrar_clases_por_fecha()  # Actualiza la lista de clases disponibles

    # Vuelve al selector de rol
    def volver(self):
        self.destroy()
        from rol_selector import RolSelector
        RolSelector().mainloop()
