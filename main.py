kimport customtkinter as ctk
from playwright.sync_api import sync_playwright
import threading, time, asyncio, os
from telegram import Bot
import config

class NeuralEmpire(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEURAL EMPIRE - PROJETO LUCAS")
        self.geometry("1300x750")
        
        self.velas_historico = []
        
        # --- UI DO PAINEL ---
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#0a0a0a")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="NEURAL EMPIRE", font=("Impact", 32), text_color="#00FF41").pack(pady=20)
        
        self.btn_start = ctk.CTkButton(self.sidebar, text="🚀 INICIAR SCANNER", command=self.iniciar)
        self.btn_start.pack(pady=10, padx=20, fill="x")

        self.log_box = ctk.CTkTextbox(self.sidebar, height=450, fg_color="#000", text_color="#00FF41")
        self.log_box.pack(pady=20, padx=10, fill="both")

    def log(self, msg):
        self.log_box.insert("end", f"\n[{time.strftime('%H:%M:%S')}] {msg}")
        self.log_box.see("end")

    def iniciar(self):
        self.log("Buscando padrões na tela...")
        threading.Thread(target=self.core_engine, daemon=True).start()

    def core_engine(self):
        with sync_playwright() as p:
            # Abre o navegador igual você está na foto
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            self.page = context.new_page()
            self.page.goto("https://www.reidopitaco.com.br/casino/game/aviator")
            
            self.log("Aguardando você logar e entrar no jogo...")
            
            ultimo_valor = ""
            while True:
                try:
                    # Tenta ler o valor da última vela no histórico (as bolinhas lá no topo)
                    # Esse seletor pega o primeiro item da lista de resultados
                    elemento = self.page.locator(".payouts-block .bubble-multiplier").first
                    valor_atual = elemento.inner_text().strip()
                    
                    if valor_atual != ultimo_valor:
                        self.log(f"Vela Detectada: {valor_atual}")
                        ultimo_valor = valor_atual
                        
                        # Salva no arquivo de aprendizado
                        with open("logs/aprendizado.txt", "a") as f:
                            f.write(f"{valor_atual}\n")
                except:
                    pass
                time.sleep(2)

if __name__ == "__main__":
    if not os.path.exists("logs"): os.makedirs("logs")
    app = NeuralEmpire()
    app.mainloop()
