Support Bot
-

A ticket-processing system, which uses Telegram bot to receive support tickets and Django to store and process them.

How the system works:

1. Creating the ticket.
   1. The user logs into the bot and starts working.
   2. The user creates a ticket through the bot, specifying its name.
   3. The user creates a message in the ticket, describing their problem.
2. Processing the ticket.
   1. The administrator or moderator (hereinafter referred to as the user) logs into the ticket processing panel (currently in progress).
   2. The user receives active tickets.
   3. The user reads the active ticket.
   4. The user sends a message to the ticket.
   5. The ticket is then assigned to the user and is no longer considered active, as its status changes to "in progress."
3. Continuing to work with the ticket.
   1. The ticket creator (hereinafter referred to as the user) receives a message through the bot informing them of a new message.
   2. The user reads the message.
   3. The user replies to the message or closes the ticket if the issue is resolved.
   4. If a ticket is closed, it is assigned the corresponding status and becomes available for reading, but not editing.
   5. The bot user can view their own ticket history, as well as the message history for each ticket, at any time.

---

Used technologies:
- `Docker`
- `Django`
- `aiogram` and `aiogram-dialogs`
- `uv`
- `redis`
- `celery`

___
### Quick start

1. Clone the repository

```bash
git clone https://github.com/Arsterid/support-bot.git
cd support-bot
```

2. Create .env file in the root folder and fill it:

```env
DJANGO_SECRET_KEY=django-insecure-...  # your django secret key.
DJANGO_DEBUG=True  # set to False in prod
DJANGO_ALLOWED_HOSTS=backend,localhost  # 'backend' is required, 'localhost' is optional if you want to use Django admin.
PSQL_NAME=todo_list
PSQL_USER=user
PSQL_PASS=some_password
PSQL_PORT=5432
BOT_TOKEN=your_telegram_bot_token  # you can get telegram bot token from @BotFather bot in telegram
BASE_API_URL=http://backend:8000  # base django api url for bot. format: 'container_name:internal_port'
TELEGRAM_BOT_API_TOKEN=some_very_secure_token  # a token used by django to identify that request made by bot
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

#### You can generate `DJANGO_SECRET_KEY` with command bellow ( make sure Django is installed beforehand ):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Run docker-compose

```bash
docker-compose up --build 
```
