#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telethon.sessions import StringSession
import asyncio, re, json, shutil
from kvsqlite.sync import Client as uu
from telethon.tl.types import KeyboardButtonUrl, KeyboardButton, ReplyInlineMarkup
from telethon import TelegramClient, events, functions, types, Button
from telethon.tl.types import DocumentAttributeFilename
import time, datetime, random 
from datetime import timedelta
from telethon.errors import (
    ApiIdInvalidError, PhoneNumberInvalidError, PhoneCodeInvalidError,
    PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError
)
from telethon.errors.rpcerrorlist import UserDeactivatedBanError
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import types
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, SessionRevokedError
import random
import asyncio
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError


if not os.path.isdir('database'):
    os.makedirs('database')

API_ID = "36737234"
API_HASH = "dff41278c9c51b006d33510a8d339dca"
BOT_TOKEN = "7580837195:AAEbQJBJ-3dp56Z_It3NTId7TQfux9T7eXc" #توكنك
ADMIN_ID = 1898106980

client = TelegramClient('AbuHamza', api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)
db = uu('database/FFJFF5.ss', 'bot')

required_channels = db.get("required_channels") or []
if not db.exists("required_channels"):
    db.set("required_channels", [])
if not db.exists("timer_settings"):
    db.set("timer_settings", {})
if not db.get("channels"):
    db.set("channels", [])
if not db.exists("users"):
    db.set("users", {})
if not db.exists("bad_guys"):
    db.set("bad_guys", [])
if not db.exists("force"):
    db.set("force", [])
if not db.exists("admins"):
    db.set("admins", [ADMIN_ID])
if not db.exists("bot_enabled"):
    db.set("bot_enabled", True)
if not db.exists("auto_reply"):
    db.set("auto_reply", {})

MESSAGES = {
    'ADMIN_MESSAGE': '''
**↯︙مرحبًا بك في لوحة التحكم .**
**↯︙يمكنك إدارة بوت النشر التلقائي من هنا .**
''',
    'USER_MESSAGE': '''
**مرحبًا بك في بوت نشر تلقائي مجاناً \n\n• البوت مجاني بالكامل ✅\n• اضف حسابك وعين كليشة النشر والوقت وانطلق لافضل نشر امن 100% على الحسابات**
''',
    'NO_ACCOUNTS': '❌ **لا يوجد حسابات في البوت**',
    'ACCOUNT_ADDED': '✅ **تم اضافة الحساب بنجاح**\n\n- اجمالي الحسابات : 1',
    'ACCOUNT_REPLACED': '✅ **تم استبدال الحساب القديم بالجديد بنجاح**',
    'MESSAGE_SET': '✅ **تم تعيين رسالة النشر بنجاح**',
    'INTERVAL_SET': '✅ **تم تعيين المدة بين النشرات بنجاح**',
    'AUTO_POST_STARTED': '✅ تم تفعيل النشر التلقائي في جميع المجموعات',
    'AUTO_POST_STOPPED': '❌ تم إيقاف النشر التلقائي',
    'NO_MESSAGE_SET': '❌ **لم تقم بتعيين رسالة النشر بعد**',
    'NO_INTERVAL_SET': '❌ **لم تقم بتعيين المدة بين النشرات بعد**',
    'BOT_DISABLED': '**عزيزي المستخدم \n\n⚠️ البوت تحت الصيانة الان ، سوف يعود للعمل في الساعات القادمه \n• تابع قناة التحديثات : @EgyCodes1**',
    'BOT_DISABLEDs': '⛔ تم تعطيل البوت بنجاح \n\n• اي مستخدم سوف يراسل البوت سيتم اعلامه ان البوت في وضع الصيانه',
    'BOT_ENABLED': '✅ **تم تفعيل البوت**',
    'STATS_MESSAGE': '**إحصائيات البوت:**\n\n👥 إجمالي المستخدمين: {}\n📱 إجمالي الحسابات: {}',
    'BROADCAST_STARTED': '✅ بدأ إرسال الرسالة لجميع المستخدمين',
    'BROADCAST_COMPLETED': '✅ **تم إرسال الرسالة لجميع المستخدمين بنجاح**\n\n- عدد المستخدمين: {}\n- عدد الحسابات التي نجحت: {}\n- عدد الحسابات التي فشلت: {}',
    'MASS_POST_STARTED': '✅ **بدأ النشر الجماعي في جميع المجموعات**',
    'MASS_POST_COMPLETED': '✅ **تم النشر الجماعي بنجاح**\n\n- عدد الحسابات: {}\n- عدد المجموعات: {}\n- عدد النشرات الناجحة: {}\n- عدد النشرات الفاشلة: {}',
    'CHANNEL_REQUIRED': '⚠️ **يجب عليك الانضمام إلى قناتنا أولاً** @{}',
    'MESSAGE_REPLACED': '✅ تم تحديث كليشة النشر بنجاح',
    'NO_PREVIOUS_MESSAGE': '✅ تم تعيين كليشة النشر التلقائي بنجاح'
}

