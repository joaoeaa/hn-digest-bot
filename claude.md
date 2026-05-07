# HN Daily Digest Bot

Bot que roda todo dia às 8h (horário de Brasília), busca o top 8 do Hacker News, resume e traduz cada notícia com a Claude API, e envia para um canal/grupo no Telegram.

## Stack

- **Python 3.11+**
- **requests** — scraping da HN Algolia API e chamadas ao Telegram
- **anthropic** — SDK oficial para a Claude API
- **GitHub Actions** — agendamento via cron, zero servidor

## Estrutura de pastas esperada

```
hn-digest-bot/
├── CLAUDE.md
├── .github/
│   └── workflows/
│       └── daily_digest.yml
├── src/
│   ├── fetcher.py        # Busca top 8 do HN via Algolia API
│   ├── summarizer.py     # Chama Claude API para resumir + traduzir
│   ├── formatter.py      # Formata o digest em Markdown para o Telegram
│   └── telegram.py       # Envia a mensagem via Telegram Bot API
├── main.py               # Entrypoint: orquestra fetcher → summarizer → formatter → telegram
├── requirements.txt
└── README.md
```

## Secrets necessários (GitHub Actions → Settings → Secrets)

| Nome | Descrição |
|---|---|
| `ANTHROPIC_API_KEY` | Chave da Claude API |
| `TELEGRAM_BOT_TOKEN` | Token do bot criado pelo @BotFather |
| `TELEGRAM_CHAT_ID` | ID do canal ou grupo (ex: `-1001234567890`) |

## Convenções de código

- Funções simples, sem over-engineering — uma responsabilidade por módulo
- Validação de env vars no início do `main.py`, falha rápida e com mensagem clara
- Erros de API (HN, Claude, Telegram) devem ser capturados e logados — nunca silenciosos
- Sem classes desnecessárias — funções puras onde possível
- Comentários em português

## Modelo Claude

Usar sempre `claude-sonnet-4-20250514`. Max tokens: 1000 por notícia.

## Comportamento esperado do digest

- Buscar via `https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=8`
- Para cada notícia: título original + URL + pontuação + resumo em PT-BR (3-5 parágrafos, detalhado o suficiente para o leitor entender sem precisar abrir o link)
- Mensagem final no Telegram: cabeçalho com data, 8 blocos de notícia separados, rodapé com link para o HN
- Formato Telegram: usar `*bold*`, `_italic_` e links clicáveis — parse_mode `Markdown`

## Cron

Rodar todo dia às 11h UTC (= 8h de Brasília no horário de verão, ajustar conforme necessário).

## Como testar localmente

```bash
export ANTHROPIC_API_KEY=...
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python main.py
```