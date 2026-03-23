
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")

def convertIstToUtcMs(dateStr):
    """
    Input: DD/MM/YYYY
    Output: start_ms, end_ms (UTC)
    """
    istDate = datetime.strptime(dateStr, "%d/%m/%Y")

    # Start of day IST
    startIst = IST.localize(istDate)

    # End of day IST
    endIst = startIst + timedelta(days=1)

    # Convert to UTC
    startUtc = startIst.astimezone(pytz.utc)
    endUtc = endIst.astimezone(pytz.utc)

    return int(startUtc.timestamp() * 1000), int(endUtc.timestamp() * 1000)


def convertUtcToIst(ts):
    utcTime = datetime.utcfromtimestamp(ts / 1000).replace(tzinfo=pytz.utc)
    istime = utcTime.astimezone(IST)
    return istime.strftime("%d/%m/%Y %H:%M:%S")






