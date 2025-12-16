"""
环境路由控制中间件
"""
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone


class EnvironmentRoutingMiddleware:
    """
    环境路由控制中间件
    根据环境配置决定是否允许访问特定路由
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 检查是否为外网环境
        if hasattr(settings, 'ENVIRONMENT') and settings.ENVIRONMENT == 'EXTRANET':
            path = request.path
            
            # 检查是否访问被禁用的路由
            disabled_routes = getattr(settings, 'DISABLED_ROUTES', [])
            for disabled_route in disabled_routes:
                if disabled_route and f'/{disabled_route}/' in path:
                    return JsonResponse({
                        'code': 403,
                        'message': '该功能在当前环境不可用',
                        'data': None,
                        'timestamp': timezone.now().isoformat(),
                    }, status=403)
            
            # 检查是否为只读模式下的写操作
            if getattr(settings, 'READ_ONLY_MODE', False):
                if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                    # 允许数据导入接口
                    if '/api/v1/admin/sync/import/' not in path:
                        return JsonResponse({
                            'code': 403,
                            'message': '外网环境仅支持只读操作',
                            'data': None,
                            'timestamp': timezone.now().isoformat(),
                        }, status=403)
        
        response = self.get_response(request)
        return response

