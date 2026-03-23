from cdfapp.cdfClient import client

from datetime import datetime, timedelta
import pytz
from cdfapp.cdfClient import client
from cdfapp.utils.utils import convertIstToUtcMs, convertUtcToIst
IST = pytz.timezone("Asia/Kolkata")


from cdfapp.cdfClient import client

from datetime import datetime
import pytz


def assetsByDataset(datasetId):
    assets = client.assets.list(
        data_set_ids=[datasetId],   # ✅ FIXED HERE
        limit=None
    )
    return assets


def timeseriesByAssetId(assetId):
    ts_list = client.time_series.list(
        asset_ids=[assetId],   # ✅ THIS IS IMPORTANT
        limit=None
    )
    return ts_list




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





