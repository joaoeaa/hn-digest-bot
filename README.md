# HN Daily Digest Bot

Bot que roda todo dia às 8h (horário de Brasília), busca o top 8 do Hacker News, resume e traduz cada notícia com a Claude API, e envia o digest para um canal ou grupo no Telegram.

## Pré-requisitos

- Python 3.11+
- Conta na [Anthropic](https://console.anthropic.com) com uma API key
- Um bot no Telegram com token válido
- Um canal ou grupo no Telegram onde o bot será admin

---

## 1. Criar o bot no Telegram

1. Abra o Telegram e inicie uma conversa com [@BotFather](https://t.me/BotFather)
2. Envie `/newbot` e siga as instruções (escolha nome e username)
3. Ao final, o BotFather entrega um **token** no formato `123456789:AAF...` — guarde-o

---

## 2. Obter o Chat ID

**Para um grupo:**
1. Adicione o bot ao grupo e torne-o administrador
2. Envie qualquer mensagem no grupo
3. Acesse `https://api.telegram.org/bot<TOKEN>/getUpdates` no navegador
4. Procure o campo `"chat": {"id": -1001234567890}` — o valor negativo é o chat_id

**Para um canal:**
1. Adicione o bot como administrador do canal
2. Poste uma mensagem no canal
3. Acesse o mesmo endpoint `getUpdates` acima e localize o `chat.id`

---

## 3. Configurar os secrets no GitHub

No repositório, vá em **Settings → Secrets and variables → Actions → New repository secret** e crie os três secrets:

| Nome | Valor |
|---|---|
| `ANTHROPIC_API_KEY` | Sua chave da Claude API |
| `TELEGRAM_BOT_TOKEN` | Token do bot (`123456789:AAF...`) |
| `TELEGRAM_CHAT_ID` | ID do canal/grupo (ex: `-1001234567890`) |

---

## 4. Testar localmente

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/hn-digest-bot.git
cd hn-digest-bot

# Instale as dependências
pip install -r requirements.txt

# Exporte as variáveis de ambiente
export ANTHROPIC_API_KEY="sua-chave-aqui"
export TELEGRAM_BOT_TOKEN="seu-token-aqui"
export TELEGRAM_CHAT_ID="seu-chat-id-aqui"

# Execute
python main.py
```

---

## 5. Primeiro disparo manual (importante)

O cron do GitHub Actions só roda nos horários agendados **e apenas depois que o workflow foi ativado ao menos uma vez**. Para garantir que tudo funciona sem esperar até às 11h UTC:

1. No GitHub, acesse a aba **Actions** do repositório
2. Na lista à esquerda, clique em **Daily HN Digest**
3. Clique em **Run workflow → Run workflow** (branch: main)
4. Acompanhe a execução em tempo real clicando no job gerado

Se tudo estiver certo, a mensagem aparecerá no Telegram em poucos minutos.

---

## Estrutura do projeto

```
hn-digest-bot/
├── .github/workflows/daily_digest.yml   # Agendamento via GitHub Actions
├── src/
│   ├── fetcher.py      # Busca top 8 do HN via Algolia API
│   ├── summarizer.py   # Resume e traduz via Claude API
│   ├── formatter.py    # Monta o Markdown para o Telegram
│   └── telegram.py     # Envia a mensagem via Telegram Bot API
├── main.py             # Entrypoint principal
├── requirements.txt
└── README.md
```
