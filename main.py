import customtkinter as ctk
from playwright.sync_api import sync_playwright
import threading, time, asyncio, os
from telegram import Bot

# Tenta importar o config, se não existir, cria variáveis vazias para não dar erro
try:
    import config
    TOKEN = config.TOKEN_TELEGRAM
    CHAT_ID = config.CHAT_ID
except:
    TOKEN = "SEU_TOKEN_AQUI"
    CHAT_ID = "SEU_ID_AQUI"

ctk.set_appearance_mode("dark")

class NeuralEmpirePro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEURAL EMPIRE ULTRA v4.0")
        self.geometry("1200x800")
        
        self.velas_historico = []
        self.auto_mode = False
        
        # Iniciar na tela de login
        self.tela_login()

    def tela_login(self):
        self.login_frame = ctk.CTkFrame(self, width=400, height=500, border_width=2, border_color="#00FF41")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_frame, text="SISTEMA NEURAL\nLOGIN RESTRITO", font=("Impact", 35), text_color="#00FF41").pack(pady=40)
        
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuário", width=280, height=45)
        self.user_entry.pack(pady=15)
        
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=280, height=45)
        self.pass_entry.pack(pady=15)
        
        btn = ctk.CTkButton(self.login_frame, text="ACESSAR TERMINAL", fg_color="#008F11", hover_color="#00FF41", height=55, font=("Roboto", 16, "bold"), command=self.verificar_login)
        btn.pack(pady=40)

    def verificar_login(self):
        if self.user_entry.get() == "lucas" and self.pass_entry.get() == "172830":
            self.login_frame.destroy()
            self.montar_painel()
        else:
            self.user_entry.configure(placeholder_text="DADOS INCORRETOS", placeholder_text_color="red")
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')

    def montar_painel(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#050505")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="CONTROLE", font=("Impact", 28), text_color="#00FF41").pack(pady=30)
        
        self.btn_nav = ctk.CTkButton(self.sidebar, text="🚀 ABRIR NAVEGADOR", height=50, command=self.abrir_navegador)
        self.btn_nav.pack(pady=15, padx=20, fill="x")

        self.btn_ia = ctk.CTkButton(self.sidebar, text="🧠 ATIVAR IA (SCANNER)", height=50, fg_color="#6c5ce7", command=self.ativar_ia)
        self.btn_ia.pack(pady=15, padx=20, fill="x")

        self.btn_auto = ctk.CTkButton(self.sidebar, text="🤖 MODO AUTOMÁTICO", height=50, fg_color="#d63031", command=self.toggle_auto)
        self.btn_auto.pack(pady=15, padx=20, fill="x")

        # Console Logs
        self.log_box = ctk.CTkTextbox(self, fg_color="#000", text_color="#00FF41", font=("Consolas", 14))
        self.log_box.pack(padx=20, pady=20, fill="both", expand=True)
        self.log("SISTEMA CARREGADO. Aguardando comando...")

    def log(self, msg):
        self.log_box.insert("end", f"\n[{time.strftime('%H:%M:%S')}] > {msg}")
        self.log_box.see("end")

    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        status = "ATIVADO" if self.auto_mode else "DESATIVADO"
        color = "green" if self.auto_mode else "red"
        self.log(f"Modo Automático {status}")
        self.btn_auto.configure(fg_color=color)

    def abrir_navegador(self):
        threading.Thread(target=self.run_browser, daemon=True).start()

    def run_browser(self):
        with sync_playwright() as p:
            # Pasta de cookies para o Google não bloquear
            user_data = os.path.expanduser("~/chrome_data_neural")
            self.context = p.chromium.launch_persistent_context(
                user_data_dir=user_data,
                headless=False,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            self.page = self.context.pages[0]
            self.page.goto("https://www.reidopitaco.com.br/casino/game/aviator")
            self.log("Navegador Aberto. Faça login no site se necessário.")
            while True: time.sleep(1)

    def ativar_ia(self):
        if not hasattr(self, 'page'):
            self.log("ERRO: Abra o navegador primeiro!")
            return
        self.log("IA Scanner Ativada. Lendo gráfico...")
        threading.Thread(target=self.scanner_loop, daemon=True).start()

    def scanner_loop(self):
        ultimo = ""
        while True:
            try:
                # Pega a vela mais recente (bolinha do topo)
                el = self.page.locator(".payouts-block .bubble-multiplier").first
                v_texto = el.inner_text(timeout=2000).replace('x','').strip()
                
                if v_texto != ultimo:
                    val = float(v_texto)
                    self.velas_historico.append(val)
                    self.log(f"Vela Detectada: {val}x")
                    self.processar_analise(val)
                    ultimo = v_texto
            except: pass
            time.sleep(1)

    def processar_analise(self, ultima_vela):
        if len(self.velas_historico) >= 3:
            ultimas_3 = self.velas_historico[-3:]
            # Se as 3 últimas forem menores que 1.80x (Gráfico "pagador" vindo)
            if all(v < 1.80 for v in ultimas_3):
                msg = "🚨 ALERTA: Padrão 3 Baixas detectado. Entrada Forte 2.0x!"
                self.log(msg)
                if self.auto_mode:
                    self.log("🤖 IA sugerindo entrada automática...")
                self.enviar_telegram(msg)

    def enviar_telegram(self, msg):
        async def send():
            try:
                bot = Bot(token=TOKEN)
                await bot.send_message(chat_id=CHAT_ID, text=msg)
            except: pass
        threading.Thread(target=lambda: asyncio.run(send()), daemon=True).start()

if __name__ == "__main__":
    app = NeuralEmpirePro()
    app.mainloop()
