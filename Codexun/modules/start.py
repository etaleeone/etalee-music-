import asyncio
from pytz import timezone
from datetime import datetime
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from Codexun.utils.filters import command

from Codexun import BOT_NAME, BOT_USERNAME
from Codexun.config import BOT_USERNAME 
from Codexun.config import BOT_NAME
from Codexun.config import START_IMG

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def strt_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://t.me/{BOT_USERNAME}",
        caption=f"""**مرحبا {message.from_user.mention()}** 👋

انا ربــوت **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) يتـيـح لـك تـشـغيل الـموسـيقى والفـيديـو فـي مجـموعـات مـن خـلال محـادثـات الـفيديـو الجـديـدة في Telegram!

📜 ¦ اكتــشف جـميـع أوامـر الـروبـوت وكيـفية عـملها مـن خـلال الـنقر علـى زار »  📜 ¦ الـأوامــر

🔖  لمـعرفة كـيفية اسـتخـدام هـذا الـروبـوت ، يـرجى النـقر فـوق زار » 🕊︙دليـل الـاسـتخـدام""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖥 ¦ الأوامــر", callback_data="cbcmnds"),
                    InlineKeyboardButton(
                        "⚙️ ¦ الـسـورس", callback_data="cbabout")
                ],
                [
                    InlineKeyboardButton(
                        "🧨 ¦ دلـيل الاسـتخـدام", callback_data="cbguide")
                ],
                [
                    InlineKeyboardButton(
                        "🎯 ¦ اضـفـني لـي مـجمـوعـتك ¦ 🎯", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )

