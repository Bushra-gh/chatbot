from datetime import datetime

def get_current_time():
    now = datetime.now()
    return now.strftime("It's %I:%M %p.")
