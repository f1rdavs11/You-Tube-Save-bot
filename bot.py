import os
import asyncio
import nest_asyncio  # 👈 Muammoni hal qilish uchun qo'shildi
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 🔧 nest_asyncio ni faollashtiramiz (asyncio muammolarini oldini oladi)
nest_asyncio.apply()

BOT_TOKEN = "7754968151:AAGbFTaU1isRNEY_2TKi0Ty5c2ehQQH-TEA"
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def download_video(url: str):
    ydl_opts = {
        'format': '18',  # MP4 360p
        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Salom! Menga YouTube link yuboring!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("🔄 Yuklanmoqda...")
        video_path = await download_video(url)
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)
    else:
        await update.message.reply_text("⚠️ YouTube havolasi kiriting!")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot ishlayapti...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())  # ⬅️ Asyncio xatolariga yechim
