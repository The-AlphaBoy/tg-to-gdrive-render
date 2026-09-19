import os
import sys
import asyncio
import threading
from pyrogram import Client, filters
import uvicorn
from fastapi import FastAPI

web_app = FastAPI()

@web_app.get("/")
def root():
    return {"status": "TG to GDrive Bot is running 24/7 on Render!"}

@web_app.get("/health")
def health():
    return {"status": "ok"}

API_ID = int(os.environ.get("API_ID", "26500583"))
API_HASH = os.environ.get("API_HASH", "fa2e022f47385f096b7979fa4bb607bb")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8813734676:AAF0aiSaWG1ANqYGF5z9OdA17H1K-m1G9pc")
FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "1vCQHoT87DiDVgY4re4VvuilDv9UNuZrN")

tg_app = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@tg_app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "سلام رفیق! ربات ۲۴ ساعته ابری روی سرور رندر آنلاین شد 🚀\n\nفایلت رو بفرست تا با سرعت بالا دانلود بشه."
    )

@tg_app.on_message(filters.media | filters.document)
async def handle_media(client, message):
    status_msg = await message.reply_text("⏳ در حال دریافت و دانلود فایل روی سرور ابری...")
    try:
        file_path = await message.download()
        file_name = os.path.basename(file_path)
        
        await status_msg.edit_text(
            f"✅ فایل با موفقیت دانلود و روی سرور ابری پردازش شد!\n\n📁 نام فایل: {file_name}"
        )
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await status_msg.edit_text(f"❌ خطا: {str(e)}")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(web_app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = threading.Thread(target=run_web, daemon=True)
    t.start()
    print("Starting Telegram Bot...")
    tg_app.run()
