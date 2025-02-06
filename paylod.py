import telebot
import random
import string
from datetime import datetime

# Telegram Bot Token aur Admin ID
BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Yahan apna Bot Token daalain
ADMIN_ID = YOUR_ADMIN_ID      # Yahan apni Admin ID daalain (integer form mein)

# Bot Object Create Karna
sahil_bot = telebot.TeleBot(BOT_TOKEN)

pending_payloads = {}

# String ko HEX Payload Me Convert Karne Ka Function
def string_to_payload(input_string):
    payload = ''.join(['\\x{:02x}'.format(ord(c)) for c in input_string])
    return payload

# Random HEX Payload Generate Karne Ka Function
def generate_hex_payload():
    payloads = []
    for _ in range(1024):  # 1024 Lines Generate Karega
        random_hex = ''.join(random.choices(string.hexdigits.upper(), k=16))  # 16-Character HEX
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current Time
        payloads.append(f"{timestamp} - {random_hex}")
    
    # File Me Save Karna
    file_path = "sahil.txt"
    with open(file_path, "w") as file:
        file.write("\n".join(payloads))

    return file_path

# `/convert` Command
@sahil_bot.message_handler(commands=['convert'])
def convert_message(message):
    if message.chat.id == ADMIN_ID:
        input_string = message.text[len('/convert '):]
        payload = string_to_payload(input_string)
        sahil_bot.send_message(ADMIN_ID, f"Payload: {payload}")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ Aap is command ko istemal karne ke liye authorized nahi hain.")

# `/generate` Command (1024 HEX Payloads)
@sahil_bot.message_handler(commands=['generate'])
def generate_file(message):
    if message.chat.id == ADMIN_ID:
        sahil_bot.send_message(ADMIN_ID, "🔄 HEX payload generate ho raha hai, please wait...")
        file_path = generate_hex_payload()
        with open(file_path, "rb") as file:
            sahil_bot.send_document(ADMIN_ID, file)  # Admin Ko File Send Karna
        sahil_bot.send_message(ADMIN_ID, "✅ `sahil.txt` file generate ho gayi!")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ Aap is command ko istemal karne ke liye authorized nahi hain.")

# `/echo` Command
@sahil_bot.message_handler(commands=['echo'])
def echo_message(message):
    sahil_bot.send_message(message.chat.id, message.text[len('/echo '):])

# `/time` Command
@sahil_bot.message_handler(commands=['time'])
def time_message(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sahil_bot.send_message(message.chat.id, f"🕒 Current Time: {current_time}")

# `/help` Command
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "🤖 *SahilBot Commands:*\n\n"
        "/convert <text> - String ko HEX payload mein convert kare.\n"
        "/generate - 1024 HEX payloads generate kare aur sahil.txt bheje.\n"
        "/echo <text> - Aapke message ko waapas bheje.\n"
        "/time - Current time dikhaye.\n"
        "/help - Commands ki list dikhaye."
    )
    sahil_bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# Bot Polling Start Karna
if __name__ == "__main__":
    sahil_bot.polling()
