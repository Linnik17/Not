import asyncio
import os
import re
import aiohttp
import phonenumbers
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------------------
# DETECT TYPE
# ----------------------------

def is_email(text):
    return "@" in text and "." in text

def is_phone(text):
    try:
        phonenumbers.parse(text, None)
        return True
    except:
        return False

# ----------------------------
# USERNAME CHECK
# ----------------------------

SITES = {
    "Telegram": "https://t.me/{}",
    "GitHub": "https://github.com/{}",
    "Instagram": "https://instagram.com/{}",
    "TikTok": "https://tiktok.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}"
}

async def check_sites(username):
    async with aiohttp.ClientSession() as session:
        results = []

        for name, url in SITES.items():
            try:
                async with session.get(url.format(username), timeout=5) as r:
                    if r.status == 200:
                        results.append(f"✔ {name}: FOUND")
                    else:
                        results.append(f"✖ {name}: NOT FOUND")
            except:
                results.append(f"✖ {name}: ERROR")

        return results

# ----------------------------
# EMAIL MODULE
# ----------------------------

def email_report(email):
    return f"""
📧 OSINT EMAIL REPORT

Email: {email}

🌐 Google search:
https://www.google.com/search?q={email}

🔐 Breach check (manual):
https://haveibeenpwned.com/

Status: OPEN SOURCE ONLY
"""

# ----------------------------
# PHONE MODULE
# ----------------------------

def phone_report(phone):
    try:
        parsed = phonenumbers.parse(phone, None)
        country = phonenumbers.region_code_for_number(parsed)
        valid = phonenumbers.is_valid_number(parsed)

        return f"""
📞 PHONE OSINT REPORT

Number: {phone}

Country: {country}
Valid: {valid}

🌐 Google search:
https://www.google.com/search?q={phone}

Telegram/WhatsApp:
→ no direct access (open-source limitation)

Status: OPEN SOURCE ONLY
"""
    except:
        return "Invalid phone number"

# ----------------------------
# USERNAME REPORT
# ----------------------------

async def username_report(username):
    results = await check_sites(username)

    text = f"""
🧠 OSINT USERNAME REPORT

Username: {username}

"""

    text += "\n".join(results)
    return text

# ----------------------------
# ROUTER
# ----------------------------

async def process(text):
    text = text.strip()

    if is_email(text):
        return email_report(text)

    if is_phone(text):
        return phone_report(text)

    return await username_report(text)

# ----------------------------
# BOT HANDLER
# ----------------------------

@dp.message()
async def handler(message: types.Message):
    try:
        result = await process(message.text)
        await message.answer(result)
    except:
        await message.answer("⚠️ error processing request")

# ----------------------------
# START
# ----------------------------

async def main():
    print("OSINT BOT PRO STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
