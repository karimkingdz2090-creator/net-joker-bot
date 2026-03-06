import telebot
import socket
import platform
import os
from datetime import datetime

TOKEN = os.environ.get("TOKEN", "")
bot = telebot.TeleBot(TOKEN)

def check_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

@bot.message_handler(commands=["start"])
def start(msg):
    text = "👋 أهلاً! أنا *Net Joker Bot* 🤖\n\n📡 /myip\n🌍 /internet\n🔓 /ports\n🔎 /lookup\n📋 /info"
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["myip"])
def myip(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "غير متاح"
    bot.send_message(msg.chat.id, f"📡 IP: `{ip}`", parse_mode="Markdown")

@bot.message_handler(commands=["internet"])
def internet(msg):
    servers = [("8.8.8.8", 53, "Google"), ("1.1.1.1", 53, "Cloudflare")]
    text = "🌍 *فحص الإنترنت:*\n\n"
    for h, p, n in servers:
        text += f"{'✅' if check_port(h,p) else '❌'} {n}\n"
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["ports"])
def ports(msg):
    parts = msg.text.split()
    host = parts[1] if len(parts) > 1 else "127.0.0.1"
    common = {80:"HTTP",443:"HTTPS",22:"SSH",21:"FTP",3306:"MySQL",8080:"HTTP-Alt"}
    open_ports = [f"✅ {p} ({s})" for p,s in common.items() if check_port(host,p)]
    text = f"🔓 *البورتات على {host}:*\n\n" + ("\n".join(open_ports) if open_ports else "🔒 لا يوجد")
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["lookup"])
def lookup(msg):
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "⚠️ مثال: `/lookup google.com`", parse_mode="Markdown")
        return
    try:
        ip = socket.gethostbyname(parts[1])
        bot.send_message(msg.chat.id, f"🔎 `{parts[1]}` ➜ `{ip}`", parse_mode="Markdown")
    except:
        bot.send_message(msg.chat.id, "❌ فشل التحليل")

@bot.message_handler(commands=["info"])
def info(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "غير متاح"
    text = f"📊 *تقرير الشبكة*\n\n🖥️ {platform.system()} {platform.release()}\n📡 IP: `{ip}`\n🌍 {'✅' if check_port('8.8.8.8',53) else '❌'} إنترنت"
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

print("🤖 البوت يعمل...")
