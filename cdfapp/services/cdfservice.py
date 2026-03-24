from cdfapp.cdfClient import client

from datetime import datetime, timedelta
import pytz

from cdfapp.utils.utils import convertIstToUtcMs, convertUtcToIst, convertIstRangeToUtcMs
IST = pytz.timezone("Asia/Kolkata")

from collections import defaultdict


def getLastNonzeroDatapoint(externalId):
    # Fetch latest 100 datapoints (adjust limit as needed)
    dp = client.time_series.data.retrieve(
        external_id=externalId,
        # latest=True gives the latest point first in some SDKs; if not, use start/end to fetch last points
        limit=100  
    )

    data = dp.dump().get("datapoints", [])

    # Reverse to start checking from latest
    for d in reversed(data):
        if d.get("value") not in [0, None]:
            return {
                "timestamp": convertUtcToIst(d["timestamp"]),
                "value": d["value"]
            }
    # Return None if all zeros
    return None


def getDatapoints(externalId, dateStr):
    start, end = convertIstToUtcMs(dateStr)

    dp = client.time_series.data.retrieve(
        external_id=externalId,
        start=start,
        end=end
    )

    data = dp.dump()

    # Convert timestamps to IST format
    formatted = [
        {
            "timestamp": convertUtcToIst(d["timestamp"]),
            "value": d["value"]
        }
        for d in data.get("datapoints", [])
    ]

    return formatted
# =======================================================================================================

def timeseriesByAssetId(assetId):
    ts_list = client.time_series.list(
        asset_ids=[assetId], 
        limit=None
    )
    return ts_list



# using

def getLatestDatapointsBulk(external_ids):
    res = client.time_series.data.retrieve_latest(
        external_id=external_ids,
        ignore_bad_datapoints=True
    )
    return res




def assetsByDataset(datasetId):
    assets = client.assets.list(
        data_set_ids=[datasetId],  
        limit=None
    )
    return assets

# =======================================================================================================



def getEnergyData(externalId, startDateStr, endDateStr, interval):
    if not interval:
        return []

    # Convert IST → UTC
    startMs, endMs = convertIstRangeToUtcMs(startDateStr, endDateStr)

    try:
        res = client.time_series.data.retrieve(
            external_id=externalId,
            start=startMs,
            end=endMs,
            aggregates=["sum"],
            granularity=interval   
        )
    except Exception as e:
        print("CDF error:", e)
        return []

    result = []

    # res is iterable of Datapoint objects
    for dp in res:
        # dp.timestamp is in ms
        ist_time = convertUtcToIst(dp.timestamp)

        # dp.sum contains the aggregated value
        value = getattr(dp, "sum", 0)

        result.append({
            "timestamp": ist_time.strftime("%d/%m/%Y %H:%M:%S"),
            "value": value/1000
        })

    return result
    


def resolveDateRange(startDate, endDate, month, year):
    now = datetime.now(IST)

    if year and not month:
        start = IST.localize(datetime(int(year), 1, 1))
        end = now if int(year) == now.year else IST.localize(datetime(int(year), 12, 31, 23, 59, 59))
        granularity = "1month"
        mode = "year"

    elif month:
        m = int(month)
        y = int(year) if year else now.year

        start = IST.localize(datetime(y, m, 1))
        end = now if (y == now.year and m == now.month) else IST.localize(
            datetime(y, m + 1, 1) - timedelta(seconds=1)
        )

        granularity = "1day"
        mode = "month"

    else:
        start = IST.localize(datetime.strptime(startDate, "%d/%m/%Y").replace(hour=5))
        end = IST.localize(datetime.strptime(endDate, "%d/%m/%Y").replace(hour=19))

        granularity = None
        mode = "day"

    return int(start.astimezone(pytz.utc).timestamp()*1000), int(end.astimezone(pytz.utc).timestamp()*1000), granularity, mode



def fetchSeries(externalId, startMs, endMs, interval):
    try:
        res = client.time_series.data.retrieve(
            external_id=externalId,
            start=startMs,
            end=endMs,
            aggregates=["sum"],   # same as your working code
            granularity=interval
        )

        data = {}
        for dp in res:
            data[dp.timestamp] = getattr(dp, "sum", 0)

        return data

    except Exception as e:
        print("CDF error:", externalId, e)
        return {}


def getPowerDataCDF(baseExternalId, startDate, endDate, interval, inverterModel):

    startMs, endMs = convertIstRangeToUtcMs(startDate, endDate)

    result = []

    # ---------------- THEA ----------------
    if inverterModel.lower() == "thea":

        p1 = fetchSeries(f"{baseExternalId}.p1W", startMs, endMs, interval)
        p2 = fetchSeries(f"{baseExternalId}.p2W", startMs, endMs, interval)
        p3 = fetchSeries(f"{baseExternalId}.p3W", startMs, endMs, interval)
        p4 = fetchSeries(f"{baseExternalId}.dW", startMs, endMs, interval)
        ac = fetchSeries(f"{baseExternalId}.acW", startMs, endMs, interval)

        # merge timestamps
        timestamps = sorted(set(p1) | set(p2) | set(p3) | set(p4) | set(ac))

        for ts in timestamps:
            pv = (
                p1.get(ts, 0) +
                p2.get(ts, 0) +
                p3.get(ts, 0) +
                p4.get(ts, 0)
            )

            active = ac.get(ts, 0)

            ist_time = convertUtcToIst(ts)

            result.append({
                "timestamp": ist_time.strftime("%d/%m/%Y %H:%M:%S"),
                "pvPower": round(pv / 1000, 2),
                "activePower": round(active / 1000, 2)
            })

    # ---------------- KSOLARE ----------------
    else:

        p1V = fetchSeries(f"{baseExternalId}.p1V", startMs, endMs, interval)
        p1A = fetchSeries(f"{baseExternalId}.p1A", startMs, endMs, interval)

        p2V = fetchSeries(f"{baseExternalId}.p2V", startMs, endMs, interval)
        p2A = fetchSeries(f"{baseExternalId}.p2A", startMs, endMs, interval)

        p3V = fetchSeries(f"{baseExternalId}.p3V", startMs, endMs, interval)
        p3A = fetchSeries(f"{baseExternalId}.p3A", startMs, endMs, interval)

        p4V = fetchSeries(f"{baseExternalId}.p4V", startMs, endMs, interval)
        p4A = fetchSeries(f"{baseExternalId}.p4A", startMs, endMs, interval)

        oP = fetchSeries(f"{baseExternalId}.oP", startMs, endMs, interval)

        timestamps = sorted(set(oP))

        for ts in timestamps:

            pv = (
                p1V.get(ts, 0) * p1A.get(ts, 0) +
                p2V.get(ts, 0) * p2A.get(ts, 0) +
                p3V.get(ts, 0) * p3A.get(ts, 0) +
                p4V.get(ts, 0) * p4A.get(ts, 0)
            )

            active = oP.get(ts, 0)

            ist_time = convertUtcToIst(ts)

            result.append({
                "timestamp": ist_time.strftime("%d/%m/%Y %H:%M:%S"),
                "pvPower": round(pv / 1000, 2),
                "activePower": round(active / 1000, 2)
            })

    return result











































