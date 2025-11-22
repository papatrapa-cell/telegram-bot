import telebot
import os
from openai import OpenAI

# === Токен Telegram ===
TOKEN = os.getenv("TOKEN")  # Подставится с Render
bot = telebot.TeleBot(TOKEN)

# === OpenAI Client (бесплатная модель: gpt-4o-mini) ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я умный бот. Напиши /help чтобы узнать, что я умею."
    )

# === Команда /help ===
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
        "Вот что я умею:\n\n"
        "/ask <вопрос> — задать вопрос ИИ\n"
        "/calc <выражение> — калькулятор\n"
        "/raffle add <имя> — добавить участника\n"
        "/raffle run — провести розыгрыш\n"
    )

# === ИИ /ask ===
@bot.message_handler(commands=['ask'])
def ask_ai(message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        bot.send_message(message.chat.id, "Напиши вопрос после команды /ask")
        return

    bot.send_message(message.chat.id, "Думаю... 🧠")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )

    answer = response.choices[0].message.content
    bot.send_message(message.chat.id, answer)

# === Калькулятор ===
@bot.message_handler(commands=['calc'])
def calc(message):
    expr = message.text.replace("/calc", "").strip()
    try:
        result = eval(expr)
        bot.send_message(message.chat.id, f"Результат: {result}")
    except:
        bot.send_message(message.chat.id, "Ошибка. Пиши пример: 2+2*3")

# === Розыгрыш ===
raffle_list = []

@bot.message_handler(commands=['raffle'])
def raffle(message):
    global raffle_list
    args = message.text.split()

    if len(args) < 2:
        bot.send_message(message.chat.id, "Используй:\n/raffle add <имя>\n/raffle run")
        return

    action = args[1]

    if action == "add":
        name = " ".join(args[2:])
        raffle_list.append(name)
        bot.send_message(message.chat.id, f"Добавлен: {name}")

    elif action == "run":
        if not raffle_list:
            bot.send_message(message.chat.id, "Список пуст ⛔")
            return
        import random
        winner = random.choice(raffle_list)
        bot.send_message(message.chat.id, f"🎉 Победитель: {winner} 🎉")
        raffle_list = []

# === Ответ на любые сообщения ===
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

# === Запуск ===
bot.polling()
