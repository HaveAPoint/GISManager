"""
自定义异常处理器
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    
    统一处理 API 异常，返回标准格式的错误响应
    """
    # 调用默认的异常处理器
    response = exception_handler(exc, context)
    
    # 如果响应为 None，说明是未处理的异常
    if response is not None:
        # 自定义响应格式
        custom_response_data = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', '发生错误'),
                'details': response.data
            }
        }
        response.data = custom_response_data
    
    return response

