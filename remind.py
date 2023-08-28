from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time

# Replace with your own API credentials
api_id = 23298188
api_hash = '49869a9d2c46007cc1c1e002e8f8ef2b'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Replace with your own bot owner's chat ID
bot_owner_chat_id = "-1001975251757'

# Dictionary to store VPS purchase dates for each user
vps_purchase_dates = {}

def calculate_next_reminder_date(purchase_date):
    return purchase_date + datetime.timedelta(days=30)

def send_renewal_request_to_channel(user_id):
    # Send a message to the channel requesting renewal for the user
    app.send_message(bot_owner_chat_id, f"Renewal request for user {user_id}: Renewal is due today!")

@app.on_message(filters.command("renew"))
def renew_handler(client, message):
    user_id = message.from_user.id
    vps_purchase_date = datetime.datetime.now()  # Replace with the actual purchase date
    
    vps_purchase_dates[user_id] = vps_purchase_date
    next_reminder_date = calculate_next_reminder_date(vps_purchase_date)
    
    message.reply("VPS purchase date recorded. Next reminder will be sent on {}".format(next_reminder_date))

@app.on_message(filters.command("setreminder"))
def set_reminder_handler(client, message):
    user_id = message.from_user.id
    if user_id not in vps_purchase_dates:
        message.reply("Please use the /renew command first to record your VPS purchase date.")
        return
    
    next_reminder_date = calculate_next_reminder_date(vps_purchase_dates[user_id])
    message.reply("Next reminder will be sent on {}".format(next_reminder_date))

@app.on_callback_query()
def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in vps_purchase_dates:
        if callback_query.data == "yes":
            send_renewal_request_to_channel(user_id)
            callback_query.answer("Renewal request sent to the channel!")
        elif callback_query.data == "no":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Tomorrow", callback_data="tomorrow"), InlineKeyboardButton("Contact Server Owner", callback_data="contact_owner")]
            ])
            callback_query.message.reply("When can you renew?", reply_markup=keyboard)
    else:
        callback_query.answer("Please use the /renew command first to record your VPS purchase date.")

def check_reminders():
    while True:
        current_time = datetime.datetime.now()
        for user_id, purchase_date in vps_purchase_dates.items():
            next_reminder_date = calculate_next_reminder_date(purchase_date)
            if current_time >= next_reminder_date:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Yes", callback_data="yes"), InlineKeyboardButton("No", callback_data="no")]
                ])
                app.send_message(user_id, "Reminder: Your VPS renewal is due today! Do you want to renew?", reply_markup=keyboard)
                vps_purchase_dates[user_id] = next_reminder_date
        time.sleep(3600)  # Check every hour

@app.on_channel_post(filters.channel & ~filters.edited)
def channel_post_handler(client, message):
    # Process purchase details posted in the channel
    # You can extract user IDs and purchase dates from the message and update vps_purchase_dates
    
    # For example:
    user_id = message.from_user.id
    purchase_date = datetime.datetime.now()  # Replace with the actual purchase date
    vps_purchase_dates[user_id] = purchase_date

@app.on_message(filters.command("test"))
async def test_command(client: Client, message: types.Message):
    print(f"/test command invoked by user {message.from_user.id} in group {message.chat.id}")
    await message.reply("Test command received.")

if __name__ == "__main__":
    app.start()
    check_reminders()
    app.run()
