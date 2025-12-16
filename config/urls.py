"""
项目主URL配置
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI 配置
# 注意：JWT 认证配置在 settings.py 的 SWAGGER_SETTINGS 中
# drf_yasg 会自动读取 SWAGGER_SETTINGS['SECURITY_DEFINITIONS'] 并应用到所有接口
schema_view = get_schema_view(
    openapi.Info(
        title="GIS文件管理系统 API",
        default_version='v1',
        description="""
        GIS文件管理系统 API 文档
        
        ## 功能模块
        - 用户管理（部门管理）
        - 项目管理（项目管理、进度管理）
        - 文档管理（Word、PDF、CSV、txt等）管理
        - 地理数据管理（矢量、瓦片、影像，3D等）打包的.zip文件管理
        - 日志管理（操作日志、通知）
        
        ## 认证方式
        使用 JWT Token 认证，在请求头中添加：
        ```
        Authorization: Bearer <your_token>
        ```
        
        1. 先调用 `/api/v1/auth/login/` 接口登录获取 token
        2. 点击右上角 "Authorize" 按钮，输入: Bearer <your_token>
        3. 之后所有需要认证的接口都会自动携带 token
        """,
        #terms_of_service="https://www.example.com/terms/",
        #contact=openapi.Contact(email="contact@example.com"),
        #license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.gateway.urls')),
]

# 开发环境启用 Swagger UI
if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    ]
    # 开发环境静态文件服务
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

