import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análise de Tráfego - Dashboard")
        self.geometry("1000x700")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.create_tabs()

    def create_tabs(self):
        self.add_table_tab("IPG", "metricas/ipg.csv")
        self.add_table_tab("Pacotes por IP (Tamanho médio)", "metricas/packets_per_min.csv")
        self.add_table_tab("Burstness", "metricas/burstness.csv")
        self.add_image_tab("Distribuição por Janela", "metricas/windowed_packets.png")
        self.add_image_tab("CDF dos Pacotes", "metricas/cdf_packet_sizes.png")
        self.add_text_tab("Skewness & Kurtosis do IPG", "metricas/ipg_stats.txt")
        self.add_table_tab("Horizontal Scan (IPs suspeitos)", "metricas/suspicious_ips.csv")
        self.add_table_tab("Top 10 IPs Ativos", "metricas/top_10_ips.csv")
        self.add_table_tab("IPG médio e desvio padrão por IP", "metricas/ipg_stats_per_ip.csv")
        self.add_text_tab("Entropia dos IPs de origem", "metricas/src_entropy.txt")
        self.add_table_tab("Bytes por IP", "metricas/bytes_per_ip.csv")
        self.add_image_tab("Variação de tráfego (5s)", "metricas/packets_5s.png")
        self.add_table_tab("Relação Tamanho x Frequência", "metricas/packet_size_frequency.csv")
        self.add_text_tab("Padrões suspeitos", "metricas/suspicious_patterns.txt")

    def add_table_tab(self, title, filepath):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            text = ScrolledText(frame, wrap="none", font=("Courier", 10))
            text.insert("1.0", df.to_string(index=False))
            text.pack(fill="both", expand=True)
        else:
            ttk.Label(frame, text=f"Arquivo não encontrado: {filepath}").pack()

    def add_image_tab(self, title, image_path):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((900, 600), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            label = ttk.Label(frame, image=photo)
            label.image = photo
            label.pack()
        else:
            ttk.Label(frame, text=f"Imagem não encontrada: {image_path}").pack()

    def add_text_tab(self, title, txt_path):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                content = file.read()
            text_widget = ScrolledText(frame, wrap="word", font=("Courier", 11))
            text_widget.insert("1.0", content)
            text_widget.pack(fill="both", expand=True)
        else:
            ttk.Label(frame, text=f"Arquivo de texto não encontrado: {txt_path}").pack()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
