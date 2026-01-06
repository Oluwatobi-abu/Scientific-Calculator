import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class GraphPanel(tk.Frame):
    def __init__(self, master, engine):
        super().__init__(master)
        
        save_btn = tk.Button(self, text="Save PNG", command=self.save_png)
        save_btn.pack(pady=4)
        
        clear_btn = tk.Button(self, text="Clear Graph", command=self.clear)
        clear_btn.pack(pady=2)
        
        close_btn = tk.Button(self, text="Close Graph", command=self.destroy)
        close_btn.pack(pady=2)

        self.engine = engine

        control_frame = tk.Frame(self)
        control_frame.pack(fill="x")

        tk.Label(control_frame, text="x min").pack(side="left")
        self.xmin_entry = tk.Entry(control_frame, width=6)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.pack(side="left")

        tk.Label(control_frame, text="x max").pack(side="left")
        self.xmax_entry = tk.Entry(control_frame, width=6)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.pack(side="left")
        # domain defaults
        self.x_min = -10
        self.x_max = 10
        self.steps = 400

        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        
    def save_png(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Save graph as PNG"
        )

        if file_path:
            self.figure.savefig(file_path, dpi=150)

    def plot(self, expr):
        if "x" not in expr:
            return

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        try:
            x_min = float(self.xmin_entry.get())
            x_max = float(self.xmax_entry.get())
        except ValueError:
            x_min, x_max = -10, 10

        x_vals = np.linspace(x_min, x_max, self.steps)
        y_vals = []

        for x in x_vals:
            try:
                y = self.engine.evaluate(expr, x=x)
                y_vals.append(y)
            except Exception:
                y_vals.append(np.nan)

        self.ax.plot(x_vals, y_vals, label=expr)

        self.ax.relim()
        self.ax.autoscale_view()

        self.ax.set_title(expr)
        self.ax.grid(True)
        self.ax.legend()

        self.canvas.draw()
        
    def clear(self):
        self.ax.clear()
        self.ax.grid(True)
        self.canvas.draw()
