import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import pandas as pd
import os

DARK_BG = "#1e1e1e"
DARK_FG = "#ffffff"
DARK_ACCENT = "#333333"

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard de Métricas")
        self.geometry("1200x700")
        self.configure(bg=DARK_BG)

        self.style = ttk.Style(self)
        self._set_dark_theme()

        self.metrics = {
            "IPG": ("table", "metricas/ipg.csv"),
            "Pacotes por IP": ("table", "metricas/packets_per_min.csv"),
            "Burstness": ("table", "metricas/burstness.csv"),
            "Distribuição por Janela": ("image", "metricas/windowed_packets.png"),
            "CDF dos Pacotes": ("image", "metricas/cdf_packet_sizes.png"),
            "Skewness/Kurtosis IPG": ("text", "metricas/ipg_stats.txt"),
            "Horizontal Scan": ("table", "metricas/suspicious_ips.csv"),
            "Top 10 IPs": ("table", "metricas/top_10_ips.csv"),
            "IPG médio/desvio IP": ("table", "metricas/ipg_stats_per_ip.csv"),
            "Entropia IPs Origem": ("text", "metricas/src_entropy.txt"),
            "Bytes por IP": ("table", "metricas/bytes_per_ip.csv"),
            "Tráfego em 5s": ("image", "metricas/packets_5s.png"),
            "Tamanho x Frequência": ("table", "metricas/packet_size_frequency.csv"),
            "Padrões suspeitos": ("text", "metricas/suspicious_patterns.txt"),
        }

        self._build_layout()

    def _set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TFrame", background=DARK_BG)
        self.style.configure("TLabel", background=DARK_BG, foreground=DARK_FG)
        self.style.configure("TButton", background=DARK_ACCENT, foreground=DARK_FG)
        self.style.map("TButton",
                       background=[("active", "#444444")],
                       foreground=[("active", "#ffffff")])
        self.style.configure("TNotebook", background=DARK_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=DARK_ACCENT, foreground=DARK_FG)

    def _build_layout(self):
        self.sidebar = ttk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Botão expansível "Métricas"
        self.metrics_frame = ttk.Frame(self.sidebar)
        self.metrics_frame.pack(fill="x", pady=10)

        self.expand = tk.BooleanVar(value=False)
        self.metrics_btn = ttk.Button(self.metrics_frame, text="▶ Métricas", command=self.toggle_metrics)
        self.metrics_btn.pack(fill="x", padx=10)

        self.metric_buttons_frame = ttk.Frame(self.sidebar)
        self.metric_buttons_frame.pack(fill="x", padx=10)

    def toggle_metrics(self):
        if self.expand.get():
            self.expand.set(False)
            self.metrics_btn.config(text="▶ Métricas")
            for widget in self.metric_buttons_frame.winfo_children():
                widget.destroy()
        else:
            self.expand.set(True)
            self.metrics_btn.config(text="▼ Métricas")
            for name, (mtype, path) in self.metrics.items():
                btn = ttk.Button(self.metric_buttons_frame, text=name, command=lambda n=name: self.load_metric(n))
                btn.pack(fill="x", pady=1)

    def load_metric(self, metric_name):
        # Limpa conteúdo atual
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        mtype, path = self.metrics[metric_name]
        if not os.path.exists(path):
            ttk.Label(self.main_frame, text=f"Arquivo não encontrado: {path}").pack(pady=20)
            return

        if mtype == "table":
            df = pd.read_csv(path)
            text = ScrolledText(self.main_frame, wrap="none", font=("Courier", 10), bg=DARK_BG, fg=DARK_FG, insertbackground='white')
            text.insert("1.0", df.to_string(index=False))
            text.config(state="disabled")
            text.pack(fill="both", expand=True, padx=10, pady=10)
        elif mtype == "image":
            img = Image.open(path)
            img = img.resize((900, 600), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = ttk.Label(self.main_frame, image=photo)
            label.image = photo
            label.pack(pady=10)
        elif mtype == "text":
            with open(path, 'r') as file:
                content = file.read()
            text = ScrolledText(self.main_frame, wrap="word", font=("Courier", 11), bg=DARK_BG, fg=DARK_FG, insertbackground='white')
            text.insert("1.0", content)
            text.config(state="disabled")
            text.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
