from datetime import datetime

def get_current_date():
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y.")
