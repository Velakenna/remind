from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time

# Replace with your own API credentials
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

app = Client("me_account", api_id=api_id, api_hash=api_hash)

# Replace with your own bot owner's chat ID
bot_owner_chat_id = YOUR_BOT_OWNER_CHAT_ID

# Dictionary to store VPS purchase details
vps_purchase_details = {}  # Key: user_id, Value: {"username": "", "purchase_date": datetime.datetime}

def calculate_reminder_dates(purchase_date):
    reminder_date = purchase_date + datetime.timedelta(days=31)
    renewal_date = purchase_date + datetime.timedelta(days=32)
    return reminder_date, renewal_date

def send_renewal_request_to_channel(user_id, username):
    # Send a message to the channel requesting renewal for the user
    app.send_message(bot_owner_chat_id, f"Renewal request for user {username} (ID: {user_id}): Renewal is due today!")

@app.on_message(filters.group & ~filters.edited)
def group_message_handler(client, message):
    try:
        if "vps purchase" in message.text.lower():
            user_id = message.from_user.id
            username = message.from_user.username
            purchase_date = datetime.datetime.now()  # Replace with the actual purchase date
            
            vps_purchase_details[user_id] = {"username": username, "purchase_date": purchase_date}
            
            reminder_date, renewal_date = calculate_reminder_dates(purchase_date)
            app.send_message(user_id, f"Reminder: Your VPS renewal is due on {reminder_date.date()}!")
    except Exception as e:
        print("An error occurred in group_message_handler:", e)
    
def check_reminders():
    while True:
        try:
            current_time = datetime.datetime.now()
            for user_id, purchase_info in vps_purchase_details.items():
                purchase_date = purchase_info["purchase_date"]
                reminder_date, renewal_date = calculate_reminder_dates(purchase_date)
                if current_time.date() == reminder_date.date():
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("Renew Now", callback_data="renew_now")]
                    ])
                    app.send_message(user_id, f"Reminder: Your VPS renewal is due tomorrow. Would you like to renew now?", reply_markup=keyboard)
                elif current_time.date() == renewal_date.date():
                    send_renewal_request_to_channel(user_id, purchase_info["username"])
            time.sleep(3600)  # Check every hour
        except Exception as e:
            print("An error occurred in check_reminders:", e)
          
@app.on_callback_query()
def callback_handler(client, callback_query):
    try:
        if callback_query.data == "renew_now":
            user_id = callback_query.from_user.id
            app.send_message(user_id, "Please proceed with the renewal process.")
            # You can add further logic here for handling the renewal process
    except Exception as e:
        print("An error occurred in callback_handler:", e)

if __name__ == "__main__":
    try:
        app.start()
        check_reminders()
        app.run()
    except Exception as e:
        print("An error occurred during app execution:", e)
