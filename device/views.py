import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# import cmdCPU
from device.models import *


def index(request):
    return HttpResponse("Hello, world. You're at the device index.")


def infoSet(request):
    response = {'infoSet success'}
    return HttpResponse(response)


def netInfo(request):
    try:
        infos = netInfoModel.objects.all()
    except Exception as e:
        return HttpResponse(type(e).__name__ + " " + str(e), status=500)

    response = {}
    for info in infos:
        response[info.id] = {
            'ipAddress': info.ipAddress,
            'mask': info.mask,
            'arriveSpeed': info.arriveSpeed,
        }
    return JsonResponse(response)


def portInfo(request):
    try:
        infos = portInfoModel.objects.all()
    except Exception as e:
        return HttpResponse(type(e).__name__ + " " + str(e), status=500)

    response = {}
    for info in infos:
        response[info.id] = {
            'ipAddress': info.ipAddress,
            'mask': info.mask,
            'arriveSpeed': info.arriveSpeed,
            'rx': info.rx,
            'tx': info.tx,
        }
    # response = [{'rx': 10690, 'tx': 2},
    #             {'rx': 2, 'tx': 10690},
    #             {'rx': 0, 'tx': 0},
    #             {'rx': 0, 'tx': 0},
    #            ]
    return JsonResponse(response)

def verifySwitch(request):
    payload = json.loads(request.body)
    device_id = payload.get('id')

    if device_id is not None:
        try:
            info = deviceInfoModel.objects.get(id=device_id)
            info.verifyMode = not info.verifyMode
            info.save()
            response = {'verifyMode': info.verifyMode}
            return JsonResponse(response, safe=False)
        except deviceInfoModel.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)
    else:
        return JsonResponse({'error': 'ID not provided'}, status=400)

def routeAdd(request):
    response = {'routeAdd success'}
    return HttpResponse(response)


def routeDel(request):
    response = {'routeDel success'}
    return HttpResponse(response)


def routeList(request):
    response = ['10.0.0.0/24 => 0', '10.0.1.0/24 => 1']
    return JsonResponse(response, safe=False)


def verifyAdd(request):
    response = {'verifyAdd success'}
    return HttpResponse(response)


def verifyDel(request):
    response = {'verifyDel success'}
    return HttpResponse(response)


def verifyList(request):
    response = ['10.0.0.0/24 & 0', '10.0.1.0/24 & 1']
    return JsonResponse(response, safe=False)


def deviceInfo(request):
    try:
        all_info = deviceInfoModel.objects.all()
        response = []
        for info in all_info:
            response.append({
                'id': info.id,
                'throughput': info.throughput,
                'verifySpeed': info.verifySpeed,
                'avgDelay': info.avgDelay,
                'verifyMode': info.verifyMode,
                'tableUsage': info.tableUsage,
                'deviceType': info.deviceType  # 添加设备类型
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        return HttpResponse(type(e).__name__ + " " + str(e), status=500)


def log(request):
    response = {"log......"}
    return HttpResponse(response)


def vpn(request):
    return HttpResponse("Hello, world. You're at the device vpn.")
