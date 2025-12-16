"""
API Gateway 视图
提供系统级别的 API 接口
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    operation_summary="健康检查",
    operation_description="检查 API 服务是否正常运行",
    responses={
        200: openapi.Response(
            description="服务正常",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="服务状态",
                        example="ok"
                    ),
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="状态消息",
                        example="API 服务运行正常"
                    ),
                }
            )
        ),
    },
    tags=['系统']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    健康检查接口
    
    用于检查 API 服务是否正常运行，无需认证即可访问
    """
    return Response({
        'status': 'ok',
        'message': 'API 服务运行正常'
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="获取 API 信息",
    operation_description="获取当前 API 版本和基本信息",
    responses={
        200: openapi.Response(
            description="成功返回 API 信息",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'version': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="API 版本",
                        example="v1"
                    ),
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="API 名称",
                        example="GIS文件管理系统 API"
                    ),
                    'description': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="API 描述"
                    ),
                }
            )
        ),
    },
    tags=['系统']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    获取 API 信息
    
    返回当前 API 的版本和基本信息
    """
    return Response({
        'version': 'v1',
        'name': 'GIS文件管理系统 API',
        'description': 'GIS文件管理系统的 RESTful API 接口'
    }, status=status.HTTP_200_OK)

