from django.http import JsonResponse
import json

def is_json(str):
    try:
        json.loads(str)
        return True
    except json.JSONDecodeError:
        return False

class UnifiedResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith('/device'):
            return response
        # 定义统一的响应格式
        unified_response = {
            'code': response.status_code,
            # 'message': response.reason_phrase,
            "order": json.loads(request.body).get('order') if is_json(request.body) else None,
            'data': json.loads(response.content.decode('utf-8')) if is_json(response.content.decode('utf-8')) else response.content.decode('utf-8'),
        }
        # 将原始响应替换为统一的JsonResponse
        new_response = JsonResponse(unified_response)
        # 将原始响应的状态码和其他头信息复制到新的JsonResponse中
        new_response.status_code = response.status_code
        for header, value in response.items():
            new_response[header] = value
        print(unified_response.get('data'))
        return new_response
