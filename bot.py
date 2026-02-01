import feedparser
import requests
from datetime import datetime

TOKEN = 8536609104:AAG_AO7jftggNoVWnC5uayOR6upX4bkFeIQ
CHAT_ID = 1152311283

# Pares que você quer
PARES = ["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "AUD/USD", "USD/CAD"]

FEEDS = [
    "https://br.dailyforex.com/rss",
    "https://www.fxleaders.com/feed/",
    "https://www.moneymunch.com/feed/",
]

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def contem_par(texto):
    for par in PARES:
        if par.lower() in texto.lower():
            return True
    return False

def gerar_resumo():
    hoje = datetime.now().strftime("%d/%m/%Y")
    resumo = f"📊 *Forex Daily Tips — {hoje}*\n\n"

    for feed in FEEDS:
        f = feedparser.parse(feed)

        for entry in f.entries[:10]:
            titulo = entry.title
            link = entry.link

            if contem_par(titulo):
                resumo += f"• {titulo}\n{link}\n\n"

    return resumo

if __name__ == "__main__":
    mensagem = gerar_resumo()
    enviar_telegram(mensagem)
