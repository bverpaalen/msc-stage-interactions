import time
import datetime


#Converts timestamp to seconds
def convertToSeconds(strTime):
    strTime = strTime.replace(" ","")
    varTime = time.strptime(strTime,'%H:%M:%S')
    return datetime.timedelta(hours=varTime.tm_hour,minutes=varTime.tm_min,seconds=varTime.tm_sec).total_seconds()
