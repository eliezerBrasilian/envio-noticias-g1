import asyncio
from bs4 import BeautifulSoup
import requests
import httpx
import json

TELEGRAM_TOKEN = "7646356506:AAH4ygxDAY1NFr6YRqTP6rukHlMz4Xr74J0"
CANAL_USERNAME = "@noticiasg1"

links_enviados = set()

def carrega_links_de_arquivo():
    global links_enviados  # Modifica a variável global
    try:
        with open("links_enviados.json", "r") as f:
            links_enviados = set(json.load(f))
    except FileNotFoundError:
        links_enviados = set()

def escreve_links_em_arquivo():
    global links_enviados  # Garante que estamos usando a variável global
    with open("links_enviados.json", "w") as f:
        json.dump(list(links_enviados), f)

async def enviar_mensagem(dados: dict):
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    url_message = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    print(url_photo)

    link = dados.get("link", "#")
    titulo = dados.get("titulo", "Sem título disponível")
    
    payload_photo = {
        "chat_id": CANAL_USERNAME,
        "caption": f"<b>{titulo}</b>",
        "photo": dados.get("imagem", "Sem imagem"),
        "parse_mode": "HTML"
    }

    payload_message = {
        "chat_id": CANAL_USERNAME,
        "text": f"Acesse a notícia completa aqui: {link}",
        "disable_web_page_preview": False
    }

    async with httpx.AsyncClient() as client:
        try:
            response_photo = await client.post(url_photo, json=payload_photo)
            print(response_photo.json())

            response_message = await client.post(url_message, json=payload_message)
            print(response_message.json())
        except Exception as e:
            print("Falha ao enviar notificação:", e)

# Carrega links previamente enviados
carrega_links_de_arquivo()

page = requests.get("https://g1.globo.com/")

if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")
    main_news = soup.find_all(class_="_evt")

    loop = asyncio.get_event_loop()
    
    for noticia in main_news:
        if noticia.find("img") is not None:
            link = noticia.find("a")["href"]
            
            if link not in links_enviados:
                dados = {
                    "imagem": noticia.find("img")["src"],
                    "titulo": noticia.find("a").text,
                    "link": link
                }
                print("Nova notícia encontrada:", dados["titulo"])
                links_enviados.add(link)
                loop.run_until_complete(enviar_mensagem(dados))
            else:
                print("Notícia já enviada:", noticia.find("a").text)
    
    escreve_links_em_arquivo()
else:
    print("Error:", page.status_code)