import tkinter as tk
from tkinter import ttk, messagebox
import string
import platform  # Para detectar el sistema operativo

# Importar los métodos existentes
from northwest_corner.northwest_corner import northwest_corner_method
from vogel_approximation.vogel_approximation import vogel_approximation_method
from minimum_cost.minimum_cost import minimum_cost_method

# Importar los nuevos métodos
from sequential_steps.sequential_steps import sequential_steps_method
from modified_distribution.modified_distribution import modified_distribution_method

def calculate_cost(allocations, costs):
    total = 0
    for ((i, j), alloc) in allocations:
        total += alloc * costs[i][j]
    return total

def index_to_letter(index):
    if index < 26:
        return string.ascii_uppercase[index]
    else:
        # Para índices >=26, usar letras dobles como AA, AB, etc.
        return string.ascii_uppercase[index // 26 - 1] + string.ascii_uppercase[index % 26]

class ScrollableFrame(ttk.Frame):
    """
    Un frame desplazable que puede contener otros widgets y responde a la rueda del ratón.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Detectar la plataforma
        self.platform = platform.system()
        
        # Enlazar eventos de la rueda del ratón
        if self.platform == "Windows":
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        elif self.platform == "Darwin":  # macOS
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_mac)
        else:  # Linux y otros
            self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)
        
        # Opcional: Cambiar el cursor para indicar que es desplazable
        self.canvas.configure(cursor="hand2")

    def _on_mousewheel_windows(self, event):
        # En Windows, event.delta es positivo hacia arriba y negativo hacia abajo
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_mac(self, event):
        # En macOS, event.delta es generalmente muy pequeño, se multiplica para mayor sensibilidad
        self.canvas.yview_scroll(int(-1*event.delta), "units")

    def _on_mousewheel_linux(self, event):
        # En Linux, los eventos de desplazamiento vienen en Button-4 (arriba) y Button-5 (abajo)
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

class TransportationProblemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Problema de Transporte")

        # Frame para entradas
        self.input_frame = ttk.Frame(master)
        self.input_frame.pack(padx=10, pady=10)

        ttk.Label(self.input_frame, text="Número de Proveedores:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.num_supply = tk.IntVar(value=4)
        ttk.Entry(self.input_frame, textvariable=self.num_supply, width=5).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(self.input_frame, text="Número de Consumidores:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.num_demand = tk.IntVar(value=4)
        ttk.Entry(self.input_frame, textvariable=self.num_demand, width=5).grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Button(self.input_frame, text="Crear Tabla", command=self.create_tables).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para botones de métodos (empaquetado único en la parte superior)
        self.methods_buttons_frame = ttk.Frame(master)
        self.methods_buttons_frame.pack(padx=10, pady=5)

        self.current_method = tk.StringVar(value="Esquina Noroeste")

        # Crear botones de métodos una sola vez
        self.btn_nw = ttk.Button(self.methods_buttons_frame, text="Esquina Noroeste", command=lambda: self.display_method("Esquina Noroeste"))
        self.btn_vogel = ttk.Button(self.methods_buttons_frame, text="Vogel", command=lambda: self.display_method("Vogel"))
        self.btn_min_cost = ttk.Button(self.methods_buttons_frame, text="Costo Mínimo", command=lambda: self.display_method("Costo Mínimo"))
        self.btn_seq_steps = ttk.Button(self.methods_buttons_frame, text="Pasos Secuenciales", command=lambda: self.display_method("Pasos Secuenciales"))
        self.btn_mod_dist = ttk.Button(self.methods_buttons_frame, text="Distribución Modificada", command=lambda: self.display_method("Distribución Modificada"))

        self.btn_nw.pack(side="left", padx=5)
        self.btn_vogel.pack(side="left", padx=5)
        self.btn_min_cost.pack(side="left", padx=5)
        self.btn_seq_steps.pack(side="left", padx=5)        # Nuevo botón
        self.btn_mod_dist.pack(side="left", padx=5)         # Nuevo botón

        # Frame para tablas
        self.tables_frame = ttk.Frame(master)
        self.tables_frame.pack(padx=10, pady=10, anchor='center')  # Centrar la tabla

        # Frame para resultados
        self.results_frame = ttk.Frame(master)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Inicializar variables para resultados
        self.methods_results = {}

    def create_tables(self):
        # Limpiar tablas anteriores
        for widget in self.tables_frame.winfo_children():
            widget.destroy()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.num_supply_val = self.num_supply.get()
        self.num_demand_val = self.num_demand.get()

        # Crear un contenedor para centrar la tabla
        table_container = ttk.Frame(self.tables_frame)
        table_container.pack()

        # Configurar el ancho mínimo de la columna 0 para mostrar "Demanda" completamente
        table_container.grid_columnconfigure(0, minsize=200)  # Incrementado a 200

        # Crear tabla de costos
        ttk.Label(table_container, text="Costos").grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.costs_entries = []
        for i in range(self.num_supply_val):
            row_entries = []
            for j in range(self.num_demand_val):
                e = ttk.Entry(table_container, width=10)  # Aumentar ancho para mejor visualización
                e.grid(row=i+1, column=j+1, padx=2, pady=2)
                row_entries.append(e)
            self.costs_entries.append(row_entries)

        # Crear entradas de oferta
        ttk.Label(table_container, text="Oferta").grid(row=0, column=self.num_demand_val + 1, padx=5, pady=5, sticky=tk.W)
        self.supply_entries = []
        for i in range(self.num_supply_val):
            e = ttk.Entry(table_container, width=10)
            e.grid(row=i+1, column=self.num_demand_val + 1, padx=2, pady=2)
            self.supply_entries.append(e)

        # Crear entradas de demanda
        ttk.Label(table_container, text="Demanda").grid(row=self.num_supply_val + 1, column=0, padx=5, pady=5, sticky=tk.W)
        self.demand_entries = []
        for j in range(self.num_demand_val):
            e = ttk.Entry(table_container, width=10)
            e.grid(row=self.num_supply_val + 1, column=j+1, padx=2, pady=2)
            self.demand_entries.append(e)

        # Botón para resolver
        ttk.Button(table_container, text="Resolver", command=self.solve).grid(row=self.num_supply_val + 2, column=0, columnspan=self.num_demand_val + 2, pady=10)

    def solve(self):
        try:
            # Obtener costos
            costs = []
            for row in self.costs_entries:
                cost_row = []
                for e in row:
                    val = float(e.get())
                    cost_row.append(val)
                costs.append(cost_row)
            # Obtener oferta
            supply = []
            for e in self.supply_entries:
                val = float(e.get())
                supply.append(val)
            # Obtener demanda
            demand = []
            for e in self.demand_entries:
                val = float(e.get())
                demand.append(val)
            # Verificar balance
            if sum(supply) != sum(demand):
                messagebox.showerror("Error", "La oferta y la demanda no están balanceadas.")
                return
            # Resolver métodos
            nc_alloc = northwest_corner_method(costs, supply.copy(), demand.copy())
            v_alloc = vogel_approximation_method(costs, supply.copy(), demand.copy())
            mc_alloc = minimum_cost_method(costs, supply.copy(), demand.copy())
            ss_alloc = sequential_steps_method(costs, supply.copy(), demand.copy())
            md_alloc = modified_distribution_method(costs, supply.copy(), demand.copy())

            # Calcular costos
            nc_cost = calculate_cost(nc_alloc, costs)
            v_cost = calculate_cost(v_alloc, costs)
            mc_cost = calculate_cost(mc_alloc, costs)
            ss_cost = calculate_cost(ss_alloc, costs)
            md_cost = calculate_cost(md_alloc, costs)

            # Guardar resultados
            self.methods_results = {
                "Esquina Noroeste": {
                    "alloc": nc_alloc,
                    "cost": nc_cost
                },
                "Vogel": {
                    "alloc": v_alloc,
                    "cost": v_cost
                },
                "Costo Mínimo": {
                    "alloc": mc_alloc,
                    "cost": mc_cost
                },
                "Pasos Secuenciales": {
                    "alloc": ss_alloc,
                    "cost": ss_cost
                },
                "Distribución Modificada": {
                    "alloc": md_alloc,
                    "cost": md_cost
                }
            }

            # Mostrar resultados del método Esquina Noroeste por defecto
            self.display_method("Esquina Noroeste")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

    def display_method(self, method_name):
        if not self.methods_results:
            messagebox.showerror("Error", "Por favor, resuelve el problema primero.")
            return

        self.current_method.set(method_name)

        # Limpiar resultados anteriores
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Crear ScrollableFrame
        scrollable_frame = ScrollableFrame(self.results_frame)
        scrollable_frame.pack(fill="both", expand=True)

        # Crear tabla comparativa de costos y rutas
        summary_frame = ttk.Frame(scrollable_frame.scrollable_frame)
        summary_frame.pack(padx=10, pady=10, anchor='w')

        cols_summary = ["Método", "Costo Total", "Rutas Utilizadas"]
        data_summary = [
            ["Esquina Noroeste", self.methods_results["Esquina Noroeste"]["cost"], len(self.methods_results["Esquina Noroeste"]["alloc"])],
            ["Vogel", self.methods_results["Vogel"]["cost"], len(self.methods_results["Vogel"]["alloc"])],
            ["Costo Mínimo", self.methods_results["Costo Mínimo"]["cost"], len(self.methods_results["Costo Mínimo"]["alloc"])],
            ["Pasos Secuenciales", self.methods_results["Pasos Secuenciales"]["cost"], len(self.methods_results["Pasos Secuenciales"]["alloc"])],
            ["Distribución Modificada", self.methods_results["Distribución Modificada"]["cost"], len(self.methods_results["Distribución Modificada"]["alloc"])]
        ]

        ttk.Label(summary_frame, text="Comparación de Métodos", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=3, pady=5)

        tree_summary = ttk.Treeview(summary_frame, columns=cols_summary, show='headings', height=5)
        for col in cols_summary:
            tree_summary.heading(col, text=col)
            tree_summary.column(col, anchor=tk.CENTER, width=150)
        for row in data_summary:
            tree_summary.insert('', tk.END, values=row)
        tree_summary.grid(row=1, column=0, columnspan=3, pady=5)

        # Crear marco para la matriz de costos con Demanda y Oferta
        cost_matrix_frame = ttk.LabelFrame(scrollable_frame.scrollable_frame, text="Matriz de Costos")
        cost_matrix_frame.pack(padx=10, pady=10, anchor='w')

        # Crear Treeview para mostrar la matriz de costos con Demanda y Oferta
        sources_labels = [index_to_letter(i) for i in range(self.num_supply_val)]
        destinations_labels = [index_to_letter(j) for j in range(self.num_demand_val)]  # Etiquetas corregidas

        cols = ["Oferta/Demanda"] + destinations_labels + ["Oferta"]
        tree_cost = ttk.Treeview(cost_matrix_frame, columns=cols, show='headings', height=10)

        for col in cols:
            tree_cost.heading(col, text=col)
            if col == "Oferta/Demanda":
                tree_cost.column(col, anchor=tk.W, width=200)  # Alineación a la izquierda y ancho aumentado
            elif col == "Oferta":
                tree_cost.column(col, anchor=tk.CENTER, width=120)  # Ancho aumentado
            else:
                tree_cost.column(col, anchor=tk.CENTER, width=80)
        tree_cost.pack(padx=5, pady=5, fill="x")  # Usar fill="x" para expandirse horizontalmente

        # Insertar filas con Oferta
        for i, row in enumerate([ [entry.get() for entry in row] for row in self.costs_entries]):
            tree_cost.insert('', tk.END, values=[sources_labels[i]] + row + [self.supply_entries[i].get()])

        # Insertar una fila para Demanda
        tree_cost.insert('', tk.END, values=["Demanda"] + [entry.get() for entry in self.demand_entries] + [""])

        # Crear marco para las asignaciones detalladas
        allocations_frame = ttk.Frame(scrollable_frame.scrollable_frame)
        allocations_frame.pack(padx=10, pady=10, anchor='w')

        # Crear sección para el método seleccionado
        method_section = ttk.LabelFrame(allocations_frame, text=method_name)
        method_section.pack(padx=10, pady=10, fill="x", expand=True)

        # Crear dos subframes dentro de cada método: uno para Asignaciones Detalladas y otro para Matriz de Costos
        detail_frame = ttk.Frame(method_section)
        detail_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        matrix_frame = ttk.Frame(method_section)
        matrix_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)

        # Asignaciones Detalladas
        frame_alloc = ttk.LabelFrame(detail_frame, text="Asignaciones Detalladas")
        frame_alloc.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        cols_alloc = ["Proveedor", "Consumidor", "Cantidad", "Costo Unitario", "Costo Total"]
        tree_alloc = ttk.Treeview(frame_alloc, columns=cols_alloc, show='headings', height=10)
        for col in cols_alloc:
            tree_alloc.heading(col, text=col)
            tree_alloc.column(col, anchor=tk.CENTER, width=120)  # Ancho aumentado
        tree_alloc.pack(padx=5, pady=5, fill="both", expand=True)

        sources_labels = [index_to_letter(i) for i in range(self.num_supply_val)]
        destinations_labels = [index_to_letter(j) for j in range(self.num_demand_val)]

        total_method_cost = 0
        for ((i, j), alloc_qty) in self.methods_results[method_name]["alloc"]:
            cost_unit = float(self.costs_entries[i][j].get())
            cost_total = alloc_qty * cost_unit
            total_method_cost += cost_total
            tree_alloc.insert('', tk.END, values=(sources_labels[i], destinations_labels[j], alloc_qty, cost_unit, cost_total))
        tree_alloc.pack(padx=5, pady=5, fill="both", expand=True)

        # Mostrar Costo Total
        ttk.Label(frame_alloc, text=f"Costo Total: {total_method_cost}").pack(pady=5)

        # Matriz de Costos
        frame_grid = ttk.LabelFrame(matrix_frame, text="Matriz de Costos")
        frame_grid.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        # Compute allocation cost matrix
        cost_matrix = [[0 for _ in range(self.num_demand_val)] for _ in range(self.num_supply_val)]
        for ((i, j), alloc_qty) in self.methods_results[method_name]["alloc"]:
            cost_matrix[i][j] = alloc_qty * float(self.costs_entries[i][j].get())
        # Compute row sums
        row_sums = [sum(row) for row in cost_matrix]

        # Crear Treeview para la tabla de asignaciones en formato de matriz
        tree_grid = ttk.Treeview(frame_grid, columns=['Proveedor'] + destinations_labels + ['Total'], show='headings', height=10)
        for col in ['Proveedor'] + destinations_labels + ['Total']:
            tree_grid.heading(col, text=col)
            if col == 'Proveedor':
                tree_grid.column(col, anchor=tk.CENTER, width=120)  # Ancho aumentado
            elif col == 'Total':
                tree_grid.column(col, anchor=tk.CENTER, width=120)  # Ancho aumentado
            else:
                tree_grid.column(col, anchor=tk.CENTER, width=80)
        tree_grid.pack(padx=5, pady=5, fill="both", expand=True)

        # Insertar filas
        for i in range(self.num_supply_val):
            row_values = [sources_labels[i]] + cost_matrix[i] + [row_sums[i]]
            tree_grid.insert('', tk.END, values=row_values)

    def demand_entries_vals(self, costs):
        # Esta función extrae los valores de demanda ingresados por el usuario
        # Se asume que la fila de demanda está después de las filas de oferta
        return [float(e.get()) for e in self.demand_entries]

def main():
    root = tk.Tk()
    app = TransportationProblemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
