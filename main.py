import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

notificati = []

def invia_messaggio(testo):
    data = {"chat_id": CHAT_ID, "text": testo}
    requests.post(URL_TELEGRAM, data=data)

def controlla_novitá():
    url = "https://www.pokemon.com/it/notizie-pokemon"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articoli = soup.select("ul.news-articles li")

    for articolo in articoli:
        titolo = articolo.find("h5").get_text(strip=True)
        link = "https://www.pokemon.com" + articolo.find("a")["href"]

        parole_chiave = ["collezione", "uscita", "pokémon ex", "tcg", "bustine", "mazzo", "espansione"]
        if any(parola.lower() in titolo.lower() for parola in parole_chiave):
            if link not in notificati:
                notificati.append(link)
                invia_messaggio(f"🆕 Nuova uscita trovata!\n\n📌 {titolo}\n🔗 {link}")

controlla_novitá()
