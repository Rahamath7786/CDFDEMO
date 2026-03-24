from django.http import JsonResponse
from .cdfClient import client

from .services.cdfservice import assetsByDataset, timeseriesByAssetId, getPowerDataCDF, getEnergyData, getLatestDatapointsBulk
# from cdfapp.utils.utils import convertIstToUtcMs, convertUtcToIst, convertUtcToIsts
from cdfapp.utils.utils import convertIstToUtcMs, convertUtcToIst

from django.http import JsonResponse

from django.http import JsonResponse
from cdfapp.cdfClient import client



from django.shortcuts import render
def dashboard(request):
    return render(request, "assets.html")
def getAssets(request):
    try:
        assets = client.assets.list(limit=10)

        data = [
            {
                "name": asset.name,
                "external_id": asset.external_id
            }
            for asset in assets
        ]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def assetsList(request):
    try:
        datasetId = 2732891455160365

        assets = assetsByDataset(datasetId)

        asset_list = [a.dump() for a in assets]

        return JsonResponse({
            "count": len(asset_list),
            "data": asset_list
        }, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

# def inverterTimeseries(request):
#     try:
#         assetId = request.GET.get("assetId")
#         if not assetId:
#             return JsonResponse({"error": "assetId is required"}, status=400)

#         assetId = int(assetId)
#         asset = client.assets.retrieve(id=assetId)
#         assetMake=asset.metadata["make"]
#         # print(assetMake)
#         # print("Metadata:", asset.metadata)

#         ts_list = timeseriesByAssetId(assetId)

#         external_ids = [ts.external_id for ts in ts_list]


#         # SINGLE API CALL
#         latest_data = getLatestDatapointsBulk(external_ids)

#         # Map for fast lookup
#         dp_map = {dp.external_id: dp for dp in latest_data}
#         result = []
#         for ts in ts_list:
#             dp = dp_map.get(ts.external_id)


#             if dp and dp.value not in [0, None]:
#                 last_dp = {
#                     "timestamp": convertUtcToIst(dp.timestamp),
#                     "value": dp.value
#                 }
#             else:
#                 last_dp = None

#             result.append({
#                 "externalId": ts.external_id,
#                 "name": ts.name,
#                 "last_datapoint": last_dp
#             })

#         return JsonResponse({
#             "count": len(result),
#             "data": result
#         })

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)




# =======================================================================================
from django.http import JsonResponse
from .cdfClient import client

from .services.cdfservice import assetsByDataset, timeseriesByAssetId,getLatestDatapointsBulk
from cdfapp.utils.utils import convertIstToUtcMs, convertUtcToIst,convertIstRangeToUtcMs

from django.http import JsonResponse

from django.http import JsonResponse
from cdfapp.cdfClient import client


   
def inverterTimeseries(request):
    try:
        assetId = request.GET.get("assetId")
        if not assetId:
            return JsonResponse({"error": "assetId is required"}, status=400)

        assetId = int(assetId)
        asset = client.assets.retrieve(id=assetId)
        assetMake=asset.metadata["make"]
        # print(assetMake)
        # print("Metadata:", asset.metadata)

        ts_list = timeseriesByAssetId(assetId)

        external_ids = [ts.external_id for ts in ts_list]


        # SINGLE API CALL
        latest_data = getLatestDatapointsBulk(external_ids)

        # Map for fast lookup
        dp_map = {dp.external_id: dp for dp in latest_data}
        result = []
        for ts in ts_list:
            dp = dp_map.get(ts.external_id)


            if dp and dp.value not in [0, None]:
                last_dp = {
                    "timestamp": convertUtcToIst(dp.timestamp),
                    "value": dp.value
                }
            else:
                last_dp = None

            result.append({
                "externalId": ts.external_id,
                "name": ts.name,
                "last_datapoint": last_dp
            })

        return JsonResponse({
            "count": len(result),
            "data": result
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




# =======================================================================================









# ======================================================================================
from django.http import JsonResponse

from datetime import datetime
from django.http import JsonResponse
from datetime import datetime



def energyData(request):
    try:
        externalId = request.GET.get("externalId")
        startDate = request.GET.get("startDate")
        endDate = request.GET.get("endDate")
        interval = request.GET.get("interval")  # ✅ no default hardcode
        dateStr = request.GET.get("date")

        if not externalId:
            return JsonResponse({"status": "error", "message": "externalId required"}, status=400)

        if not interval:
            return JsonResponse({"status": "error", "message": "interval required"}, status=400)

        # Support single date
        if dateStr:
            parsed = datetime.strptime(dateStr, "%Y-%m-%d")
            startDate = parsed.strftime("%d/%m/%Y")
            endDate = startDate

        if not startDate:
            return JsonResponse({"status": "error", "message": "startDate required"}, status=400)

        if not endDate:
            endDate = startDate

        data = getEnergyData(externalId, startDate, endDate, interval)

        return JsonResponse({
            "status": "success",
            "count": len(data),
            "interval": interval,
            "data": data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)




def powerDataCDF(request):
    try:
        externalId = request.GET.get("externalId")
        startDate = request.GET.get("startDate")
        endDate = request.GET.get("endDate")
        interval = request.GET.get("interval")
        inverterModel = request.GET.get("inverterModel")

        if not externalId:
            return JsonResponse({"status": "error", "message": "externalId required"})

        if not interval:
            return JsonResponse({"status": "error", "message": "interval required"})

        if not inverterModel:
            return JsonResponse({"status": "error", "message": "inverterModel required"})

        if not startDate:
            return JsonResponse({"status": "error", "message": "startDate required"})

        if not endDate:
            endDate = startDate

        data = getPowerDataCDF(
            externalId,
            startDate,
            endDate,
            interval,
            inverterModel
        )

        return JsonResponse({
            "status": "success",
            "count": len(data),
            "data": data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })



















