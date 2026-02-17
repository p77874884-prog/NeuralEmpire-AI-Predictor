import customtkinter as ctkk
from playwright.sync_api import sync_playwright
import threading, time, asyncio, os
from telegram import Bot
import config

# Configurações de Design Matrix
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeuralEmpirePro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEURAL EMPIRE ULTRA v3.0")
        self.geometry("1100x750")
        
        self.velas_historico = []
        self.logado = False
        self.browser_context = None
        
        # Iniciar na tela de login
        self.tela_login()

    def tela_login(self):
        self.login_frame = ctk.CTkFrame(self, width=400, height=500, border_width=2, border_color="#00FF41")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.login_frame, text="NEURAL EMPIRE\nACESSO RESTRITO", font=("Impact", 30), text_color="#00FF41").pack(pady=40)
        
        self.user_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Utilizador", width=280, height=40)
        self.user_entry.pack(pady=15)
        
        self.pass_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=280, height=40)
        self.pass_entry.pack(pady=15)
        
        btn = ctk.CTkButton(self.login_frame, text="ENTRAR NO IMPÉRIO", font=("Roboto", 16, "bold"), 
                            fg_color="#008F11", hover_color="#00FF41", height=50, command=self.verificar_login)
        btn.pack(pady=40)

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
        # Sidebar de Navegação
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color="#0a0a0a")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)
        
        ctk.CTkLabel(self.sidebar, text="CONTROLO IA", font=("Impact", 24), text_color="#00FF41").pack(pady=30)
        
        self.btn_nav = ctk.CTkButton(self.sidebar, text="1. ABRIR AVIATOR", height=45, fg_color="#1f538d", command=self.abrir_navegador)
        self.btn_nav.pack(pady=15, padx=20)

        self.btn_ia = ctk.CTkButton(self.sidebar, text="2. ATIVAR IA NEURAL", height=45, fg_color="#6c5ce7", command=self.ativar_ia)
        self.btn_ia.pack(pady=15, padx=20)

        # Consola de Logs (Efeito Hacker)
        self.log_box = ctk.CTkTextbox(self, fg_color="#000", text_color="#00FF41", font=("Consolas", 13), border_width=1, border_color="#333")
        self.log_box.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.log("SISTEMA ONLINE. Bem-vindo, Lucas.")

    def log(self, msg):
        self.log_box.insert("end", f"\n[{time.strftime('%H:%M:%S')}] >> {msg}")
        self.log_box.see("end")

    def abrir_navegador(self):
        self.log("A iniciar navegador Stealth (Modo Camaleão)...")
        threading.Thread(target=self.loop_navegador, daemon=True).start()

    def loop_navegador(self):
        with sync_playwright() as p:
            # Pasta onde ficarão guardados os cookies (para não pedir login sempre)
            user_data = os.path.expanduser("~/neural_empire_data")
            
            self.browser_context = p.chromium.launch_persistent_context(
                user_data_dir=user_data,
                headless=False,
                channel="chrome", # Força o uso do Chrome estável do Kali
                viewport={'width': 1280, 'height': 720},
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )
            
            self.page = self.browser_context.pages[0]
            # Injeta scripts para parecer um humano
            self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.page.goto("https://www.reidopitaco.com.br/casino/game/aviator")
            self.log("Site carregado. Faz o login manualmente se necessário.")
            
            while True: 
                time.sleep(1)

    def ativar_ia(self):
        if not hasattr(self, 'page'):
            self.log("ERRO: Abre o Aviator primeiro!")
            return
        self.log("IA MONITORIZANDO PADRÕES... Procurando Velas Rosas.")
        threading.Thread(target=self.monitoramento_velas, daemon=True).start()

    def monitoramento_velas(self):
        ultimo_valor = ""
        while True:
            try:
                # Localiza a última vela que apareceu no topo do gráfico
                vela_elemento = self.page.locator(".payouts-block .bubble-multiplier").first
                vela_texto = vela_elemento.inner_text(timeout=5000).replace('x', '').strip()
                
                if vela_texto != ultimo_valor:
                    val = float(vela_texto)
                    self.velas_historico.append(val)
                    
                    cor = "ROSA" if val >= 10 else "AZUL" if val < 2 else "ROXA"
                    self.log(f"Vela Detetada: {val}x ({cor})")
                    
                    self.analisar_estratégia()
                    ultimo_valor = vela_texto
            except Exception as e:
                pass
            time.sleep(1)

    def analisar_estratégia(self):
        if len(self.velas_historico) < 3: return
        
        ultimas = self.velas_historico[-3:]
        
        # ESTRATÉGIA 1: Recuperação (3 velas baixas = Entrada para 2.0x)
        if all(v < 1.8 for v in ultimas):
            msg = "🔥 SINAL NEURAL: Padrão de Recuperação! Entrada Sugerida (Busca 2.0x)"
            self.log(msg)
            self.enviar_telegram(msg)
            
        # ESTRATÉGIA 2: Alerta de Vela Rosa
        if ultimas[-1] > 10.0:
            self.log("💎 VELA ROSA DETETADA! O sistema vai aguardar o gráfico estabilizar.")

    def enviar_telegram(self, msg):
        async def send():
            try:
                bot = Bot(token=config.TOKEN_TELEGRAM)
                await bot.send_message(chat_id=config.CHAT_ID, text=msg)
            except: pass
        threading.Thread(target=lambda: asyncio.run(send()), daemon=True).start()

if __name__ == "__main__":
    app = NeuralEmpirePro()
    app.mainloop()
