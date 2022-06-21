import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


from Codexun.tgcalls import calls, queues
from Codexun.tgcalls.youtube import download
from Codexun.tgcalls import convert as cconvert
from Codexun.tgcalls.calls import client as ASS_ACC
from Codexun.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)

from Codexun import BOT_NAME, BOT_USERNAME
from Codexun import app
import Codexun.tgcalls
from Codexun.tgcalls import youtube
from Codexun.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    START_IMG,
    SUPPORT,
    UPDATE,
    BOT_NAME,
    BOT_USERNAME,
)
from Codexun.utils.filters import command
from Codexun.utils.decorators import errors, sudo_users_only
from Codexun.utils.administrator import adminsOnly
from Codexun.utils.errors import DurationLimitError
from Codexun.utils.gets import get_url, get_file_name
from Codexun.modules.admins import member_permissions


def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc"),
        ],[
            InlineKeyboardButton(text="Manage", callback_data=f"cls"),
        ],
        
    ]
    return buttons


fifth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200% 🔊", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)

fourth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150% 🔊", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)

third_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100% 🔊", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)

second_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50% 🔊", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)

first_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20% 🔊", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)
highquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality ✅", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Close 🗑️", callback_data=f"cls"),
        ],
    ]
)
lowquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality ✅", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Close 🗑️", callback_data=f"cls"),
        ],
    ]
)
mediumquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Low Quality", callback_data="low"),],
         [   InlineKeyboardButton("Medium Quality ✅", callback_data="medium"),
            
        ],[   InlineKeyboardButton("High Quality", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="Close 🗑️", callback_data=f"cls"),
        ],
    ]
)

dbclean_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("Yes, Proceed !", callback_data="cleandb"),],
        [    InlineKeyboardButton("Nope, Cancel !", callback_data="cbmenu"),
            
        ],[
            InlineKeyboardButton(text="⬅️ Back", callback_data=f"cbmenu"),
        ],
    ]
)
menu_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],[
            InlineKeyboardButton(text="Volume", callback_data=f"fifth"),
             InlineKeyboardButton(text="Quality", callback_data=f"high"),
        ],[
            InlineKeyboardButton(text="CleanDB", callback_data=f"dbconfirm"),
             InlineKeyboardButton(text="About", callback_data=f"nonabout"),
        ],[
             InlineKeyboardButton(text="🗑️ Close Menu", callback_data=f"cls"),
        ],
    ]
)


