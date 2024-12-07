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
        # 获取设备名称参数
        device_name = request.GET.get('deviceName')
        
        if device_name:
            # 如果提供了设备名称,只返回该设备的端口信息
            infos = portInfoModel.objects.filter(deviceName=device_name)
        else:
            # 否则返回所有端口信息
            infos = portInfoModel.objects.all()
            
        if not infos.exists():
            return JsonResponse({
                'code': 404,
                'message': f'未找到设备 {device_name} 的端口信息' if device_name else '未找到任何端口信息',
                'data': []
            })
            
        # 构建响应数据
        port_list = []
        for info in infos:
            port_list.append({
                'ipAddress': info.ipAddress,
                'mask': info.mask,
                'arriveSpeed': info.arriveSpeed,
                'rx': info.rx,
                'tx': info.tx,
                'portName': info.portName,
                'deviceName': info.deviceName
            })
            
        response = {
            'code': 200,
            'message': 'success',
            'data': port_list
        }
        
        return JsonResponse(response)
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'获取端口信息失败: {str(e)}',
            'data': []
        })


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
                'deviceType': info.deviceType,  # 添加设备类型
                'deviceName': info.deviceName  # 添加设备名称
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        return HttpResponse(type(e).__name__ + " " + str(e), status=500)


def log(request):
    response = {"log......"}
    return HttpResponse(response)


def vpn(request):
    return HttpResponse("Hello, world. You're at the device vpn.")
