import telebot
from transformers import pipeline

# ---- Твой новый Telegram-токен ----
TOKEN = "ВСТАВЬ_НОВЫЙ_ТОКЕН_ОТ_BOTFATHER"
bot = telebot.TeleBot(TOKEN)

# ---- Бесплатная ИИ-модель ----
chatbot = pipeline("text-generation", model="TheBloke/vicuna-7B-1.1-HF")

# ---- Команда /start ----
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! ✨\n"
        f"Я умный бот. Напиши /help чтобы узнать, что я умею."
    )

# ---- Команда /help ----
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
        "Вот что я умею:\n\n"
        "/ask <вопрос> — задать вопрос ИИ\n"
        "/calc <выражение> — калькулятор\n"
        "/raffle add <имя> — добавить участника\n"
        "/raffle run — провести розыгрыш\n"
    )

# ---- ИИ /ask ----
@bot.message_handler(commands=['ask'])
def ask_ai(message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        bot.send_message(message.chat.id, "Напиши вопрос после команды /ask")
        return
    bot.send_message(message.chat.id, "Думаю... 🤔")
    answer = chatbot(question, max_length=200)[0]["generated_text"]
    bot.send_message(message.chat.id, answer)

# ---- Калькулятор /calc ----
@bot.message_handler(commands=['calc'])
def calc(message):
    expr = message.text.replace("/calc", "").strip()
    try:
        result = eval(expr)
        bot.send_message(message.chat.id, f"Результат: {result}")
    except:
        bot.send_message(message.chat.id, "Ошибка. Пиши пример вида: 2+2*3")

# ---- Розыгрыш ----
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
        bot.send_message(message.chat.id, f"Участник добавлен: {name}")

    elif action == "run":
        if not raffle_list:
            bot.send_message(message.chat.id, "Список пуст ⛔")
            return
        import random
        winner = random.choice(raffle_list)
        bot.send_message(message.chat.id, f"🎉 ПОБЕДИТЕЛЬ: {winner} 🎉")
        raffle_list = []

# ---- Фолбэк: ответ на сообщения ----
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

# ---- Запуск ----
bot.polling()
