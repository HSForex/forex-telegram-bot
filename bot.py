import feedparser
import requests
import os
from datetime import datetime

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

FEEDS = {
    "DailyForex": "https://br.dailyforex.com/rss",
    "FXEmpire": "https://www.fxempire.com/api/v1/en/articles/rss/news",
    "InstaForex": "https://www.instaforex.com/pt/forex_rss",
}

PAIRS = ["EUR/USD", "GBP/USD", "XAU/USD", "USD/JPY"]

def detectar_tendencia(texto):
    texto = texto.lower()
    if "buy" in texto or "compra" in texto or "bullish" in texto:
        return "Buy"
    if "sell" in texto or "venda" in texto or "bearish" in texto:
        return "Sell"
    return "Neutral"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def obter_dados():
    resultado = {pair: {} for pair in PAIRS}

    for nome, url in FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries[:20]:
            titulo = entry.title
            descricao = entry.get("description", "")

            for pair in PAIRS:
                if pair in titulo or pair in descricao:
                    tendencia = detectar_tendencia(titulo + " " + descricao)
                    resultado[pair][nome] = tendencia

    return resultado

def calcular_consenso(dados):
    mensagem = f"📊 *Resumo Diário Forex — {datetime.now().strftime('%d/%m/%Y')}*\n\n"

    for pair, fontes in dados.items():
        if not fontes:
            continue

        mensagem += f"*{pair}*\n"
        contagem = {"Buy": 0, "Sell": 0, "Neutral": 0}

        for fonte, tendencia in fontes.items():
            mensagem += f"- {fonte}: {tendencia}\n"
            contagem[tendencia] += 1

        consenso = max(contagem, key=contagem.get)
        mensagem += f"✅ Tendência geral: *{consenso}* ({contagem[consenso]}/{len(fontes)})\n\n"

    return mensagem

if __name__ == "__main__":
    dados = obter_dados()
    resumo = calcular_consenso(dados)
    enviar_telegram(resumo)