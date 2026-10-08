import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

COMMUNITY_URL = "https://t.me/nofmtrade"
HFM_URL = "https://www.hfmtrade-ind.com/sv/en/?refid=30587341"

WELCOME = """━━━━━━━━━━━━━━━━━━
        NOFM$TRADE
━━━━━━━━━━━━━━━━━━

Welcome to NOFM$TRADE 👋

Forex • XAUUSD • Education • Community

Trade smarter. Learn continuously. Manage your risk.

Pilih menu di bawah."""


def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Market", callback_data="market"),
            InlineKeyboardButton("📚 Education", callback_data="education"),
        ],
        [InlineKeyboardButton("💬 Community", url=COMMUNITY_URL)],
        [InlineKeyboardButton("🚀 Open Account", url=HFM_URL)],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("⚠️ Risk Warning", callback_data="risk"),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=main_menu())


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pages = {
        "market": (
            "📊 MARKET\n\n"
            "NOFM$TRADE menyediakan market insight dan materi edukasi "
            "seputar Forex & XAUUSD.\n\n"
            "Gunakan informasi sebagai bahan belajar, bukan jaminan hasil trading."
        ),
        "education": (
            "📚 EDUCATION\n\n"
            "Materi NOFM$TRADE mencakup:\n"
            "• Forex basics\n"
            "• XAUUSD\n"
            "• Risk management\n"
            "• Trading psychology\n"
            "• Market fundamentals\n\n"
            "Trade • Learn • Grow"
        ),
        "about": (
            "ℹ️ ABOUT NOFM$TRADE\n\n"
            "NOFM$TRADE adalah komunitas yang berfokus pada edukasi, "
            "market insight, dan risk management untuk trader.\n\n"
            "Forex • XAUUSD • Education • Community"
        ),
        "risk": (
            "⚠️ RISK WARNING\n\n"
            "Trading Forex/CFD dengan leverage memiliki risiko tinggi "
            "dan dapat menyebabkan kerugian yang signifikan.\n\n"
            "Pastikan memahami produk dan risikonya sebelum trading. "
            "Informasi di bot/channel ini bersifat edukasi dan bukan "
            "jaminan keuntungan atau nasihat investasi."
        ),
    }

    await query.edit_message_text(
        pages.get(query.data, WELCOME),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
        ])
    )


async def home_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(WELCOME, reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Gunakan /start untuk membuka menu NOFM$TRADE."
    )


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"NOFM$TRADE bot is running")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def build_app():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN belum diset sebagai environment variable.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(home_callback, pattern="^home$"))
    app.add_handler(CallbackQueryHandler(menu_callback))
    return app


if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    build_app().run_polling()
