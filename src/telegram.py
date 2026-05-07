import os
import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
# Limite de caracteres por mensagem do Telegram
MAX_CHARS = 4096


def send_message(text: str):
    """Envia mensagem para o canal/grupo configurado via Telegram Bot API."""
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = TELEGRAM_API.format(token=token)

    # Divide em partes caso o digest ultrapasse o limite do Telegram
    partes = _dividir_mensagem(text, MAX_CHARS)

    for parte in partes:
        payload = {
            "chat_id": chat_id,
            "text": parte,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"[telegram] Mensagem enviada ({len(parte)} chars)")
        except requests.RequestException as e:
            print(f"[telegram] Erro ao enviar mensagem: {e}")
            raise


def _dividir_mensagem(texto: str, limite: int) -> list:
    """Divide o texto em partes respeitando o limite de caracteres."""
    if len(texto) <= limite:
        return [texto]

    partes = []
    while texto:
        if len(texto) <= limite:
            partes.append(texto)
            break
        # Corta na última quebra de linha antes do limite
        corte = texto.rfind("\n", 0, limite)
        if corte == -1:
            corte = limite
        partes.append(texto[:corte])
        texto = texto[corte:].lstrip("\n")

    return partes
