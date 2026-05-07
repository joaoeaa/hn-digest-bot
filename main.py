import os
import sys

from src.fetcher import fetch_top_stories
from src.summarizer import summarize_story
from src.formatter import format_digest
from src.telegram import send_message

VARS_OBRIGATORIAS = ["ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]


def validar_env():
    """Verifica se todas as variáveis de ambiente necessárias estão definidas."""
    faltando = [v for v in VARS_OBRIGATORIAS if not os.environ.get(v)]
    if faltando:
        raise ValueError(f"Variáveis de ambiente ausentes: {', '.join(faltando)}")


def main():
    validar_env()

    print("[main] Buscando top 8 histórias do Hacker News...")
    stories = fetch_top_stories(n=8)
    print(f"[main] {len(stories)} histórias encontradas.")

    stories_with_summaries = []
    for i, story in enumerate(stories, start=1):
        print(f"[main] Resumindo {i}/{len(stories)}: {story['title']}")
        try:
            summary = summarize_story(story)
        except Exception as e:
            print(f"[main] Falha ao resumir história {i}, pulando. Erro: {e}")
            summary = "_Resumo indisponível._"
        stories_with_summaries.append({"story": story, "summary": summary})

    print("[main] Formatando digest...")
    digest = format_digest(stories_with_summaries)

    print("[main] Enviando para o Telegram...")
    send_message(digest)
    print("[main] Digest enviado com sucesso!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[main] Erro fatal: {e}")
        sys.exit(1)
