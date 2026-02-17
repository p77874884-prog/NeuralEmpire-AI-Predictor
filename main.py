import customtkinter as ctk
from playwright.sync_api import sync_playwright
import threading, time, asyncio, os
from telegram import Bot
import config

# Configurações de Design
ctk.set_appearance_mode("dark")

class NeuralEmpirePro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEURAL EMPIRE ULTRA v3.0")
        self.geometry("1100x700")
        
        self.velas_historico = []
        self.logado = False
        
        # Iniciar na tela de login
        self.tela_login()

    def tela_login(self):
        self.login_frame = ctk.CTkFrame(self, width=400, height=500)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_frame, text="SISTEMA NEURAL\nACESSO RESTRITO", font=("Impact", 25), text_color="#00FF41").pack(pady=30)
        
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuário", width=250)
        self.user_entry.pack(pady=10)
        
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=250)
        self.pass_entry.pack(pady=10)
        
        btn = ctk.CTkButton(self.login_frame, text="ENTRAR NO IMPÉRIO", fg_color="#1f538d", command=self.verificar_login)
        btn.pack(pady=30)

    def verificar_login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        
        if u == "lucas" and p == "172830":
            self.login_frame.destroy()
            self.montar_painel_controle()
        else:
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.user_entry.configure(placeholder_text="ACESSO NEGADO", placeholder_text_color="red")

    def montar_painel_controle(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color="#050505")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="OPERAÇÃO", font=("Impact", 20), text_color="#00FF41").pack(pady=20)
        
        self.btn_nav = ctk.CTkButton(self.sidebar, text="1. ABRIR AVIATOR", command=self.abrir_navegador)
        self.btn_nav.pack(pady=10, padx=20)

        self.btn_ia = ctk.CTkButton(self.sidebar, text="2. ATIVAR IA", fg_color="#6c5ce7", command=self.ativar_ia)
        self.btn_ia.pack(pady=10, padx=20)

        self.log_box = ctk.CTkTextbox(self, fg_color="#000", text_color="#00FF41", font=("Consolas", 12))
        self.log_box.pack(padx=20, pady=20, fill="both", expand=True)

    def log(self, msg):
        self.log_box.insert("end", f"\n[{time.strftime('%H:%M:%S')}] {msg}")
        self.log_box.see("end")

    def abrir_navegador(self):
        threading.Thread(target=self.loop_navegador, daemon=True).start()

    def loop_navegador(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            self.page = browser.new_page()
            self.page.goto("https://www.reidopitaco.com.br/casino/game/aviator")
            self.log("Navegador pronto. Faça login no site.")
            while True: time.sleep(1)

    def ativar_ia(self):
        self.log("IA Neural Ativada. Monitorando padrões...")
        threading.Thread(target=self.monitoramento_velas, daemon=True).start()

    def monitoramento_velas(self):
        ultimo = ""
        while True:
            try:
                # Seletor das velas do Aviator
                vela_atual = self.page.locator(".payouts-block .bubble-multiplier").first.inner_text().replace('x','')
                
                if vela_atual != ultimo:
                    val = float(vela_atual)
                    self.velas_historico.append(val)
                    self.log(f"Vela Coletada: {val}x")
                    self.analisar_tendencia()
                    ultimo = vela_atual
            except: pass
            time.sleep(2)

    def analisar_tendencia(self):
        if len(self.velas_historico) >= 3:
            ultimas_3 = self.velas_historico[-3:]
            # Estratégia: Se as últimas 3 forem baixas (< 2x), chance de alta aumenta
            if all(v < 2.0 for v in ultimas_3):
                self.log("🔥 ALERTA: Padrão de Recuperação detectado! Possível vela alta.")
                self.enviar_telegram("🚀 ALERTA NEURAL: Chance de Vela Alta (2x+) detectada!")
            elif any(v > 10.0 for v in ultimas_3):
                self.log("⚠️ CUIDADO: Vela Rosa recente. Gráfico pode esfriar.")

    def enviar_telegram(self, msg):
        try:
            bot = Bot(token=config.TOKEN_TELEGRAM)
            asyncio.run(bot.send_message(chat_id=config.CHAT_ID, text=msg))
        except: pass

if __name__ == "__main__":
    app = NeuralEmpirePro()
    app.mainloop()
