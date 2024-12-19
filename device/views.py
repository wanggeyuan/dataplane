import json
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# import cmdCPU
from device.models import *
from django.db import transaction
from device.config import CURRENT_DEVICE_NAME
from threading import Timer

# 在文件顶部添加一个全局变量来存储上一次的路由表
last_printed_routes = None
last_routes = None
print_timer = None

# 在文件开头添加接口映射关系
INTERFACE_MAPPING = {
    'v6_1': 'eth5',
    'v6_3': 'eth3',
    'v6_4': 'eth2'
}

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
        
        # 检查设备名是否已存在
        device_name = payload.get('deviceName')
        print(f"检查设备名 '{device_name}' 是否已存在...")
        
        if deviceInfoModel.objects.filter(deviceName=device_name).exists():
            print(f"设备名 '{device_name}' 已存在")
            return JsonResponse({
                'success': False,
                'message': f"设备名 '{device_name}' 已存在，请使用其他设备名"
            })
        
        # 创建新设备
        print("开始创建新设备...")
        new_device = deviceInfoModel(
            deviceType=payload.get('deviceType'),
            deviceName=device_name,
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
    
def deleteDevice(request):
    try:
        print("开始解析请求数据...")
        payload = json.loads(request.body)
        device_name = payload.get('deviceName')
        print(f"请求删除设备: {device_name}")
        
        # 使用事务确保原子性
        with transaction.atomic():
            try:
                # 先删除设备
                device = deviceInfoModel.objects.get(deviceName=device_name)
                device.delete()
                print(f"设备 {device_name} 删除成功")
                
                # 返回成功响应
                return JsonResponse({
                    'data': {
                        'success': True,
                        'message': f'设备 {device_name} 删除成功'
                    }
                })
                
            except deviceInfoModel.DoesNotExist:
                print(f"设备 {device_name} 不存在")
                return JsonResponse({
                    'data': {
                        'success': False,
                        'message': f'设备 {device_name} 不存在'
                    }
                }, status=404)
            
    except Exception as e:
        print(f"删除设备时发生错误: {str(e)}")
        return JsonResponse({
            'data': {
                'success': False,
                'message': f'删除设备失败: {str(e)}'
            }
        }, status=500)

def deleteDevicePorts(request):
    try:
        payload = json.loads(request.body)
        device_name = payload.get('deviceName')
        
        # 删除设备相关的所有端口
        ports = portInfoModel.objects.filter(deviceName=device_name)
        if ports.exists():
            ports.delete()
            return JsonResponse({
                'data': {
                    'success': True,
                    'message': f'设备 {device_name} 的端口信息删除成功'
                }
            })
        else:
            return JsonResponse({
                'data': {
                    'success': True,
                    'message': f'设备 {device_name} 没有相关的端口信息'
                }
            })
            
    except Exception as e:
        return JsonResponse({
            'data': {
                'success': False,
                'message': f'删除端口信息失败: {str(e)}'
            }
        }, status=500)
    
def deletePort(request):
    try:
        payload = json.loads(request.body)
        device_name = payload.get('deviceName')
        port_name = payload.get('portName')
        
        # 查找并删除指定的端口
        try:
            port = portInfoModel.objects.get(
                deviceName=device_name,
                portName=port_name
            )
            port.delete()
            
            return JsonResponse({
                'data': {
                    'success': True,
                    'message': f'端口 {port_name} 删除成功'
                }
            })
            
        except portInfoModel.DoesNotExist:
            return JsonResponse({
                'data': {
                    'success': False,
                    'message': f'端口不存在'
                }
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            'data': {
                'success': False,
                'message': f'删除端口失败: {str(e)}'
            }
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


def generate_openwrt_commands(routes):
    """生成OpenWrt命令"""
    commands = []
    processed_tables = set()
    
    for route in routes["根据路径转换后的路由表"]:
        try:
            source_network = route["源地址"]
            target_network = route["目标"]
            table_name = f"table_from_{source_network.split(':')[1].split('/')[0]}"
            
            # 检查接口映射是否存在
            if route['入接口'] not in INTERFACE_MAPPING:
                print(f"跳过路由: 接口 {route['入接口']} 未配置映射关系")
                continue
            if route['出接口'] not in INTERFACE_MAPPING:
                print(f"跳过路由: 接口 {route['出接口']} 未配置映射关系")
                continue
            
            # 如果是新的路由表，添加创建、清空和规则相关命令
            if table_name not in processed_tables:
                commands.extend([
                    f"# 创建路由表 {table_name}",
                    f"cat /etc/iproute2/rt_tables | grep {table_name} || echo \"100 {table_name}\" >> /etc/iproute2/rt_tables",
                    "",
                    f"# 清空路由表 {table_name}",
                    f"ip -6 route flush table {table_name}",
                    "",
                    f"# 删除与 {table_name} 相关的规则",
                    f"ip -6 rule del from {source_network} iif {INTERFACE_MAPPING[route['入接口']]} lookup {table_name} prio 32764 2>/dev/null || true",
                    "",
                    f"# 添加规则到 {table_name}",
                    f"ip -6 rule add from {source_network} iif {INTERFACE_MAPPING[route['入接口']]} lookup {table_name} prio 32764",
                    ""
                ])
                processed_tables.add(table_name)
            
            # 添加具体路由命令
            commands.append(f"# 添加从 {source_network} 到 {target_network} 的路由")
            commands.append(
                f"ip -6 route add {target_network} via {route['网关']} dev {INTERFACE_MAPPING[route['出接口']]} table {table_name}"
            )
            commands.append("")
            
        except KeyError as e:
            print(f"错误: 处理路由时发生错误，缺少必要的字段: {e}")
            continue
        except Exception as e:
            print(f"错误: 处理路由时发生未知错误: {e}")
            continue
    
    return "\n".join(commands)

def receiveRouteTable(request):
    try:
        global last_routes, print_timer
        print(f"当前设备名称: {CURRENT_DEVICE_NAME}")
        payload = json.loads(request.body)
        route_table = payload.get('routeTable')

        if route_table is None:
            return JsonResponse({
                'code': 400,
                'message': '缺少路由表数据'
            }, status=400)
            
        # 过滤当前设备的路由表内容
        device_routes = [route for route in route_table if route['deviceName'] == CURRENT_DEVICE_NAME]
        
        # 构建格式化的路由表数据
        formatted_routes = {
            "设备名称": CURRENT_DEVICE_NAME,
            "根据路径转换后的路由表": [
                {
                    "入接口": route['in_interface'],
                    "出接口": route['out_interface'],
                    "源地址": route['source_network'],
                    "目标": route['target'],
                    "网关": route['gateway'],
                    "度量值": route['metric'],
                    "表": route['table'],
                    "说明": f"到达终端{route['target'][-1]}的路由：通过{route['deviceName']}转发到终端{route['target'][-1]}"
                }
                for route in device_routes
            ]
        }

        # 保存当前路由表
        last_routes = formatted_routes

        # 如果有定时器在运行，取消它
        if print_timer:
            print_timer.cancel()

        # 设置新的定时器，2秒后打印
        def delayed_print():
            if last_routes:
                print("\n最终路由表内容:")
                print(json.dumps(last_routes, ensure_ascii=False, indent=2))
                print("\nOpenWrt命令:")
                print(generate_openwrt_commands(last_routes))

        print_timer = Timer(1.5, delayed_print)
        print_timer.start()

        return JsonResponse({
            'code': 200,
            'message': '路由表信息接收并打印成功'
        })

    except Exception as e:
        print(f"\n处理路由表时发生错误: {str(e)}")
        return JsonResponse({
            'code': 500,
            'message': f'接收路由表信息失败: {str(e)}'
        }, status=500)
