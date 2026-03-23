from django.http import JsonResponse
from .cdfClient import client

from .services.cdfservice import assetsByDataset, timeseriesByAssetId, getDatapoints, getLastNonzeroDatapoint

from django.http import JsonResponse

from django.http import JsonResponse
from cdfapp.cdfClient import client



from django.shortcuts import render

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
    


def inverterTimeseries(request):
    try:
        assetId = request.GET.get("assetId")
        if not assetId:
            return JsonResponse({"error": "assetId is required"}, status=400)

        assetId = int(assetId)
        ts_list = timeseriesByAssetId(assetId)

        result = []

        for ts in ts_list:
            last_dp = getLastNonzeroDatapoint(ts.external_id)
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







def dashboard(request):
    return render(request, "assets.html")