@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
Only admin with manage voice chat permission can do this.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**Skip Button Used By** {rpk}
• No more songs in Queue
`Leaving Voice Chat..`
"""
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
            await CallbackQuery.answer("تخطي الدردشة الصوتية.!", show_alert=True)     

@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music_off(chat_id)
            await calls.pytgcalls.pause_stream(chat_id)
            await CallbackQuery.answer("تم إيقاف الموسيقى مؤقتًا بنجاح.", show_alert=True)
            
        else:
            await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية!!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية!", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "لا شيء يلعب في الدردشة الصوتية",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await calls.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Music resumed successfully.", show_alert=True)
            
    else:
        await CallbackQuery.answer(f"Nothing is playing.", show_alert=True)


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Music stream ended.", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"**• Music successfully stopped by {rpk}.**")
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)

@Client.on_callback_query(filters.regex("cleandb"))
async def cleandb(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "Only admin with manage voice chat permission can do this.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Db cleaned successfully!", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.edit_message_text(
        f"✅ __Erased queues successfully__\n│\n╰ Database cleaned by {rpk}",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("❎ ¦ الـغـاء", callback_data="cls")]])
        
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)


@Client.on_callback_query(filters.regex("cbcmnds"))
async def cbcmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**• 📮 ¦ قائمة الأوامر الأساسيه**

• /play (song name) 
- لتشغيل الموسيقى

• /pause 
- لإيقاف الموسيقى

• /resume 
- لاستئناف الموسيقى

• /skip 
- لتخطي الأغنية الحالية

• /search (song name) 
- للبحث عن الموسيقى

• /song 
- لتحميل الموسيقى
""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton(
                        "⚡ ¦ قـايمـه التشغيل", callback_data="cbstgs"),
                    InlineKeyboardButton(
                        "🦸‍♂️¦ أوامر الادمنيه", callback_data="cbowncmnds")
                ],
              [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbhome")]]
        ),
    )
@Client.on_callback_query(filters.regex("cbowncmnds"))
async def cbowncmnds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**أوامر المالك والمطورين 💡**

• /broadcast (massage)
- بث اذاعه من خلال البوت

• /gcast (massage) 
- بث اذاعه بالتثبيت من خلال البوت

• /restart 
- أعد تشغيل البوت من الخادم

• /exec
- نفذ أي كود

• /stats
- احصل على كل الإحصائيات

• /ping 
- الجهوزية بينغ

• /update
- تحديث البوت بأحدث إصدار

• /gban او /ungban
- نظام الحظر العالمي

• /leaveall 
ترك المساعد من جميع الدردشات
""",
        reply_markup=InlineKeyboardMarkup(
            [
              
              [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbcmnds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**About {BOT_NAME} Bot 💡**

**[{BOT_NAME}](https://t.me/{BOT_USERNAME})** برنامج Music Bot هو الروبوت المصمم بواسطة @MK_1B_PY لتشغيل موسيقى عالية الجودة وغير قابلة للكسر في الدردشة الصوتية الجماعية.

يساعدك هذا الروبوت على تشغيل الموسيقى والبحث عن الموسيقى من youtube وتنزيل الموسيقى من خادم youtube والعديد من الميزات الأخرى المتعلقة بميزة الدردشة الصوتية telegram..

**المـساعد :- @{ASSUSERNAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("🪄 ¦ الـدعـم", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("⚙️ ¦ الـسورس", url=f"https://t.me/MK_1B_PY")
                ],
            [InlineKeyboardButton("💭 ¦ لـي تنـصيـب بـوتـك مجـاني", url=f"https://t.me/MK_1B_PY/1124")],
            [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbstgs"))
async def cbstgs(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**🔍 ¦ حـول أزرار الـقـائمة**

بعد تشغيل أغنيتك ، ستظهر بعض أزرار القائمة لإدارة تشغيل الموسيقى على الدردشة الصوتية. وهم على النحو التالي :

• ▶️
- استـئنـاف المـوسيـقى
• ⏸
- وقـفـة الـموسـيقى
• ⏹  
- نهـايـة المـوسـيقى
• ⏭️
- تـخـطي المـوسـيقى

 يـمـكنك أيـضًا فتـح هذه القـائمة مـن خـلال الأمر /settings 

**يمكن للمسؤولين فقط استخدام هذه الأزرار 📍**""",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbcmnds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**اقرأ الدليل الأساسي بعناية 💡**

• قم أولاً بإضافة هذا الروبوت في مجموعتك

• تعيين مدير الروبوت

• امنح إذن المسؤول المطلو

• • اكتب /reload في مجموعتك

ابدأ الدردشة الصوتية لمجموعاتك

• الآن قم بتشغيل أغنيتك واستمتع!""",
        reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton("🤕 ¦ خطـأ شـائع", callback_data="cberror")],
              [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbhome")]]
        ),
    )


@Client.on_callback_query(filters.regex("cberror"))
async def cberror(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**معظم الأخطاء التي تواجهها 💡**

في الغالب ، سيكون هناك الخطأ الرئيسي حول مساعد الموسيقى. إذا كنت تواجه أي نوع من الأخطاء في مجموعتك ، فتأكد أولاً في تلك المرة من أن @{ASSUSERNAME} متاح في مجموعتك. إذا لم يكن كذلك ، قم بإضافته يدويًا وقبل ذلك تأكد أيضًا أنه غير محظور في الدردشة.المساعد: - @{ASSUSERNAME} \n\nشكرًا💞!""",
        reply_markup=InlineKeyboardMarkup(
            [
            [
                    InlineKeyboardButton("☢️ ¦ المـساعد", url=f"https://t.me/{ASSUSERNAME}")
                ],
              [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbguide")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**مرحبا [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})** 👋

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


@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "ليس لديك أذونات كافية للقيام بهذا الإجراء.",
            show_alert=True,
        )
    await query.message.delete()

@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسؤول مجهول !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("يمكن للمسؤولين فقط استخدام هذا ..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**⚙️ {BOT_NAME} Bot Settings**\n\n📮 Group : {query.message.chat.title}.\n📖 Grp ID : {query.message.chat.id}\n\n**Manage Your Groups Music System By Pressing Buttons Given Below 💡**",

              reply_markup=menu_keyboard
         )
    else:
        await query.answer("لا شيء يتدفق حاليا", show_alert=True)



@Client.on_callback_query(filters.regex("high"))
async def high(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بجودة عالية!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nاختر خيارك من المعطى أدناه لإدارة جودة الصوت",
        reply_markup=highquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية..", show_alert=True)


@Client.on_callback_query(filters.regex("low"))
async def low(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بجودة منخفضة!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nاختر خيارك من المعطى أدناه لإدارة جودة الصوت.",
        reply_markup=lowquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)

@Client.on_callback_query(filters.regex("medium"))
async def medium(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بجودة متوسطة!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nاختر خيارك من المعطى أدناه لإدارة جودة الصوت",
        reply_markup=mediumquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية..", show_alert=True)

@Client.on_callback_query(filters.regex("fifth"))
async def fifth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بحجم 200٪!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nإذا كنت تريد إدارة مستوى الصوت من خلال الأزرار ، فقم بتعيين مسؤول مساعد أولاً.",
        reply_markup=fifth_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يتدفق حاليا", show_alert=True)

@Client.on_callback_query(filters.regex("fourth"))
async def fourth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفق الآن حجم 150!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nإذا كنت تريد إدارة مستوى الصوت من خلال الأزرار ، فقم بتعيين مسؤول مساعد أولاً.",
        reply_markup=fourth_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)

@Client.on_callback_query(filters.regex("third"))
async def third(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بحجم 100٪!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nإذا كنت تريد إدارة مستوى الصوت من خلال الأزرار ، فقم بتعيين مسؤول مساعد أولاً.",
        reply_markup=third_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)


@Client.on_callback_query(filters.regex("second"))
async def second(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بحجم 50٪!!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nإذا كنت تريد إدارة مستوى الصوت من خلال الأزرار ، فقم بتعيين مسؤول مساعد أولاً.",
        reply_markup=second_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)


@Client.on_callback_query(filters.regex("first"))
async def first(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "يمكن فقط للمسؤول الذي لديه إذن إدارة الدردشة الصوتية القيام بذلك.",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("يتدفقون الآن بحجم 20٪!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**إدارة مستوى الصوت 🔊**\n\nإذا كنت تريد إدارة مستوى الصوت من خلال الأزرار ، فقم بتعيين مدير مساعد أولاً.",
        reply_markup=first_keyboard
    )
    else:
        await CallbackQuery.answer(f"لا شيء يلعب في الدردشة الصوتية.", show_alert=True)

@Client.on_callback_query(filters.regex("nonabout"))
async def nonabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**إليك بعض المعلومات الأساسية حول {BOT_NAME} ، من هنا يمكنك ببساطة الاتصال بنا والانضمام إلينا!**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("🪄 ¦ الـدعـم", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("⚙️ ¦ الـسورس", url=f"https://t.me/MK_1B_PY")
                ],
              [InlineKeyboardButton("↩️ ¦ رجــوع", callback_data="cbmenu")]]
        ),
    )


@Client.on_callback_query(filters.regex("dbconfirm"))
async def dbconfirm(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("Only admins cam use this..!", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**Confirmation ⚠️**\n\nAre you sure want to end stream in {query.message.chat.title} and clean all Queued songs in db ?**",

              reply_markup=dbclean_keyboard
         )
    else:
        await query.answer("لا شيء يتدفق حاليا", show_alert=True)

