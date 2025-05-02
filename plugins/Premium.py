# © TechifyBots (Rahul)
import pytz
import datetime
import asyncio
from info import ADMINS, USERNAME, LOG_CHANNEL, QR_CODE
from Script import script 
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong

@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium(client, message):
    try:
        _, user_id, time, *custom_message = message.text.split(" ", 3)
        custom_message = "Thanks For Taking Subscription" if not custom_message else " ".join(custom_message)
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y : %I:%M:%S %p")
        user = await client.get_users(user_id)
        seconds = await get_seconds(time)        
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user.id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            data = await db.get_user(user.id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  :  %I:%M:%S %p")
            await message.reply_text(f"Premium access added to the user\n\nUser: {user.mention}\n\nUser ID: <code>{user_id}</code>\n\nPremium access: {time}\n\nJoining: {current_time}\n\nExpiry: {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(chat_id=user_id, text=f"<b>{user.mention},\n\nPremium added to your account. Enjoy!\n\nPremium Access - {time}\n\nJoining - {current_time}\n\nExpire In - {expiry_str_in_ist}</b>\n\n{custom_message}", disable_web_page_preview=True)
            await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\nUser - {user.mention}\n\nID - <code>{user_id}</code>\n\nPremium Access - {time}\n\nJoining - {current_time}\n\nExpiry - {expiry_str_in_ist}\n\n{custom_message}", disable_web_page_preview=True)
        else:
            await message.reply_text("<b>⚠️ Invalid format, use this format - <code>/addpremium 1030335104 1day</code>\n\n<u>Time format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange as your wish like 2, 3, 4, 5 etc....</b>")
    except ValueError:
        await message.reply_text("<b>⚠️ Invalid format, use this format - <code>/addpremium 1030335104 1day</code>\n\n<u>Time format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange as your wish like 2, 3, 4, 5 etc....</b>")
    except Exception as e:
        await message.reply_text(f"error - {e}")

@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("Successfully removed.")
            await client.send_message(
                chat_id=user_id,
                text=f"Hi {user.mention},\n\nYour premium access has been removed."
            )
        else:
            await message.reply_text("Unable to remove. Are you sure it was a premium user ID?")
    else:
        await message.reply_text("Usage: <code>/removepremium user_id</code>")

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")            
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"#Premium_Info:\n\nUser: {user}\n\nUser ID: <code>{user_id}</code>\n\nTime Left: {time_left_str}\n\nExpiry: {expiry_str_in_ist}.")   
    else:
        await message.reply_text(f"{user},\n\nYou do not have any active premium plans. If you want to take premium then check /plan for more details...")

@Client.on_message(filters.command("checkplan") & filters.user(ADMINS))
async def check_plan(client, message):
    if len(message.text.split()) == 1:
        await message.reply_text("Use this command with user ID... like\n\n /checkplan user_id")
        return
    user_id = int(message.text.split(' ')[1])
    user_data = await db.get_user(user_id)

    if user_data and user_data.get("expiry_time"):
        expiry = user_data.get("expiry_time")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        response = (
            f"User ID: {user_id}\n"
            f"Name: {(await client.get_users(user_id)).mention}\n"
            f"Expiry Date: {expiry_str_in_ist}\n"
            f"Expiry Time: {time_left_str}"
        )
    else:
        response = "User does not have premium..."
    await message.reply_text(response)

@Client.on_message(filters.command('plan') & filters.incoming)
async def plan(client, message):
    user_id = message.from_user.id
    if message.from_user.username:
        user_info = f"@{message.from_user.username}"
    else:
        user_info = f"{message.from_user.mention}"
    log_message = f"#Plan\n\nThis user tried to check plan\n\n- ID - `{user_id}`\n- Name - {user_info}"
    btn = [[
        InlineKeyboardButton("Send Screenshot", url=USERNAME),
    ],[
        InlineKeyboardButton("Close", callback_data="close_data")
    ]]
    await client.send_message(LOG_CHANNEL, log_message)
    r=await message.reply_photo(
        photo=(QR_CODE),
        caption=script.PREMIUM_TEXT, 
        reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(120)
    await r.delete()

@Client.on_message(filters.command("premiumuser") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("Fetching ...")  
    users = await db.get_all_users()
    users_list = []
    async for user in users:
        users_list.append(user)    
    user_data = {user['id']: await db.get_user(user['id']) for user in users_list}    
    new_users = []
    for user in users_list:
        user_id = user['id']
        data = user_data.get(user_id)
        expiry = data.get("expiry_time") if data else None        
        if expiry:
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")          
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days, remainder = divmod(time_left.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)            
            time_left_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"            
            user_info = await client.get_users(user_id)
            user_str = (
                f"{len(new_users) + 1}. User ID: {user_id}\n"
                f"Name: {user_info.mention}\n"
                f"Expiry Date: {expiry_str_in_ist}\n"
                f"Expiry Time: {time_left_str}\n\n"
            )
            new_users.append(user_str)
    new = "Paid Users - \n\n" + "\n".join(new_users)   
    try:
        await aa.edit_text(new)
    except MessageTooLong:
        with open('premiumuser.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('premiumuser.txt', caption="Paid Users:")
