# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
from logica import SistemaPolinizacion

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Camino de Polinización")
        self.root.geometry("850x500")
        self.root.configure(bg="#FFF8E7") # Fondo color crema/miel

        self.sistema = SistemaPolinizacion()
        self.camino_optimo = []

        #  PANEL LATERAL DE CONTROLES 
        panel_control = tk.Frame(self.root, bg="#FFF8E7", width=220)
        panel_control.pack(side="left", fill="y", padx=20, pady=20)

        tk.Label(panel_control, text=" Camino de una abeja ", font=("Segoe UI", 14, "bold"), fg="#5D4037", bg="#FFF8E7").pack(pady=10)

        # Selectores de Origen y Destino
        nodos_disponibles = list(self.sistema.nodos.keys())
        
        tk.Label(panel_control, text="Origen:", font=("Segoe UI", 10), bg="#FFF8E7").pack(anchor="w")
        self.cb_origen = ttk.Combobox(panel_control, values=nodos_disponibles, state="readonly")
        self.cb_origen.pack(fill="x", pady=5)
        self.cb_origen.set("Colmena")

        tk.Label(panel_control, text="Destino:", font=("Segoe UI", 10), bg="#FFF8E7").pack(anchor="w")
        self.cb_destino = ttk.Combobox(panel_control, values=nodos_disponibles, state="readonly")
        self.cb_destino.pack(fill="x", pady=5)
        self.cb_destino.set("Flor E")

        # Botón de cálculo
        btn_calcular = tk.Button(panel_control, text="Calcular Ruta", font=("Segoe UI", 11, "bold"), bg="#84CC16", fg="white", bd=0, pady=5, command=self.procesar_ruta)
        btn_calcular.pack(fill="x", pady=20)

        # Etiqueta de resultados
        self.lbl_resultado = tk.Label(panel_control, text="Selecciona la ruta\ny presiona Calcular.", font=("Segoe UI", 10), bg="#FFF8E7", fg="#5D4037", justify="left")
        self.lbl_resultado.pack(fill="x", pady=10)

        
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=1, highlightbackground="#E5E7EB")
        self.canvas.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.dibujar_jardin()

    def dibujar_jardin(self):
        self.canvas.delete("all")

        # 1. Dibujar Caminos (Aristas)
        for u, v, peso in self.sistema.aristas:
            x1, y1 = self.sistema.nodos[u]
            x2, y2 = self.sistema.nodos[v]
            
            # Si el camino pertenece a la ruta óptima, lo pintamos de amarillo grueso
            es_optimo = False
            if u in self.camino_optimo and v in self.camino_optimo:
                if abs(self.camino_optimo.index(u) - self.camino_optimo.index(v)) == 1:
                    es_optimo = True
            
            color = "#F6C445" if es_optimo else "#E5E7EB"
            ancho = 4 if es_optimo else 2
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)
            
            # Dibujar el costo en medio de la línea
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my-10, text=str(peso), font=("Segoe UI", 9, "bold"), fill="#5D4037")

        # 2. Dibujar Flores/Colmena (Nodos)
        for nombre, (x, y) in self.sistema.nodos.items():
            color_nodo = "#F59E0B" if nombre == "Colmena" else "#84CC16"
            
            # Círculo del nodo
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color_nodo, outline="#5D4037", width=2)
            # Etiqueta del nodo
            self.canvas.create_text(x, y+30, text=nombre, font=("Segoe UI", 9, "bold"), fill="#5D4037")

    def procesar_ruta(self):
        origen = self.cb_origen.get()
        destino = self.cb_destino.get()

        if origen == destino:
            messagebox.showwarning("Atención", "El origen y el destino no pueden ser iguales.")
            return

        # Calcular mediante lógica pura
        camino, costo = self.sistema.calcular_dijkstra(origen, destino)
        
        self.camino_optimo = camino
        self.dibujar_jardin() # Redibuja para resaltar las líneas amarillas

        # Actualizar texto informativo
        texto_ruta = " → \n".join(camino)
        self.lbl_resultado.config(text=f"Distancia: {costo} u.\n\nRuta óptima:\n{texto_ruta}")

        # Iniciar animación de la abeja
        self.animar_abeja(0)

    def animar_abeja(self, indice):
        if indice >= len(self.camino_optimo):
            return

        nodo_actual = self.camino_optimo[indice]
        x, y = self.sistema.nodos[nodo_actual]

        # Borrar el rastro anterior de la abeja
        self.canvas.delete("abeja")
        
        # Dibujar la abeja (un círculo amarillo con alas grises básico)
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="yellow", outline="black", tags="abeja")
        self.canvas.create_oval(x-5, y-15, x+5, y-5, fill="lightblue", tags="abeja") # Alita

        # Programar el siguiente movimiento en 600 milisegundos
        self.root.after(600, lambda: self.animar_abeja(indice + 1))
