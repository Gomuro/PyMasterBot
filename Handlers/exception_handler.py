import os
import traceback


def handle_exception(e, bot):
    print(e)
    traceback_info = traceback.format_exc()  # Get information about the call stack
    error_message = str(traceback_info)
    if len(error_message) < 4000:
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Error in bot:\n\n{error_message}")
    else:
        bot.send_message(os.getenv('OWNER_CHAT_ID'), f"Error in bot:\n\n{error_message[:4000]}")
