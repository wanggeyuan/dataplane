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
    
def addPortInfo(request):
    try:
        # 获取POST请求中的数据
        data = json.loads(request.body)
        
        # 验证必要字段
        required_fields = ['ipAddress', 'mask', 'arriveSpeed', 'rx', 'tx', 'portName', 'deviceName']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'code': 400,
                    'message': f'缺少必要字段: {field}',
                    'data': []
                })
        
        # 创建新的端口信息记录
        new_port = portInfoModel(
            ipAddress=data['ipAddress'],
            mask=data['mask'],
            arriveSpeed=data['arriveSpeed'],
            rx=data['rx'],
            tx=data['tx'],
            portName=data['portName'],
            deviceName=data['deviceName']
        )
        new_port.save()
        
        # 返回成功响应
        return JsonResponse({
            'code': 200,
            'message': '端口信息添加成功',
            'data': {
                'ipAddress': new_port.ipAddress,
                'mask': new_port.mask,
                'arriveSpeed': new_port.arriveSpeed,
                'rx': new_port.rx,
                'tx': new_port.tx,
                'portName': new_port.portName,
                'deviceName': new_port.deviceName
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'添加端口信息失败: {str(e)}',
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
    
def addDevice(request):
    try:
        # 解析请求数据
        print("开始解析请求数据...")
        payload = json.loads(request.body)
        print(f"请求数据: {payload}")
        
        # 创建新设备
        print("开始创建新设备...")
        new_device = deviceInfoModel(
            deviceType=payload.get('deviceType'),
            deviceName=payload.get('deviceName'),
            throughput=payload.get('throughput', 0),
            verifySpeed=payload.get('verifySpeed', 0),
            avgDelay=payload.get('avgDelay', 0.0),
            verifyMode=payload.get('verifyMode', False),
            tableUsage=payload.get('tableUsage', 0.0)
        )
        print(f"新设备对象创建完成: {new_device.__dict__}")
        
        # 保存到数据库
        print("正在保存到数据库...")
        new_device.save()
        print(f"设备保存成功,ID为: {new_device.id}")
        
        # 返回成功响应
        response_data = {
            'success': True,
            'message': '设备添加成功',
            'data': {
                'id': new_device.id,
                'deviceType': new_device.deviceType,
                'deviceName': new_device.deviceName,
                'throughput': new_device.throughput,
                'verifySpeed': new_device.verifySpeed,
                'avgDelay': new_device.avgDelay,
                'verifyMode': new_device.verifyMode,
                'tableUsage': new_device.tableUsage
            }
        }
        print(f"返回响应: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"添加设备时发生错误: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'添加设备失败: {str(e)}'
        }, status=500)

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
