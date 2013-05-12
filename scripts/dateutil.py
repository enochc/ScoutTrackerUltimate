import datetime

today = datetime.datetime.today()

def addMonth(months, date):
    m=0
    month = date.month
    day = date.day
    mod = -1 if months<0 else 1
    while m < abs(months):
        date = date+datetime.timedelta(days=mod)
        if month != date.month:
            m+=1
            month = date.month
    
    while date.day != day:
        date = date+datetime.timedelta(days=mod)          
    return date


print today
print addMonth(-6, today) 
    