import os
import anthropic

PROMPT_TEMPLATE = """Você é um assistente que resume notícias tecnológicas do Hacker News para um leitor brasileiro.

Notícia:
Título: {title}
URL: {url}
Pontuação: {score} pontos

Escreva um resumo em português brasileiro com 3 a 5 parágrafos. O resumo deve:
- Explicar o que é o assunto (contexto para quem não conhece)
- Descrever o que há de novo ou relevante nessa notícia
- Explicar por que isso importa para a comunidade de tecnologia
- Ser detalhado o suficiente para o leitor entender completamente sem precisar abrir o link

Responda APENAS com o resumo, sem introduções como "Aqui está o resumo" ou similares."""


def summarize_story(story: dict) -> str:
    """Chama a Claude API para resumir e traduzir uma notícia para PT-BR."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = PROMPT_TEMPLATE.format(
        title=story["title"],
        url=story["url"],
        score=story["score"],
    )

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except anthropic.APIError as e:
        print(f"[summarizer] Erro na Claude API para '{story['title']}': {e}")
        raise
