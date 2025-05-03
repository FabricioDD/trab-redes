import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Minimal Tkinter")
        self.geometry("700x550")
        self._setup_ui()
        self._init_plot()

    def _setup_ui(self):
        # Frame para o gráfico
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.update_btn = ttk.Button(btn_frame, text="Atualizar Dados", command=self.update_plot)
        self.update_btn.pack(side="left")

        self.quit_btn = ttk.Button(btn_frame, text="Sair", command=self.destroy)
        self.quit_btn.pack(side="right")

    def _init_plot(self):
        # Dados iniciais
        self.x = np.linspace(0, 10, 100)
        self.y = np.sin(self.x)

        # Cria figura e eixo
        self.fig, self.ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        self.line, = self.ax.plot(self.x, self.y, lw=2)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Seno aleatório")

        # Insere no Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_plot(self):
        # Gera novos dados (exemplo)
        phase = np.random.rand() * 2 * np.pi
        self.line.set_ydata(np.sin(self.x + phase))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()