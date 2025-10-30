import tkinter as tk
from tkinter import filedialog
import json
from recomendaciones import RECOMENDACIONES, MENU_SIMPLIFICADO

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Arial", 10), wraplength=250)
        label.pack(ipadx=5, ipady=5)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class IngenieroACC:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingeniero de Pista ACC")
        self.root.geometry("900x700")
        self.setup = None
        self.cambios = []

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.menu_principal()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------------- HOME ----------------
    def menu_principal(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Ingeniero de Pista ACC", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.main_frame, text="Cargar setup", font=("Arial", 14),
                  width=30, height=2, command=self.cargar_setup).pack(pady=10)
        tk.Button(self.main_frame, text="Continuar sin setup", font=("Arial", 14),
                  width=30, height=2, command=self.continuar_sin_setup).pack(pady=10)

        if self.cambios:
            tk.Button(self.main_frame, text="Borrar todo y volver a home", font=("Arial", 12),
                      command=self.resetear_todo).pack(pady=20)

        self.mostrar_resumen()

    def resetear_todo(self):
        self.cambios = []
        self.setup = None
        self.menu_principal()

    def cargar_setup(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.setup = json.load(f)
                self.menu_categorias()
            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo leer el setup:\n{e}")

    def continuar_sin_setup(self):
        self.menu_categorias()

    # ---------------- CATEGORIAS ----------------
    def menu_categorias(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Menú Principal", font=("Arial", 22)).pack(pady=20)

        for categoria in MENU_SIMPLIFICADO.keys():
            tk.Button(self.main_frame, text=categoria, font=("Arial", 14),
                      width=40, height=2,
                      command=lambda c=categoria: self.menu_sintomas(c)).pack(pady=10)

        tk.Button(self.main_frame, text="Volver al home", font=("Arial", 12),
                  command=self.menu_principal).pack(pady=20)

    # ---------------- SINTOMAS ----------------
    def menu_sintomas(self, categoria):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"{categoria}", font=("Arial", 20)).pack(pady=20)

        for sintoma in MENU_SIMPLIFICADO[categoria]:
            tk.Button(self.main_frame, text=sintoma, font=("Arial", 12),
                      width=60, height=2,
                      command=lambda s=sintoma: self.menu_recomendaciones(categoria, s)).pack(pady=5)

        tk.Button(self.main_frame, text="Volver al menú principal", font=("Arial", 12),
                  command=self.menu_categorias).pack(pady=20)

    # ---------------- RECOMENDACIONES ----------------
    def menu_recomendaciones(self, categoria, sintoma):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"{sintoma}", font=("Arial", 20)).pack(pady=20)

        recomendaciones = RECOMENDACIONES[categoria][sintoma]

        for rec in recomendaciones:
            btn = tk.Button(self.main_frame, text=rec["accion"], font=("Arial", 12),
                            width=60, height=2)
            btn.pack(pady=5)

            ToolTip(btn, rec.get("desc",""))

            def apply_rec(r=rec):
                self.cambios.append(r)
                msg = f"Aplicado: {r['accion']} {r['change']}{r['unit']}"
                temp = tk.Toplevel(self.root)
                temp.geometry("300x100+400+300")
                tk.Label(temp, text=msg, font=("Arial", 12)).pack(expand=True)
                self.root.after(2000, temp.destroy)
                self.revisar_setup_botones()
                self.mostrar_resumen()

            btn.config(command=apply_rec)

        # Navegación
        nav_frame = tk.Frame(self.main_frame)
        nav_frame.pack(pady=20)
        tk.Button(nav_frame, text="Volver al menú de síntomas", font=("Arial", 12),
                  command=lambda c=categoria: self.menu_sintomas(c)).pack(side="left", padx=10)
        tk.Button(nav_frame, text="Volver al menú principal", font=("Arial", 12),
                  command=self.menu_categorias).pack(side="left", padx=10)

        self.mostrar_resumen()

    # ---------------- RESUMEN ----------------
    def mostrar_resumen(self):
        if not self.cambios:
            return
        frame = tk.Frame(self.main_frame, relief="solid", borderwidth=2, background="#e0f7fa")
        frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(frame, text="Resumen de recomendaciones aplicadas:", font=("Arial", 14, "bold"),
                 background="#e0f7fa").pack(pady=5)
        for idx, c in enumerate(self.cambios):
            item_frame = tk.Frame(frame, background="#e0f7fa")
            item_frame.pack(fill="x", padx=5, pady=2)
            tk.Label(item_frame, text=f"- {c['accion']} {c['change']}{c['unit']}",
                     background="#e0f7fa").pack(side="left", anchor="w")
            tk.Button(item_frame, text="X", font=("Arial", 8), width=2,
                      command=lambda i=idx: self.eliminar_cambio(i)).pack(side="right")

        if self.cambios:
            tk.Button(frame, text="Revisar setup", font=("Arial", 12),
                      command=self.menu_revisar_setup).pack(pady=5)

    def eliminar_cambio(self, idx):
        del self.cambios[idx]
        self.menu_principal()

    # ---------------- REVISAR SETUP ----------------
    def menu_revisar_setup(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Revisar Setup", font=("Arial", 20)).pack(pady=20)

        for c in self.cambios:
            tk.Label(self.main_frame, text=f"- {c['accion']} {c['change']}{c['unit']}", font=("Arial", 12)).pack(anchor="w")

        # Botones exportar/cargar
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=20)
        if self.setup:
            tk.Button(btn_frame, text="Exportar setup modificado", font=("Arial", 12),
                      command=self.exportar_setup).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cargar setup con cambios", font=("Arial", 12),
                  command=self.cargar_setup_con_cambios).pack(side="left", padx=10)

        tk.Button(self.main_frame, text="Volver al menú principal", font=("Arial", 12),
                  command=self.menu_principal).pack(pady=10)

    def exportar_setup(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if file_path:
            # Aplicar cambios a setup y exportar
            for c in self.cambios:
                self.aplicar_cambio(self.setup, c)
            with open(file_path, "w") as f:
                json.dump(self.setup, f, indent=4)
            tk.messagebox.showinfo("Éxito", f"Setup exportado a {file_path}")

    def cargar_setup_con_cambios(self):
        if not self.setup:
            tk.messagebox.showerror("Error", "No se cargó ningún setup inicial")
            return
        for c in self.cambios:
            self.aplicar_cambio(self.setup, c)
        tk.messagebox.showinfo("Éxito", "Cambios aplicados al setup")

    def aplicar_cambio(self, setup_obj, cambio):
        obj = setup_obj
        for p in cambio["path"][:-1]:
            obj = obj[p]
        obj[cambio["path"][-1]] = self.calcular_nuevo_valor(obj[cambio["path"][-1]], cambio["change"])

    def calcular_nuevo_valor(self, valor_actual, cambio):
        try:
            if isinstance(valor_actual, (int, float)):
                if isinstance(cambio, str):
                    if cambio.startswith("+"):
                        return valor_actual + float(cambio[1:])
                    elif cambio.startswith("-"):
                        return valor_actual - float(cambio[1:])
                else:
                    return cambio
        except:
            pass
        return valor_actual

    def revisar_setup_botones(self):
        pass  # placeholder para habilitar botones de revisión si se desea

if __name__ == "__main__":
    root = tk.Tk()
    app = IngenieroACC(root)
    root.mainloop()
