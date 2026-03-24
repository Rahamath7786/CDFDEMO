
# =======================================================================================
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




# def convertIstRangeToUtcMss(startStr, endStr):
#     startDt = datetime.strptime(startStr, "%Y-%m-%d %H:%M:%S")
#     endDt = datetime.strptime(endStr, "%Y-%m-%d %H:%M:%S")

#     # Optional safety
#     if startDt == endDt:
#         endDt = endDt + timedelta(days=1)

#     startIst = IST.localize(startDt)
#     endIst = IST.localize(endDt)

#     startUtc = startIst.astimezone(pytz.utc)
#     endUtc = endIst.astimezone(pytz.utc)

#     return int(startUtc.timestamp() * 1000), int(endUtc.timestamp() * 1000)


# def convertUtcToIstnew(dt):
#     if not dt:
#         return None

#     ist_time = dt + timedelta(hours=5, minutes=30)
#     return ist_time.strftime("%Y-%m-%d %H:%M:%S")
# =======================================================================================






from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")


def convertIstRangeToUtcMs(startDateStr, endDateStr):
    """
    Input: DD/MM/YYYY, DD/MM/YYYY
    Output: UTC ms range (5AM to 7PM IST)
    """
    startDate = datetime.strptime(startDateStr, "%d/%m/%Y")
    endDate = datetime.strptime(endDateStr, "%d/%m/%Y")

    startIst = IST.localize(startDate.replace(hour=5, minute=0, second=0))
    endIst = IST.localize(endDate.replace(hour=19, minute=0, second=0))

    startUtc = startIst.astimezone(pytz.utc)
    endUtc = endIst.astimezone(pytz.utc)

    return int(startUtc.timestamp() * 1000), int(endUtc.timestamp() * 1000)


def convertUtcToIst(ts):
    utcTime = datetime.utcfromtimestamp(ts / 1000).replace(tzinfo=pytz.utc)
    return utcTime.astimezone(IST)


