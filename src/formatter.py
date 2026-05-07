from datetime import datetime, timezone, timedelta

FUSO_BRASILIA = timezone(timedelta(hours=-3))


def format_digest(stories_with_summaries: list) -> str:
    """Monta a mensagem final do digest em Markdown compatível com Telegram."""
    hoje = datetime.now(FUSO_BRASILIA).strftime("%d/%m/%Y")

    linhas = [
        f"*🗞 HN Daily Digest — {hoje}*",
        "_As 8 histórias mais votadas do Hacker News hoje_",
        "",
    ]

    for i, item in enumerate(stories_with_summaries, start=1):
        story = item["story"]
        summary = item["summary"]

        titulo = story["title"].replace("*", "\\*").replace("_", "\\_").replace("`", "\\`")
        url = story["url"]
        score = story["score"]

        linhas += [
            f"*{i}. [{titulo}]({url})*",
            f"_{score} pontos_",
            "",
            summary,
            "",
            "—" * 20,
            "",
        ]

    linhas += [
        "_Fonte: [Hacker News](https://news.ycombinator.com)_",
    ]

    return "\n".join(linhas)
