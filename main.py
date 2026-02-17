import customtkinter as ctk
from playwright.sync_api import sync_playwright
import threading, time, asyncio, os
from telegram import Bot

# Configuração de Cores e Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeuralEmpirePro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEURAL EMPIRE ULTRA v5.0")
        self.geometry("1100x750")
        
        self.velas_historico = []
        self.auto_mode = False
        
        # Iniciar na tela de login
        self.tela_login()

    def tela_login(self):
        self.login_frame = ctk.CTkFrame(self, width=400, height=500, border_width=2, border_color="#00FF41")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_frame, text="NEURAL EMPIRE\nACESSO RESTRITO", font=("Impact", 32), text_color="#00FF41").pack(pady=40)
        
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuário", width=280, height=45)
        self.user_entry.pack(pady=15)
        
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=280, height=45)
        self.pass_entry.pack(pady=15)
        
        btn = ctk.CTkButton(self.login_frame, text="ACESSAR SISTEMA", fg_color="#008F11", hover_color="#00FF41", 
                            height=55, font=("Roboto", 16, "bold"), command=self.verificar_login)
        btn.pack(pady=40)

    def verificar_login(self):
        if self.user_entry.get() == "lucas" and self.pass_entry.get() == "172830":
            self.login_frame.destroy()
            self.montar_painel()
        else:
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.user_entry.configure(placeholder_text="ACESSO NEGADO", placeholder_text_color="red")

    def montar_painel(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#050505")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)
        
        ctk.CTkLabel(self.sidebar, text="MENU PRO", font=("Impact", 24), text_color="#00FF41").pack(pady=30)
        
        ctk.CTkButton(self.sidebar, text="🚀 ABRIR AVIATOR", height=50, command=self.abrir_navegador).pack(pady=15, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="🧠 ATIVAR IA SCANNER", height=50, fg_color="#6c5ce7", command=self.ativar_ia).pack(pady=15, padx=20, fill="x")
        
        self.btn_auto = ctk.CTkButton(self.sidebar, text="🤖 MODO AUTOMÁTICO", height=50, fg_color="#d63031", command=self.toggle_auto)
        self.btn_auto.pack(pady=15, padx=20, fill="x")

        # Console de Operações
        self.log_box = ctk.CTkTextbox(self, fg_color="#000", text_color="#00FF41", font=("Consolas", 14), border_width=1, border_color="#333")
        self.log_box.pack(padx=20, pady=20, fill="both", expand=True)
        self.log("SISTEMA ONLINE. Pronto para operar, Lucas.")

    def log(self, msg):
        self.log_box.insert("end", f"\n[{time.strftime('%H:%M:%S')}] > {msg}")
        self.log_box.see("end")

    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        status = "LIGADO" if self.auto_mode else "DESLIGADO"
        color = "#2ecc71" if self.auto_mode else "#d63031"
        self.log(f"Modo Automático: {status}")
        self.btn_auto.configure(fg_color=color)

    def abrir_navegador(self):
        threading.Thread(target=self.run_browser, daemon=True).start()

    def run_browser(self):
        with sync_playwright() as p:
            # Pasta para salvar login e não precisar logar toda hora
            user_data = os.path.expanduser("~/neural_browser_data")
            self.log("Iniciando Chromium Engine...")
            
            # CONFIGURAÇÃO PARA QUALQUER NAVEGADOR PADRÃO DO PLAYWRIGHT
            self.context = p.chromium.launch_persistent_context(
                user_data_dir=user_data,
                headless=False,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            
            self.page = self.context.pages[0]
            self.page.goto("https://www.reidopitaco.com.br/casino/game/aviator")
            self.log("Navegador pronto no Rei do Pitaco!")
            
            while True: time.sleep(1)

    def ativar_ia(self):
        if not hasattr(self, 'page'):
            self.log("ERRO: Clique em ABRIR AVIATOR primeiro!")
            return
        self.log("IA Scaneando o gráfico em tempo real...")
        threading.Thread(target=self.scanner_loop, daemon=True).start()

    def scanner_loop(self):
        ultimo = ""
        while True:
            try:
                # Localiza o seletor das velas do Aviator
                el = self.page.locator(".payouts-block .bubble-multiplier").first
                v_texto = el.inner_text(timeout=2000).replace('x','').strip()
                
                if v_texto != ultimo:
                    val = float(v_texto)
                    self.velas_historico.append(val)
                    self.log(f"Nova Vela: {val}x")
                    self.analisar_sinal(val)
                    ultimo = v_texto
            except: pass
