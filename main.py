import tkinter as tk
from interfaz import VentanaPrincipal

def main():
    # Inicializa el motor de ventanas de Python
    root = tk.Tk()
    
    # Carga la interfaz gráfica que creamos
    app = VentanaPrincipal(root)
    
    # Mantiene la ventana abierta esperando clics
    root.mainloop()

if __name__ == "__main__":
    main()
