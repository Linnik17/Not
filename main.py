import asyncio
import os
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def build(text: str):
    text = text.strip()

    return f"""
🧠 bot is working

🔎 query: {text}

📱 Telegram: https://t.me/{text}
📸 Instagram: https://instagram.com/{text}
🎵 TikTok: https://tiktok.com/@{text}

🌐 Google:
https://www.google.com/search?q={text}
"""

@dp.message()
async def handler(message: types.Message):
    try:
        text = message.text or ""
        await message.answer(build(text))
    except:
        await message.answer("error")

async def main():
    print("bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