NUMBER_STYLES = {
    "Bold": ["𝟏", "𝟐", "𝟑", "𝟒", "𝟓", "𝟔", "𝟕", "𝟖", "𝟗", "𝟎"],
    "Bold Sans": ["𝟭", "𝟮", "𝟯", "𝟰", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵", "𝟬"],
    "Circled": ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⓪"],
    "Numbered": ["❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "⓿"],
    "Circled 11-20": ["⓫", "⓬", "⓭", "⓮", "⓯", "⓰", "⓱", "⓲", "⓳", "⓴"],
    "Monospace": ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟼", "𝟽", "𝟾", "𝟿"],
    "Double-Struck": ["𝟘", "𝟙", "𝟚", "𝟛", "𝟜", "𝟝", "𝟞", "𝟟", "𝟠", "𝟡"],
    "Sans-Serif": ["𝟬", "𝟭", "𝟮", "𝟯", "𝟰", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵"],
    "Arabic-Indic": ["𝟎", "𝟏", "𝟐", "𝟑", "𝟒", "𝟓", "𝟔", "𝟕", "𝟖", "𝟗"],
    "Fullwidth": ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"],
    "Arabic": ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"],
    "Math Bold": ["𝟢", "𝟣", "𝟤", "𝟥", "𝟦", "𝟧", "𝟨", "𝟩", "𝟪", "𝟫"]
}

def convert_time_to_style(time_str, style_name):
    """تحويل الوقت إلى النمط المطلوب"""
    if style_name not in NUMBER_STYLES:
        return time_str
    
    style = NUMBER_STYLES[style_name]
    result = ""
    
    for char in time_str:
        if char.isdigit():
            result += style[int(char)]
        else:
            result += char
    
    return result

def get_iraq_time():
    iraq_tz = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(iraq_tz)
    
    time_12h = now.strftime("%I:%M %p")
    
    time_12h = time_12h.replace("AM", "AM").replace("PM", "PM")
    
    return time_12h

def convert_time_to_style(time_str, style_name):
    if style_name not in NUMBER_STYLES:
        return time_str
    
    style = NUMBER_STYLES[style_name]
    result = ""
    
    for char in time_str:
        if char.isdigit():
            result += style[int(char)]
        else:
            result += char
    
    return result

async def is_user_member(user_id):
    try:
        required_channels = db.get("required_channels") or []
        
        if not required_channels:
            return True
        
        for channel in required_channels:
            try:
                channel_entity = await client.get_entity(f"t.me/{channel}")
                
                bot_id = (await client.get_me()).id
                admins = await client.get_participants(channel_entity, filter=types.ChannelParticipantsAdmins)
                is_bot_admin = any(admin.id == bot_id for admin in admins)
                
                if not is_bot_admin:
                    print(f"⚠️ البوت ليس مشرفاً في القناة: {channel}")
                    continue
                    
                try:
                    await client(GetParticipantRequest(
                        channel=channel_entity,
                        participant=user_id
                    ))
                except UserNotParticipantError:
                    return False
                except ValueError:
                    return False
                    
            except Exception as e:
                print(f"❌ خطأ في التحقق من القناة {channel}: {e}")
                continue
        
        return True
            
    except Exception as e:
        print(f"❌ خطأ عام في التحقق من اشتراك القنوات: {e}")
        return False

async def send_admin_controls():
    users = db.get("users") if db.exists("users") else {}
    total_users = len(users)
    total_accounts = sum(len(user.get("accounts", [])) for user in users.values())
    
    buttons = [
        [
            Button.inline("تعطيل البوت", data="disable_bot"),
            Button.inline("تفعيل البوت", data="enable_bot")
        ],
        [
            Button.inline("قسم الاشتراك التلقائي", data="xhhdhshs")
        ],
        [
            Button.inline("قسم الاشتراك الاجباري", data="manage_required_channels")
        ],
        [
            Button.inline("الاحصائيات", data="user_stats"),
            Button.inline("إذاعة", data="broadcast_users")
        ],
        [
            Button.inline("المستخدمين", data="total_users")
        ],
        [
            Button.inline("فحص الحسابات", data="check_all_accounts")
        ],
        [
            Button.inline("نشر بكل الحسابات", data="mass_post_groups")
        ]
    ]
    
    message = MESSAGES['ADMIN_MESSAGE'] + f"\n\n**حالة البوت:** {'✅ مفعل' if db.get('bot_enabled') else '❌ معطل'}"
    await client.send_message(ADMIN_ID, message, buttons=buttons)

@client.on(events.NewMessage(pattern="/start", func=lambda x: x.is_private))
async def start(event):
    if db.exists("bot_enabled"):
        if not db.get("bot_enabled"):
            return await event.respond(MESSAGES['BOT_DISABLED'])
    else:
        db.set("bot_enabled", True)
    
    user_id = event.chat_id
    
    if not await is_user_member(user_id):
        required_channels = db.get("required_channels") or []
        if required_channels:
            channels_list = "\n".join([f"• @{channel}" for channel in required_channels])
            return await event.respond(
                f"⚠️ **يجب الاشتراك في القنوات التالية أولاً:**\n\n{channels_list}\n\n"
                "✅ **بعد الاشتراك اضغط /start مرة أخرى**",
                buttons=[
                    [Button.inline("🔄 تحقق من الاشتراك", data="check_subscription")]
                ]
            )
    
    users = db.get("users") if db.exists("users") else {}
    user_accounts = users.get(str(user_id), {}).get("accounts", [])
    auto_reply = db.get("auto_reply") or {}
    user_auto_reply = auto_reply.get(str(user_id), {})
    
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    timer_enabled = user_timer.get("enabled", False)
    timer_font = user_timer.get("font", "Arial")
    
    buttons = [
        [
            Button.inline(f"الحساب : {'✅' if user_accounts else '❌'}", data="account_status"),
            Button.inline(f"الرد التلقائي : {'✅' if user_auto_reply.get('enabled', False) else '❌'}", data="account_status")
        ],
        [
            Button.inline("إضافة حساب", data="add_account"),
            Button.inline("حذف الحساب", data="delete_account")
        ],
        [
            Button.inline("الانضمام لمجموعة/قناة", data="join_group"),
        ],
        [
            Button.inline("تعيين الكليشة", data="set_post_msg"),
            Button.inline("تعيين الفاصل", data="set_post_interval")
        ],
        [
            Button.inline("تفعيل النشر", data="start_auto_post"),
            Button.inline("إيقاف النشر", data="stop_auto_post")
        ],
        [
            Button.inline("تفعيل الرد التلقائي", data="enable_auto_reply"),
            Button.inline("تعطيل الرد التلقائي", data="disable_auto_reply")
        ],
        [
            Button.inline("تعيين رسالة الرد التلقائي", data="set_auto_reply_msg")
        ],
        [
            Button.inline("قسم المؤقت", data="timer_section")
        ]
    ]
    
    if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
        await send_admin_controls()
    
    await event.reply(MESSAGES['USER_MESSAGE'], buttons=buttons)

async def monitor_account(account_session, user_id, phone_number):
    account_client = None
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            account_client = TelegramClient(
                StringSession(account_session),
                API_ID,
                API_HASH,
                connection_retries=5,
                retry_delay=3,
                timeout=30,
                device_model="Samsung Galaxy S21",
                system_version="Android 12",
                app_version="8.9.0"
            )
            
            await account_client.connect()
            
            if not await account_client.is_user_authorized():
                print(f"❌ الجلسة غير مصرحة للحساب {phone_number}")
                break

            @account_client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
            async def handle_incoming_msg(event):
                try:
                    if event.sender_id == ADMIN_ID or event.sender_id in (db.get("admins") if db.exists("admins") else []):
                        return

                    auto_reply = db.get("auto_reply") or {}
                    user_settings = auto_reply.get(str(user_id), {})
                    
                    if (user_settings.get("enabled", False) and 
                        user_settings.get("active_accounts", {}).get(phone_number, False)):
                        try:
                            await event.reply(user_settings.get("message", "بوت نشر تلقائي مجاني ~» @N3N9bot"))
                        except FloodWaitError as e:
                            print(f"⏱ يجب الانتظار {e.seconds} ثانية")
                            await asyncio.sleep(e.seconds)
                            await event.reply(user_settings.get("message", "بوت نشر تلقائي مجاني ~» @N3N9bot"))
                        except Exception as e:
                            print(f"❌ خطأ في الرد: {str(e)}")

                except Exception as e:
                    print(f"❌ خطأ في معالجة الرسالة: {str(e)}")

            # حلقة المراقبة مع فحص دوري
            check_interval = 0
            while True:
                await asyncio.sleep(5)
                check_interval += 5
                
                # فحص كل 30 ثانية
                if check_interval >= 30:
                    auto_reply = db.get("auto_reply") or {}
                    user_settings = auto_reply.get(str(user_id), {})
                    
                    if not user_settings.get("enabled", False) or not user_settings.get("active_accounts", {}).get(phone_number, False):
                        print(f"⏹ إيقاف مراقبة الحساب {phone_number}")
                        break
                    
                    # التحقق من صلاحية الجلسة
                    if not account_client.is_connected():
                        print(f"⚠️ انقطع الاتصال للحساب {phone_number}، إعادة الاتصال...")
                        raise ConnectionError("Connection lost")
                    
                    check_interval = 0
            
            break  # خروج ناجح من الحلقة

        except (ConnectionError, TimeoutError, OSError) as e:
            retry_count += 1
            print(f"⚠️ خطأ في الاتصال للحساب {phone_number} (محاولة {retry_count}/{max_retries}): {str(e)}")
            if retry_count < max_retries:
                await asyncio.sleep(10 * retry_count)  # انتظار متزايد
            else:
                print(f"❌ فشل الاتصال بعد {max_retries} محاولات")
        except SessionRevokedError:
            print(f"🔒 تم إلغاء الجلسة للحساب {phone_number}")
            break
        except Exception as e:
            print(f"❌ خطأ غير متوقع: {str(e)}")
            break
        finally:
            if account_client and account_client.is_connected():
                try:
                    await account_client.disconnect()
                    print(f"✅ تم قطع الاتصال بنجاح للحساب {phone_number}")
                except:
                    pass

async def stop_all_auto_posts(user_id):
    users = db.get("users") if db.exists("users") else {}
    user_data = users.get(str(user_id), {})
    user_data["auto_post_enabled"] = False
    user_data["auto_post_task"] = False
    users[str(user_id)] = user_data
    db.set("users", users)

async def auto_post(user_id):
    users = db.get("users") or {}
    user_data = users.get(str(user_id), {})
    
    if not user_data.get("accounts"):
        await client.send_message(user_id, "❌ لا يوجد حساب مسجل للنشر التلقائي")
        return
        
    account = user_data["accounts"][0]
    post_message = user_data.get("post_message")
    post_interval = max(user_data.get("post_interval", 100), 200)
    
    if not post_message:
        await client.send_message(user_id, "❌ لم تقم بتعيين رسالة النشر بعد")
        return

    GROUP_COOLDOWN = random.uniform(100, 120) 
    DAILY_LIMIT = 1200
    HOURLY_LIMIT = 50
    
    post_count = 0
    last_post_time = time.time()
    posted_groups = {}
    last_reset_time = time.time()

    while users.get(str(user_id), {}).get("auto_post_enabled", False):
        current_time = time.time()
        if current_time - last_reset_time >= 86400:
            post_count = 0
            last_reset_time = current_time
            posted_groups = {}
            await client.send_message(user_id, "🔄 تم إعادة تعيين الحد اليومي، بدء النشر من جديد")
        
        if post_count >= DAILY_LIMIT:
            remaining_time = 86400 - (current_time - last_reset_time)
            if remaining_time > 0:
                wait_hours = round(remaining_time / 3600, 1)
                await client.send_message(
                    user_id,
                    f"⏳ تم الوصول للحد اليومي للنشر ({DAILY_LIMIT})، "
                    f"جاري الانتظار {wait_hours} ساعة حتى اليوم التالي وسوف استكمل النشر تلقائي..."
                )
                await asyncio.sleep(remaining_time)
                continue
        
        temp_client = None
        try:
            temp_client = TelegramClient(
                StringSession(account["session"]), 
                API_ID, 
                API_HASH,
                connection_retries=5,
                retry_delay=3,
                timeout=30,
                device_model="Samsung Galaxy S21",
                system_version="Android 12",
                app_version="8.9.0",
                lang_code="ar",
                system_lang_code="ar-AR"
            )
            
            await temp_client.connect()
            
            if not await temp_client.is_user_authorized():
                await handle_session_revoked(user_id)
                break

            dialogs = await temp_client.get_dialogs(limit=200)
            groups = [
                dialog for dialog in dialogs 
                if dialog.is_group and not getattr(dialog.entity, 'broadcast', False)
            ]
            
            random.shuffle(groups)
            
            for group in groups:
                if not users.get(str(user_id), {}).get("auto_post_enabled", False):
                    break
                    
                group_id = str(group.entity.id)
                
                if group_id in posted_groups:
                    elapsed = time.time() - posted_groups[group_id]
                    if elapsed < GROUP_COOLDOWN:
                        continue 
                
                try:
                    await temp_client.send_message(
                        group.entity,
                        post_message,
                        link_preview=False,
                        silent=True
                    )
                    
                    post_count += 1
                    last_post_time = time.time()
                    posted_groups[group_id] = last_post_time
                    
                    inter_group_delay = random.uniform(10, 20)
                    await asyncio.sleep(inter_group_delay)
                    
                    if post_count >= DAILY_LIMIT:
                        await client.send_message(
                            user_id,
                            f"⚠️ تم الوصول للحد اليومي للنشر ({DAILY_LIMIT})، "
                            "جاري الانتظار حتى اليوم التالي..."
                        )
                        break
                        
                except FloodWaitError as e:
                    wait_time = max(e.seconds, 300)
                    await client.send_message(user_id, f"⏱ تم اكتشاف قيود تليجرام، انتظر {wait_time//60} دقيقة")
                    await asyncio.sleep(wait_time)
                    continue
                    
                except Exception as e:
                    print(f"Error in {group_id}: {str(e)}")
                    await asyncio.sleep(10)
                    continue
            
            remaining_time = post_interval
            while remaining_time > 0 and users.get(str(user_id), {}).get("auto_post_enabled", False):
                check_delay = min(60, remaining_time)
                await asyncio.sleep(check_delay)
                remaining_time -= check_delay
                
                users = db.get("users") or {}
                
        except SessionRevokedError:
            await handle_session_revoked(user_id)
            break
        except (ConnectionError, TimeoutError, OSError) as e:
            print(f"⚠️ خطأ في الاتصال: {str(e)}")
            await asyncio.sleep(60)
        except Exception as e:
            print(f"❌ خطأ عام: {str(e)}")
            await asyncio.sleep(60)
        finally:
            if temp_client and temp_client.is_connected():
                try:
                    await temp_client.disconnect()
                    await asyncio.sleep(2)  # انتظار قصير بعد قطع الاتصال
                except:
                    pass
    
    users = db.get("users") or {}
    user_data = users.get(str(user_id), {})
    if user_data:
        user_data.pop("auto_post_task", None)
        users[str(user_id)] = user_data
        db.set("users", users)
    
    await client.send_message(user_id, "✅ تم إيقاف النشر التلقائي بنجاح")

async def handle_session_revoked(user_id):
    users = db.get("users") if db.exists("users") else {}
    user_data = users.get(str(user_id), {})
    user_data["auto_post_enabled"] = False
    users[str(user_id)] = user_data
    db.set("users", users)
    await client.send_message(user_id, "🔒 **انتهت صلاحية الجلسة، يرجى إضافة حساب جديد**")

async def mass_post_to_groups(message_text):
    users = db.get("users", {})
    success = 0
    failed = 0
    total_groups = 0
    
    for user_id, user_data in users.items():
        if not user_data.get("accounts"):
            continue
            
        for account in user_data["accounts"]:
            temp_client = None
            try:
                temp_client = TelegramClient(
                    StringSession(account["session"]), 
                    API_ID, 
                    API_HASH,
                    device_model="iPhone 13 Pro",
                    system_version="15.4.1",
                    app_version="9.1"
                )
                await temp_client.connect()
                
                if not await temp_client.is_user_authorized():
                    continue
                
                dialogs = await temp_client.get_dialogs(limit=200)
                
                groups = [
                    dialog.entity for dialog in dialogs 
                    if dialog.is_group and not getattr(dialog.entity, 'broadcast', False)
                ]
                total_groups += len(groups)
                
                for group in groups:
                    try:
                        await temp_client.send_message(
                            group,
                            message_text,
                            link_preview=False,
                            silent=True
                        )
                        success += 1
                        
                        group_id = str(group.id)
                        if 'last_post' not in account:
                            account['last_post'] = {}
                        account['last_post'][group_id] = time.time()
                        
                        await asyncio.sleep(300) 
                        
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds + 60)
                        failed += 1
                        continue
                        
                    except Exception as e:
                        print(f"Error in group {group.id}: {str(e)}")
                        failed += 1
                        await asyncio.sleep(30)
                        continue
                
            except Exception as e:
                print(f"Error with account {account.get('phone_number')}: {str(e)}")
                failed += 1
            finally:
                if temp_client:
                    try:
                        await temp_client.disconnect()
                    except:
                        pass
    
    return len([acc for user in users.values() for acc in user.get("accounts", [])]), total_groups, success, failed

async def broadcast_to_users(message_text):
    users = db.get("users") if db.exists("users") else {}
    success = 0
    failed = 0
    
    for user_id in users.keys():
        try:
            await client.send_message(int(user_id), message_text)
            success += 1
        except Exception as e:
            print(f"{e}")
            failed += 1
        await asyncio.sleep(1) 
    
    return len(users), success, failed

async def update_timer_name(user_id):
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    temp_client = None
    
    while user_timer.get("enabled", False):
        try:
            users = db.get("users") or {}
            user_data = users.get(str(user_id), {})
            
            if not user_data.get("accounts"):
                print(f"❌ لا يوجد حسابات للمستخدم {user_id}")
                break
                
            account = user_data["accounts"][0]
            
            temp_client = TelegramClient(
                StringSession(account["session"]), 
                API_ID, 
                API_HASH,
                connection_retries=3,
                retry_delay=2,
                timeout=20
            )
            await temp_client.connect()
            
            if not await temp_client.is_user_authorized():
                print(f"❌ الحساب غير مصرح به للمستخدم {user_id}")
                break
            
            iraq_time = get_iraq_time()
            font = user_timer.get("font", "Bold")
            
            styled_time = convert_time_to_style(iraq_time, font)
            
            time_with_font = f"{styled_time}"
            
            me = await temp_client.get_me()
            first_name = me.first_name or ""
            last_name = time_with_font
            
            print(f"🔄 {account['phone_number']}: {last_name}")
            
            await temp_client(functions.account.UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            
            await temp_client.disconnect()
            temp_client = None
            print(f"✅ {account['phone_number']}")
            
        except SessionRevokedError:
            print(f"🔒 تم إلغاء الجلسة للمستخدم {user_id}")
            break
        except (ConnectionError, TimeoutError, OSError) as e:
            print(f"⚠️ خطأ في الاتصال: {str(e)}")
            await asyncio.sleep(30)
        except Exception as e:
            print(f"❌ خطأ للمستخدم {user_id}: {str(e)}")
            await asyncio.sleep(30)
        finally:
            if temp_client and temp_client.is_connected():
                try:
                    await temp_client.disconnect()
                    temp_client = None
                except:
                    pass
        
        # فحص كل ثانية لمدة 60 ثانية
        for i in range(60):
            timer_settings = db.get("timer_settings") or {}
            user_timer = timer_settings.get(str(user_id), {})
            if not user_timer.get("enabled", False):
                print(f"⏹ تم إيقاف المؤقت للمستخدم {user_id}")
                return
            await asyncio.sleep(1)

async def update_time_immediately(user_id):
    temp_client = None
    try:
        users = db.get("users") or {}
        user_data = users.get(str(user_id), {})
        
        if not user_data.get("accounts"):
            print(f"❌ لا يوجد حسابات للمستخدم {user_id}")
            return
            
        account = user_data["accounts"][0]
        temp_client = TelegramClient(
            StringSession(account["session"]), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            retry_delay=2,
            timeout=20
        )
        await temp_client.connect()
        
        if not await temp_client.is_user_authorized():
            print(f"❌ الحساب غير مصرح به للمستخدم {user_id}")
            return
        
        timer_settings = db.get("timer_settings") or {}
        user_timer = timer_settings.get(str(user_id), {})
        
        iraq_time = get_iraq_time()
        font = user_timer.get("font", "Bold")
        
        styled_time = convert_time_to_style(iraq_time, font)
        
        time_with_font = f"{styled_time}"
        
        me = await temp_client.get_me()
        first_name = me.first_name or ""
        last_name = time_with_font
        
        print(f"⚡ {account['phone_number']} : {last_name}")
        
        await temp_client(functions.account.UpdateProfileRequest(
            first_name=first_name,
            last_name=last_name
        ))
        
        print(f"✅ {account['phone_number']}")
        
    except SessionRevokedError:
        print(f"🔒 تم إلغاء الجلسة")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass

# الدوال المساعدة
async def get_account_info(session_string):
    """جلب معلومات الحساب"""
    temp_client = None
    try:
        temp_client = TelegramClient(
            StringSession(session_string), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            retry_delay=2,
            timeout=20
        )
        await temp_client.connect()
        
        if not await temp_client.is_user_authorized():
            return {"status": "غير مصرح"}
        
        me = await temp_client.get_me()
        
        # التحقق من حالة الحساب مع SpamBot
        try:
            spam_bot = await temp_client.get_entity("SpamBot")
            await temp_client.send_message(spam_bot, "/start")
            await asyncio.sleep(2)
            messages = await temp_client.get_messages(spam_bot, limit=1)
            spam_response = messages[0].text if messages else ""
            
            if "Good" in spam_response:
                status = "✅ سليم"
            elif "I'm afraid" in spam_response:
                status = "⚠️ قيود مؤقتة"
            elif "Spam" in spam_response:
                status = "❌ سبام"
            elif "block" in spam_response:
                status = "🚫 محظور"
            else:
                status = "🔍 غير معروف"
        except:
            status = "🔍 غير معروف"
        
        return {
            "first_name": me.first_name or "لا يوجد",
            "username": me.username or "لا يوجد",
            "status": status
        }
        
    except SessionRevokedError:
        return {"status": "🔒 الجلسة ملغاة"}
    except Exception as e:
        return {"status": f"خطأ: {str(e)}"}
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass

async def get_active_sessions(session_string):
    """جلب الجلسات النشطة"""
    temp_client = None
    try:
        temp_client = TelegramClient(
            StringSession(session_string), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            retry_delay=2,
            timeout=20
        )
        await temp_client.connect()
        
        if not await temp_client.is_user_authorized():
            return []
        
        # الحصول على الجلسات النشطة
        sessions = await temp_client(functions.account.GetAuthorizationsRequest())
        
        sessions_info = []
        for session in sessions.authorizations:
            sessions_info.append({
                "hash": session.hash,
                "device_model": session.device_model or "غير معروف",
                "platform": session.platform or "غير معروف",
                "app_name": session.app_name or "غير معروف",
                "ip": session.ip or "غير معروف",
                "country": session.country or "غير معروف",
                "active": "نعم" if session.current else "لا"
            })
        
        return sessions_info
        
    except SessionRevokedError:
        print(f"🔒 الجلسة ملغاة")
        return []
    except Exception as e:
        print(f"❌ خطأ في جلب الجلسات: {str(e)}")
        return []
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass

async def get_session_details(session_string, session_hash):
    """جلب تفاصيل جلسة محددة"""
    sessions = await get_active_sessions(session_string)
    for session in sessions:
        if session["hash"] == int(session_hash):
            return session
    return {}

async def terminate_user_session(session_string, session_hash):
    """طرد جلسة محددة"""
    temp_client = None
    try:
        temp_client = TelegramClient(
            StringSession(session_string), 
            API_ID, 
            API_HASH,
            connection_retries=3,
            retry_delay=2,
            timeout=20
        )
        await temp_client.connect()
        
        if not await temp_client.is_user_authorized():
            return False
        
        # طرد الجلسة
        await temp_client(functions.account.ResetAuthorizationRequest(hash=int(session_hash)))
        return True
        
    except SessionRevokedError:
        print(f"🔒 الجلسة ملغاة")
        return False
    except Exception as e:
        print(f"❌ خطأ في طرد الجلسة: {str(e)}")
        return False
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass

async def get_verification_code_from_service(session):
    temp_client = None
    try:
        temp_client = TelegramClient(
            StringSession(session), 
            api_id=API_ID, 
            api_hash=API_HASH,
            connection_retries=3,
            retry_delay=2,
            timeout=20
        )
        await temp_client.connect()
        
        if not await temp_client.is_user_authorized():
            return "The session is not authorized."
        
        messages = await temp_client.get_messages(777000, limit=2)
        if not messages:
            return "No messages"
        
        message = messages[0]
        if not message.text:
            return "The message is empty"
        
        code_match = re.search(r'\b(\d{5})\b', message.text)
        if code_match:
            return code_match.group(1)
        
        for pattern in [r'كود التحقق: (\d+)', r'code: (\d+)', r'(\d{5})']:
            code_match = re.search(pattern, message.text)
            if code_match:
                return code_match.group(1)
        
        return "Not yet arrived"
    
    except SessionRevokedError:
        return "🔒 الجلسة ملغاة"
    except ConnectionError:
        return "خطأ في الاتصال"
    except TimeoutError:
        return "انتهى الوقت المحدد"
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        return f"خطأ: {str(e)}"
    
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass

@client.on(events.CallbackQuery(pattern=b"manage_required_channels"))
async def manage_required_channels(event):
    user_id = event.chat_id
    
    if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
        await event.respond("❌ **ليس لديك صلاحية للإدارة**")
        return
    
    required_channels = db.get("required_channels") or []
    
    channels_count = len(required_channels)
    channels_list = "\n".join([f"• @{channel}" for channel in required_channels]) if required_channels else "❌ لا توجد قنوات"
    
    await event.edit(
        f"⚙️ **قسم قنوات الاشتراك الاجباري**\n\n"
        f"📊 **عدد القنوات :** {channels_count}\n\n"
        f"📋 **القنوات الحالية :**\n{channels_list}",
        buttons=[
            [Button.inline("➕ إضافة قناة", data="ad_req_ch"), Button.inline("🗑 حذف قناة", data="de_req_ch")],
            [Button.inline("📋 عرض القنوات", data="list_required_channels")],
            [Button.inline("🔙 رجوع", data="adminback")]
        ]
    )

@client.on(events.CallbackQuery(pattern=b"ad_req_ch"))
async def add_required_channel(event):
    user_id = event.chat_id
    
    if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
        await event.respond("❌ **ليس لديك صلاحية للإدارة**")
        return
    
    async with client.conversation(event.chat_id) as conv:
        await conv.send_message("📢 **أرسل يوزر أو رابط القناة**")
        channel_msg = await conv.get_response()
        channel_input = channel_msg.text.strip()
        
        if "t.me/" in channel_input:
            channel_username = channel_input.split("t.me/")[-1].replace("@", "").split("/")[0]
        else:
            channel_username = channel_input.replace("@", "")
        
        try:
            channel_entity = await client.get_entity(f"t.me/{channel_username}")
            required_channels = db.get("required_channels") or []
            
            if channel_username in required_channels:
                await conv.send_message("❌ **هذه القناة مضافه مسبقاً**")
            else:
                required_channels.append(channel_username)
                db.set("required_channels", required_channels)
                await conv.send_message(f"✅ **تم إضافة القناة الى الاشتراك الاجباري بنجاح :** @{channel_username}")
        
        except Exception as e:
            await conv.send_message(f"❌ **خطأ في إضافة القناة:** {str(e)}")

@client.on(events.CallbackQuery(pattern=b"de_req_ch"))
async def delete_required_channel(event):
    user_id = event.chat_id
    
    if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
        await event.respond("❌ **ليس لديك صلاحية للإدارة**")
        return
    
    required_channels = db.get("required_channels") or []
    
    if not required_channels:
        await event.edit("❌ **لا توجد قنوات مضافه**")
        return
    
    buttons = []
    for channel in required_channels:
        buttons.append([Button.inline(f"🗑 @{channel}", data=f"del_req_chan_{channel}")])
    
    buttons.append([Button.inline("🔙 رجوع", data="manage_required_channels")])
    
    await event.edit("📋 **اختر القناة التي تريد حذفها:**", buttons=buttons)

@client.on(events.CallbackQuery(pattern=b"del_req_chan_"))
async def delete_specific_required_channel(event):
    user_id = event.chat_id
    
    if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
        await event.respond("❌ **ليس لديك صلاحية للإدارة**")
        return
    
    channel_to_delete = event.data.decode().replace("del_req_chan_", "")
    required_channels = db.get("required_channels") or []
    
    if channel_to_delete in required_channels:
        required_channels.remove(channel_to_delete)
        db.set("required_channels", required_channels)
        await event.edit(f"✅ **تم حذف القناة:** @{channel_to_delete}")
    else:
        await event.edit("❌ **القناة غير موجودة**")

@client.on(events.CallbackQuery(pattern=b"list_required_channels"))
async def list_required_channels(event):
    user_id = event.chat_id
    
    if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
        await event.respond("❌ **ليس لديك صلاحية للإدارة**")
        return
    
    required_channels = db.get("required_channels") or []
    
    if not required_channels:
        channels_list = "❌ **لا توجد قنوات اشتراك اجباري مضافه**"
    else:
        channels_list = "📋 **القنوات المضافه :**\n\n"
        for i, channel in enumerate(required_channels, 1):
            channels_list += f"{i}. @{channel}\n"
    
    await event.edit(
        channels_list,
        buttons=[
            [Button.inline("➕ إضافة قناة", data="add_required_channel")],
            [Button.inline("🗑 حذف قناة", data="delete_required_channel")],
            [Button.inline("🔙 رجوع", data="manage_required_channels")]
        ]
    )

@client.on(events.CallbackQuery(pattern=b"check_subscription"))
async def check_subscription(event):
    user_id = event.chat_id
    
    if await is_user_member(user_id):
        await event.edit("✅ **تم التحقق من الاشتراك بنجاح!**")
        await asyncio.sleep(2)
        await start(event)
    else:
        required_channels = db.get("required_channels") or []
        channels_list = "\n".join([f"• @{channel}" for channel in required_channels])
        
        await event.edit(
            f"❌ **لم يتم الاشتراك في جميع القنوات التاليه اولا**\n\n"
            f"{channels_list}\n\n"
            "✅ **بعد الاشتراك اضغط زر التحقق مرة أخرى**",
            buttons=[
                [Button.inline("🔄 تحقق من الاشتراك", data="check_subscription")]
            ]
        )

@client.on(events.CallbackQuery(pattern=b"timer_section"))
async def timer_section(event):
    user_id = event.chat_id
    
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    timer_enabled = user_timer.get("enabled", False)
    timer_font = user_timer.get("font", "Arial")
    
    buttons = [
        [
            Button.inline(f"تفعيل المؤقت {'✅' if timer_enabled else '❌'}", data="toggle_timer"),
            Button.inline("تعطيل المؤقت", data="disable_timer")
        ],
        [
            Button.inline(f"اختيار خط الوقت: {timer_font}", data="select_timer_font")
        ],
        [
            Button.inline("🔙 رجوع", data="back")
        ]
    ]
    
    status_text = "مفعل" if timer_enabled else "معطل"
    await event.edit(
        f"**🕐 قسم الاسم المؤقت**\n\n"
        f"• حالة المؤقت: **{status_text}**\n"
        f"• الخط الحالي: **{timer_font}**\n\n"
        f"**اختر ما تريد من الازرار الموجودة بالاسفل:**",
        buttons=buttons
    )

@client.on(events.CallbackQuery(pattern=b"toggle_timer"))
async def toggle_timer(event):
    user_id = event.chat_id
    
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    
    users = db.get("users") or {}
    user_data = users.get(str(user_id), {})
    
    if not user_data.get("accounts"):
        await event.answer("❌ ليس لديك حساب مضاف لتفعيل المؤقت", alert=True)
        return
    
    if not user_timer.get("enabled", False):
        user_timer["enabled"] = True
        timer_settings[str(user_id)] = user_timer
        db.set("timer_settings", timer_settings)
        
        asyncio.create_task(update_time_immediately(user_id))
        
        await asyncio.sleep(2)
        asyncio.create_task(update_timer_name(user_id))
        
        await event.answer("✅ تم تفعيل المؤقت وتحديث الوقت فوراً", alert=True)
    else:
        user_timer["enabled"] = False
        timer_settings[str(user_id)] = user_timer
        db.set("timer_settings", timer_settings)
        await event.answer("❌ تم تعطيل المؤقت", alert=True)
    
    await timer_section(event)

@client.on(events.CallbackQuery(pattern=b"disable_timer"))
async def disable_timer(event):
    user_id = event.chat_id
    
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    user_timer["enabled"] = False
    timer_settings[str(user_id)] = user_timer
    db.set("timer_settings", timer_settings)
    
    temp_client = None
    try:
        users = db.get("users") or {}
        user_data = users.get(str(user_id), {})
        
        if user_data.get("accounts"):
            account = user_data["accounts"][0]
            temp_client = TelegramClient(
                StringSession(account["session"]), 
                API_ID, 
                API_HASH,
                connection_retries=3,
                retry_delay=2,
                timeout=20
            )
            await temp_client.connect()
            
            if await temp_client.is_user_authorized():
                me = await temp_client.get_me()
                original_first_name = me.first_name or ""
                await temp_client(functions.account.UpdateProfileRequest(
                    first_name=original_first_name,
                    last_name=""
                ))
    except Exception as e:
        print(f"⚠️ خطأ في استعادة الاسم الأصلي: {str(e)}")
    finally:
        if temp_client and temp_client.is_connected():
            try:
                await temp_client.disconnect()
            except:
                pass
    
    await event.answer("❌ تم تعطيل المؤقت", alert=True)
    await timer_section(event)

@client.on(events.CallbackQuery(pattern=b"select_timer_font"))
async def select_timer_font(event):
    user_id = event.chat_id
    
    current_example = get_iraq_time()
    
    buttons = [
        [
            Button.inline("𝟏𝟐𝟑", data="font_Bold"),
            Button.inline("𝟭𝟮𝟯", data="font_Bold Sans")
        ],
        [
            Button.inline("①②③", data="font_Circled"),
            Button.inline("❶❷❸", data="font_Numbered")
        ],
        [
            Button.inline("11-20", data="font_Circled 11-20"),
            Button.inline("𝟷𝟸𝟹", data="font_Monospace")
        ],
        [
            Button.inline("𝟙𝟚𝟛", data="font_Double-Struck"),
            Button.inline("𝟭𝟮𝟯", data="font_Sans-Serif")
        ],
        [
            Button.inline("𝟏𝟐𝟑", data="font_Arabic-Indic"),
            Button.inline("１２３", data="font_Fullwidth")
        ],
        [
            Button.inline("٠١٢", data="font_Arabic"),
            Button.inline("𝟣𝟤𝟥", data="font_Math Bold")
        ],
        [
            Button.inline("🔙 رجوع", data="timer_section")
        ]
    ]
    
    await event.edit(
        f"**اختر نمط الأرقام الوقت التي تريدها :**\n\n"
        f"**مثال على الوقت الحالي:** {current_example}\n\n"
        "⏰ **التوقيت : توقيت العراق**",
        buttons=buttons
    )

@client.on(events.CallbackQuery(pattern=b"font_"))
async def set_timer_font(event):
    user_id = event.chat_id
    font_type = event.data.decode().replace("font_", "")
    
    timer_settings = db.get("timer_settings") or {}
    user_timer = timer_settings.get(str(user_id), {})
    user_timer["font"] = font_type
    timer_settings[str(user_id)] = user_timer
    db.set("timer_settings", timer_settings)
    
    await event.answer(f"✅ تم تعيين الخط إلى {font_type}", alert=True)
    await timer_section(event)

@client.on(events.CallbackQuery())
async def handle_callbacks(event):
    if db.exists("bot_enabled"):
        if not db.get("bot_enabled"):
            return await event.respond(MESSAGES['BOT_DISABLED'])
    else:
        db.set("bot_enabled", True)
    
    user_id = event.chat_id
    if not await is_user_member(user_id):
        return await event.answer(MESSAGES['CHANNEL_REQUIRED'].format(REQUIRED_CHANNEL), alert=True)
    
    data = event.data.decode('utf-8')
    users = db.get("users") if db.exists("users") else {}
    user_data = users.get(str(user_id), {"accounts": []})
    user_accounts = user_data.get("accounts", [])
    
    if data == "enable_auto_reply":
        users = db.get("users") or {}
        user_data = users.get(str(user_id), {})
        
        if not user_data.get("accounts"):
            await event.answer("❌ ليس لديك حساب مضاف للبوت", alert=True)
            return
        
        auto_reply = db.get("auto_reply") or {}
        
        if str(user_id) not in auto_reply:
            auto_reply[str(user_id)] = {
                "enabled": True,
                "message": "بوت نشر تلقائي مجاني ~» @N3N9bot",
                "active_accounts": {}
            }
        elif "active_accounts" not in auto_reply[str(user_id)]:
            auto_reply[str(user_id)]["active_accounts"] = {}
        
        for account in user_data["accounts"]:
            phone = account["phone_number"]
            auto_reply[str(user_id)]["active_accounts"][phone] = True
            asyncio.create_task(monitor_account(account["session"], user_id, phone))
        
        auto_reply[str(user_id)]["enabled"] = True
        db.set("auto_reply", auto_reply)
        
        await event.answer("✅ تم تفعيل الرد التلقائي وبدأ مراقبة الرسائل الواردة", alert=True)
    
    elif data == "disable_auto_reply":
        auto_reply = db.get("auto_reply") or {}
        if str(user_id) in auto_reply:
            if "active_accounts" not in auto_reply[str(user_id)]:
                auto_reply[str(user_id)]["active_accounts"] = {}
            auto_reply[str(user_id)]["enabled"] = False
            auto_reply[str(user_id)]["active_accounts"] = {}
            db.set("auto_reply", auto_reply)
        await event.answer("❌ تم تعطيل الرد التلقائي وإيقاف المراقبة", alert=True)
    
    elif data == "set_auto_reply_msg":
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("• **أرسل رسالة الرد التلقائي التي تريد استخدامها**")
            msg = await conv.get_response()
            
            auto_reply = db.get("auto_reply") or {}
            
            if str(user_id) not in auto_reply:
                auto_reply[str(user_id)] = {
                    "enabled": False,
                    "message": msg.text,
                    "active_accounts": {}
                }
            else:
                auto_reply[str(user_id)]["message"] = msg.text
                if "active_accounts" not in auto_reply[str(user_id)]:
                    auto_reply[str(user_id)]["active_accounts"] = {}
            
            db.set("auto_reply", auto_reply)
            await conv.send_message("✅ تم حفظ رسالة الرد التلقائي بنجاح")
    
    elif data == "account_status":
        users = db.get("users") or {}
        user_data = users.get(str(user_id), {})
        auto_reply = db.get("auto_reply") or {}
        user_auto_reply = auto_reply.get(str(user_id), {})
        
        status_msg = f"• حالة الحساب : {'مضاف' if user_data.get('accounts') else 'لم تضف حساب بعد'}\n"
        status_msg += f"• الرد التلقائي : {'مفعل' if user_auto_reply.get('enabled', False) else 'معطل'}\n"
        
        if user_auto_reply.get('enabled', False):
            active_accounts = [phone for phone, active in user_auto_reply.get('active_accounts', {}).items() if active]
            status_msg += f"• حساباتك المضافه : {len(active_accounts)}\n"
            status_msg += f"{user_auto_reply.get('message', 'لم يتم تعيين')[:30]}"
        
        await event.answer(status_msg, alert=True)
    
    elif data == "add_account":
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("📞 **أرسل رقم الهاتف مع رمز الدولة **+")
            phone_msg = await conv.get_response()
            phone_number = phone_msg.text.replace("+", "").replace(" ", "")
            
            temp_client = None
            try:
                await conv.send_message("• **جاري طلب كود التحقق**")
                
                from telethon.tl.functions.channels import JoinChannelRequest
                from telethon.errors import SessionPasswordNeededError
                
                # إنشاء العميل مع إعدادات محسنة
                temp_client = TelegramClient(
                    StringSession(), 
                    API_ID, 
                    API_HASH,
                    connection_retries=5,
                    retry_delay=3,
                    timeout=30,
                    device_model="Samsung Galaxy S21",
                    system_version="Android 12",
                    app_version="8.9.0",
                    lang_code="ar",
                    system_lang_code="ar-AR"
                )
                
                await temp_client.connect()
                
                code_request = await temp_client.send_code_request(phone_number)
                
                await conv.send_message("💬 **تم إرسال كود التحقق، أرسل الكود.. ارسله بهذا الشكل** : 1 2 3 4 5")
                code_msg = await conv.get_response()
                code = code_msg.text.replace(" ", "")
                
                if not code or len(code) != 5:
                    await conv.send_message("❌ **كود التحقق غير صحيح**")
                    return
                
                try:
                    await temp_client.sign_in(phone_number, code)
                    session_str = temp_client.session.save()
                    
                    await conv.send_message("✅ **جاري إضافة الحساب...**")
                    
                    channels = db.get("channels") or []
                    
                    for channel in channels:
                        try:
                            if isinstance(channel, int) or (isinstance(channel, str) and channel.isdigit()):
                                channel_entity = await temp_client.get_entity(int(channel))
                            else:
                                channel_entity = await temp_client.get_entity(channel)
                            
                            await temp_client(JoinChannelRequest(channel_entity))
                            await asyncio.sleep(2)
                        except Exception as e:
                            print(f"Error joining channel {channel}: {str(e)}")
                    
                    new_account = {
                        "phone_number": phone_number,
                        "session": session_str,
                        "two_step": None,
                        "status": "verified",
                        "verified_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if user_accounts:
                        user_accounts[0] = new_account
                    else:
                        user_accounts.append(new_account)
                    
                    user_data["accounts"] = user_accounts
                    users[str(user_id)] = user_data
                    db.set("users", users)
                    
                    join_message = f"✅ **تمت إضافة الحساب بنجاح**"
                    
                    await conv.send_message(
                        join_message,
                        buttons=[
                            [Button.inline("تعيين كليشة النشر", data="set_post_msg")],
                            [Button.inline("الرئيسية", data="back")]
                        ]
                    )
                
                except SessionPasswordNeededError:
                    await conv.send_message("🔐 **الحساب محمي بكلمة سر، أرسل كلمة السر**")
                    password_msg = await conv.get_response()
                    password = password_msg.text
                    
                    await temp_client.sign_in(password=password)
                    session_str = temp_client.session.save()
                    
                    await conv.send_message("✅ **جاري إضافة الحساب...**")
                    
                    channels = db.get("channels") or []

                    for channel in channels:
                        try:
                            if isinstance(channel, int) or (isinstance(channel, str) and channel.isdigit()):
                                channel_entity = await temp_client.get_entity(int(channel))
                            else:
                                channel_entity = await temp_client.get_entity(channel)
                            
                            await temp_client(JoinChannelRequest(channel_entity))
                            await asyncio.sleep(2)
                        except Exception as e:
                            print(f"Error joining channel {channel}: {str(e)}")
                    
                    new_account = {
                        "phone_number": phone_number,
                        "session": session_str,
                        "two_step": password,
                        "status": "verified",
                        "verified_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if user_accounts:
                        user_accounts[0] = new_account
                    else:
                        user_accounts.append(new_account)
                    
                    user_data["accounts"] = user_accounts
                    users[str(user_id)] = user_data
                    db.set("users", users)
                    
                    join_message = f"✅ **تمت إضافة الحساب بنجاح**"

                    await conv.send_message(
                        join_message,
                        buttons=[
                            [Button.inline("• الرئيسية •", data="back")]
                        ]
                    )
                
                except Exception as e:
                    await conv.send_message(
                        f"❌ **حدث خطأ أثناء التسجيل: {str(e)}**",
                        buttons=[
                            [Button.inline("إضافة حساب آخر", data="add_account")],
                            [Button.inline("إلغاء", data="back")]
                        ]
                    )
            
            except Exception as e:
                await conv.send_message(
                    f"❌ **حدث خطأ: {str(e)}**",
                    buttons=[
                        [Button.inline("إضافة حساب آخر", data="add_account")],
                        [Button.inline("إلغاء", data="back")]
                    ]
                )
            finally:
                if temp_client and temp_client.is_connected():
                    await temp_client.disconnect()

    
    elif data == "delete_account":
        if not user_accounts:
            await event.answer(MESSAGES['NO_ACCOUNTS'], alert=True)
            return
        
        user_data["accounts"] = []
        users[str(user_id)] = user_data
        db.set("users", users)
        await event.answer("تم حذف الحساب بنجاح", alert=True)
        await event.delete()
    
    elif data == "join_group":
        if not user_accounts:
            await event.answer("ليس لديك حساب مسجل لإجراء هذه العملية", alert=True)
            return
            
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("🔗 أرسل رابط المجموعة أو القناة التي تريد الانضمام إليها")
            group_msg = await conv.get_response()
            group_link = group_msg.text
            
            temp_client = None
            try:
                account = user_accounts[0]
                temp_client = TelegramClient(
                    StringSession(account["session"]), 
                    API_ID, 
                    API_HASH,
                    connection_retries=3,
                    retry_delay=2,
                    timeout=20
                )
                await temp_client.connect()
                
                if 't.me/joinchat/' in group_link or 't.me/+' in group_link:
                    invite_hash = group_link.split('/')[-1]
                    await temp_client(ImportChatInviteRequest(invite_hash))
                else:
                    group_username = group_link.split('/')[-1]
                    await temp_client(JoinChannelRequest(group_username))
                
                await conv.send_message("✅ تم الانضمام بنجاح")
            except Exception as e:
                await conv.send_message(f"❌ فشل في الانضمام: {str(e)}")
            finally:
                if temp_client and temp_client.is_connected():
                    try:
                        await temp_client.disconnect()
                    except:
                        pass
    
    elif data == "set_post_msg":
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("📜 **أرسل كليشة النشر التلقائي الخاصة بك**")
            
            msg = await conv.get_response()
            users = db.get("users") if db.exists("users") else {}
            user_data = users.get(str(user_id), {})
            
            had_previous_message = "post_message" in user_data
            
            user_data["post_message"] = msg.text
            users[str(user_id)] = user_data
            db.set("users", users)
            
            if had_previous_message:
                await conv.send_message(MESSAGES['MESSAGE_REPLACED'])
            else:
                await conv.send_message(MESSAGES['NO_PREVIOUS_MESSAGE'])
    
    elif data == "set_post_interval":
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("⏱ **أرسل الفاصل الزمني بين كل نشر (الحد الأدنى 300 ثانية)**")
            interval_msg = await conv.get_response()
            
            try:
                interval = int(interval_msg.text)
                
                if interval < 300:
                    await conv.send_message("⚠️ **الحد الأدنى المسموح به هو 300 ثانية**")
                    interval = 300 
                
                user_data["post_interval"] = interval
                users[str(user_id)] = user_data
                db.set("users", users)
                
                await conv.send_message(f"✅ **تم تعيين الفاصل الزمني إلى {interval} ثانية**")
            
            except ValueError:
                await conv.send_message("❌ يجب إدخال رقم صحيح فقط")
    
    elif data == "start_auto_post":
        if not user_accounts:
            await event.answer(MESSAGES['NO_ACCOUNTS'], alert=True)
            return
        if "post_message" not in user_data:
            await event.answer(MESSAGES['NO_MESSAGE_SET'], alert=True)
            return
        if "post_interval" not in user_data:
            await event.answer(MESSAGES['NO_INTERVAL_SET'], alert=True)
            return
            
        users = db.get("users") or {}
        user_data = users.get(str(user_id), {})
        user_data["auto_post_enabled"] = True
        user_data["auto_post_task"] = True 
        users[str(user_id)] = user_data
        db.set("users", users)
        
        if "auto_post_task" in user_data:
            try:
                user_data["auto_post_task"].cancel()
            except:
                pass
        
        asyncio.create_task(auto_post(user_id)) 
        await event.answer(MESSAGES['AUTO_POST_STARTED'], alert=True)
    
    elif data == "stop_auto_post":
        users = db.get("users") if db.exists("users") else {}
        user_data = users.get(str(user_id), {})
        user_data["auto_post_enabled"] = False
        user_data["auto_post_task"] = False
        users[str(user_id)] = user_data
        db.set("users", users)
        await event.answer(MESSAGES['AUTO_POST_STOPPED'], alert=True)
    
    elif data == "back":
        users = db.get("users") if db.exists("users") else {}
        
        user_accounts = users.get(str(user_id), {}).get("accounts", [])
        auto_reply = db.get("auto_reply") or {}
        user_auto_reply = auto_reply.get(str(user_id), {})
        
        buttons = [
            [
                Button.inline(f"الحساب : {'✅' if user_accounts else '❌'}", data="account_status"),
                Button.inline(f"الرد التلقائي : {'✅' if user_auto_reply.get('enabled', False) else '❌'}", data="account_status")
            ],
            [
                Button.inline("إضافة حساب", data="add_account"),
                Button.inline("حذف الحساب", data="delete_account")
            ],
            [
                Button.inline("الانضمام لمجموعة/قناة", data="join_group"),
            ],
            [
                Button.inline("تعيين الكليشة", data="set_post_msg"),
                Button.inline("تعيين الفاصل", data="set_post_interval")
            ],
            [
                Button.inline("تفعيل النشر", data="start_auto_post"),
                Button.inline("إيقاف النشر", data="stop_auto_post")
            ],
            [
                Button.inline("تفعيل الرد التلقائي", data="enable_auto_reply"),
                Button.inline("تعطيل الرد التلقائي", data="disable_auto_reply")
            ],
            [
                Button.inline("تعيين رسالة الرد التلقائي", data="set_auto_reply_msg")
            ]
        ]
        
        await event.edit(MESSAGES['USER_MESSAGE'], buttons=buttons)
    
    elif data == "adminback":
        users = db.get("users") if db.exists("users") else {}
        
        user_accounts = users.get(str(user_id), {}).get("accounts", [])
        auto_reply = db.get("auto_reply") or {}
        user_auto_reply = auto_reply.get(str(user_id), {})
        
        buttons = [
            [
                Button.inline("تعطيل البوت", data="disable_bot"),
                Button.inline("تفعيل البوت", data="enable_bot")
            ],
            [
                Button.inline("قسم الاشتراك التلقائي", data="xhhdhshs")
            ],
            [
                Button.inline("قسم الاشتراك الاجباري", data="manage_required_channels")
            ],
            [
                Button.inline("الاحصائيات", data="user_stats"),
                Button.inline("إذاعة", data="broadcast_users")
            ],
            [
                Button.inline("المستخدمين", data="total_users"),
                Button.inline("إجمالي الحسابات", data="total_accounts")
            ],
            [
                Button.inline("فحص الحسابات", data="check_all_accounts")
            ],
            [
                Button.inline("نشر بكل الحسابات", data="mass_post_groups")
            ]
        ]
        
        await event.edit(MESSAGES['ADMIN_MESSAGE'], buttons=buttons)

@client.on(events.CallbackQuery())
async def handle_callbacksr(event):
    user_id = event.chat_id
    data = event.data.decode('utf-8')
    users = db.get("users") if db.exists("users") else {}
    user_data = users.get(str(user_id), {"accounts": []})
    user_accounts = user_data.get("accounts", [])
        
    if data == "disable_bot":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            db.set("bot_enabled", False)
            await event.answer(MESSAGES['BOT_DISABLEDs'], alert=True)
            await send_admin_controls()
    
    elif data == "enable_bot":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            db.set("bot_enabled", True)
            await event.answer(MESSAGES['BOT_ENABLED'], alert=True)
            await send_admin_controls()
    
    elif data == "user_stats":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            users = db.get("users") if db.exists("users") else {}
            total_accounts = sum(len(user.get("accounts", [])) for user in users.values())
            await event.answer(MESSAGES['STATS_MESSAGE'].format(len(users), total_accounts), alert=True)
    
    elif data == "total_users":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            users = db.get("users") if db.exists("users") else {}
            await event.answer(f"إجمالي المستخدمين : {len(users)}", alert=True)
    
    elif data.startswith("check_account:"):
        _, owner_id, phone = data.split(":")
        users = db.get("users") or {}
        user_data = users.get(owner_id, {})
        
        account = next((acc for acc in user_data.get("accounts", []) 
                       if acc.get("phone_number") == phone), None)
        
        if not account:
            await event.answer("❌ الحساب غير موجود", alert=True)
            return
        
        try:
            temp_client = TelegramClient(
                StringSession(account["session"]), 
                API_ID, 
                API_HASH
            )
            await temp_client.connect()
            
            if not await temp_client.is_user_authorized():
                await event.answer("❌ الجلسة غير صالحة", alert=True)
                return
            
            spam_bot = await temp_client.get_entity("SpamBot")
            await temp_client.send_message(spam_bot, "/start")
            await asyncio.sleep(2)
            
            messages = await temp_client.get_messages(spam_bot, limit=1)
            spam_response = messages[0].text if messages else "لا يوجد رد"
            
            status = "❌ غير معروف"
            if "Good" in spam_response:
                status = "✅ سليم"
            elif "I'm afraid" in spam_response:
                status = "⚠️ قيود مؤقته"
            elif "Spam" in spam_response:
                status = "❌ سبام"
            elif "block" in spam_response:
                status = "🚫 محظور/مجمد"
            
            buttons = [
                [Button.inline("🔄 إعادة الفحص", data=f"check_account:{owner_id}:{phone}")],
                [Button.inline("🗑 حذف الحساب", data=f"delete_account:{owner_id}:{phone}")],
                [Button.inline("◀ العودة", data=f"view_account:{owner_id}:{phone}")]
            ]
            
            await event.edit(
                f"📊 نتيجة فحص الحساب:\n\n"
                f"📱 الرقم: {phone}\n"
                f"🔄 الحالة: {status}\n\n"
                f"📄 رد SpamBot:\n{spam_response[:200]}...",
                buttons=buttons
            )
            
        except Exception as e:
            await event.answer(f"❌ خطأ في الفحص: {str(e)}", alert=True)
        finally:
            try:
                await temp_client.disconnect()
            except:
                pass
    
    elif data == "check_all_accounts":
        users = db.get("users") or {}
        results = {
            "Good": 0,
            "afraid": 0,
            "Spam": 0,
            "Blocked": 0,
            "Error": 0
        }
        
        message = await event.edit("⏳ **جاري فحص جميع قيود الحسابات**")
        
        for user_id, user_data in users.items():
            accounts = user_data.get("accounts", [])
            new_accounts = []
            
            for account in accounts:
                try:
                    temp_client = TelegramClient(
                        StringSession(account["session"]), 
                        API_ID, 
                        API_HASH
                    )
                    await temp_client.connect()
                    
                    if not await temp_client.is_user_authorized():
                        results["Error"] += 1
                        continue
                    
                    spam_bot = await temp_client.get_entity("SpamBot")
                    await temp_client.send_message(spam_bot, "/start")
                    await asyncio.sleep(1)
                    
                    messages = await temp_client.get_messages(spam_bot, limit=1)
                    spam_response = messages[0].text if messages else ""
                    
                    if "Good" in spam_response:
                        results["Good"] += 1
                        new_accounts.append(account)
                    elif "afraid" in spam_response:
                        results["afraid"] += 1
                    elif "Spam" in spam_response:
                        results["Spam"] += 1
                    elif "block" in spam_response:
                        results["Blocked"] += 1
                    elif "frozen" in spam_response:
                        results["Blocked"] += 1
                    else:
                        results["Error"] += 1
                        new_accounts.append(account)
                        
                except Exception as e:
                    results["Error"] += 1
                    print(f"{account.get('phone_number')}: {str(e)}")
                finally:
                    try:
                        await temp_client.disconnect()
                    except:
                        pass
            
            if len(new_accounts) != len(accounts):
                user_data["accounts"] = new_accounts
                users[user_id] = user_data
                db.set("users", users)
        
        total = sum(results.values())
        report = (
            f"📊 **تقرير فحص جميع الحسابات**\n\n"
            f"• حسابات سليمة : {results['Good']}\n"
            f"• حسابات مقيده مؤقتاً : {results['afraid']}\n"
            f"• حسابات سبام: {results['Spam']}\n"
            f"• حسابات محظورة/مجمده: {results['Blocked']}\n"
            f"• جلسات منتهيه : {results['Error']}\n\n"
            f"**الإجمالي** : {total} حساب"
        )
        
        buttons = [
            [Button.inline("🔄 تحديث التقرير", data="check_all_accounts")],
            [Button.inline("• رجوع •", data="total_accounts")]
        ]
        
        await message.edit(report, buttons=buttons)
    
    elif data.startswith("delete_account:"):
        _, owner_id, phone = data.split(":")
        users = db.get("users") or {}
        user_data = users.get(owner_id, {})
        
        if user_data and "accounts" in user_data:
            user_data["accounts"] = [acc for acc in user_data["accounts"] 
                                   if acc.get("phone_number") != phone]
            
            if not user_data["accounts"]:
                user_data["auto_post_enabled"] = False
            
            users[owner_id] = user_data
            db.set("users", users)
            await event.answer(f"✅ تم حذف الحساب {phone} بنجاح", alert=True)
        else:
            await event.answer("❌ الحساب غير موجود", alert=True)
    
    elif data == "mass_post_groups":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            async with client.conversation(event.chat_id) as conv:
                await conv.send_message("💬 أرسل الرسالة التي تريد نشرها في جميع المجموعات")
                msg = await conv.get_response()
                
                await event.answer(MESSAGES['MASS_POST_STARTED'], alert=True)
                
                start_time = time.time()
                total_accounts = sum(len(user.get("accounts", [])) for user in db.get("users", {}).values())
                total_groups = 0
                success = 0
                failed = 0
                
                while time.time() - start_time < 7200:
                    result = await mass_post_to_groups(msg.text)
                    total_groups += result[1]
                    success += result[2]
                    failed += result[3]
                    
                    if int(time.time() - start_time) % 600 == 0:
                        await conv.send_message(
                            f"**إحصائيات النشر الحالية**\n"
                            f"✅ **ناجح** : {success}\n"
                            f"❌ **فاشل** : {failed}\n"
                            f"📋 **المجموعات** : {total_groups}"
                        )
                
                await conv.send_message(MESSAGES['MASS_POST_COMPLETED'].format(
                    total_accounts, total_groups, success, failed
                ))
    
    elif data == "broadcast_users":
        if user_id == ADMIN_ID or user_id in (db.get("admins") if db.exists("admins") else []):
            async with client.conversation(event.chat_id) as conv:
                await conv.send_message("• أرسل الرسالة التي تريد اذاعتها لجميع المستخدمين")
                msg = await conv.get_response()
    
                await conv.send_message(MESSAGES['BROADCAST_STARTED'])
    
                total_users, success, failed = await broadcast_to_users(msg.text)
    
                await conv.send_message(
                    MESSAGES['BROADCAST_COMPLETED'].format(
                        total_users, success, failed
                    )
                )
    
    elif data == "xhhdhshs":
        if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
            await event.respond("❌ **ليس لديك صلاحية للإدارة**")
            return
        
        await event.edit(
            "⚙️ **لوحة إدارة القنوات**\n\n"
            "**يمكنك إدارة القنوات التي سيتم الاشتراك فيها تلقائياً**",
            buttons=[
                [Button.inline("➕ إضافة قناة", data="add_channel"), Button.inline("🗑 حذف قناة", data="delete_channel")],
                [Button.inline("📋 عرض القنوات", data="list_channels")],
                [Button.inline("🔙 رجوع", data="adminback")]
            ]
        )
    
    elif data == "add_channel":
        if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
            await event.respond("❌ **ليس لديك صلاحية للإدارة**")
            return
        
        async with client.conversation(event.chat_id) as conv:
            await conv.send_message("📢 **أرسل يوزر أو رابط القناة**")
            channel_msg = await conv.get_response()
            channel_input = channel_msg.text.strip()
            
            if "t.me/" in channel_input:
                channel_username = channel_input.split("t.me/")[-1].replace("@", "")
            else:
                channel_username = channel_input.replace("@", "")
            
            channels = db.get("channels") or []
            
            if channel_username in channels:
                await conv.send_message("❌ **هذه القناة مضافه مسبقاً**")
            else:
                channels.append(channel_username)
                db.set("channels", channels)
                await conv.send_message(f"✅ **تم إضافة القناة:** @{channel_username}")
    
    elif data == "delete_channel":
        if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
            await event.respond("❌ **ليس لديك صلاحية للإدارة**")
            return
        
        channels = db.get("channels") or []
        
        if not channels:
            await event.edit("❌ **لا توجد قنوات مضافه**")
            return
        
        buttons = []
        for channel in channels:
            buttons.append([Button.inline(f"🗑 @{channel}", data=f"del_chan_{channel}")])
        
        buttons.append([Button.inline("🔙 رجوع", data="admin_panel")])
        
        await event.edit("📋 **اختر القناة التي تريد حذفها:**", buttons=buttons)
    
    elif data.startswith("del_chan_"):
        if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
            await event.respond("❌ **ليس لديك صلاحية للإدارة**")
            return
        
        channel_to_delete = data.replace("del_chan_", "")
        channels = db.get("channels") or []
        
        if channel_to_delete in channels:
            channels.remove(channel_to_delete)
            db.set("channels", channels)
            await event.edit(f"✅ **تم حذف القناة:** @{channel_to_delete}")
        else:
            await event.edit("❌ **القناة غير موجودة**")
    
    elif data == "list_channels":
        if user_id != ADMIN_ID and user_id not in (db.get("admins") if db.exists("admins") else []):
            await event.respond("❌ **ليس لديك صلاحية للإدارة**")
            return
        
        channels = db.get("channels") or []
        
        if not channels:
            channels_list = "❌ **لا توجد قنوات مضافه**"
        else:
            channels_list = "📋 **القنوات المضافه:**\n\n"
            for i, channel in enumerate(channels, 1):
                channels_list += f"{i}. @{channel}\n"
        
        await event.edit(
            channels_list,
            buttons=[
                [Button.inline("➕ إضافة قناة", data="add_channel")],
                [Button.inline("🗑 حذف قناة", data="delete_channel")],
                [Button.inline("🔙 رجوع", data="admin_panel")]
            ]
        )
    
client.run_until_disconnected()















