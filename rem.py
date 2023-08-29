from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time

# Replace with your own API credentials
api_id = 13382500
api_hash = '6f5691b23c6f032eaae722e96d7e2459'
bot_token = '5327660504:AAE4uw-AF-fWUPoywyVv_gM5EQujZnLTSl4'

app = Client("me_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Replace with your own bot owner's chat ID
bot_owner_chat_id = -1001975251757

# Dictionary to store VPS purchase details
vps_purchase_details = {}  # Key: user_id, Value: {"username": "", "purchase_date": datetime.datetime}

def calculate_reminder_dates(purchase_date):
    reminder_date = purchase_date + datetime.timedelta(days=31)
    renewal_date = purchase_date + datetime.timedelta(days=32)
    return reminder_date, renewal_date

@app.on_message(filters.group & ~filters.edited)
def group_message_handler(client, message):
    try:
        print("Received group message:", message.text)
        if "vps purchase" in message.text.lower():
            print("Found 'vps purchase' keyword")
            user_id = message.from_user.id
            username = message.from_user.username
            purchase_date = datetime.datetime.now()  # Replace with the actual purchase date
            
            vps_purchase_details[user_id] = {"username": username, "purchase_date": purchase_date}
            
            reminder_date, renewal_date = calculate_reminder_dates(purchase_date)
            app.send_message(user_id, f"Reminder: Your VPS renewal is due on {reminder_date.date()}!")
    except Exception as e:
        print("An error occurred in group_message_handler:", e)
    

if __name__ == "__main__":
    try:
        app.start()        
        app.run()
    except Exception as e:
        print("An error occurred during app execution:", e)
