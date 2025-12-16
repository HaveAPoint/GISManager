"""
API Gateway URL配置
"""
from django.urls import path, include
from . import views

urlpatterns = [
    # 系统接口
    path('health/', views.health_check, name='health-check'),
    path('info/', views.api_info, name='api-info'),
    
    # 各模块路由
    path('', include('userManager.urls')),
    path('', include('project.urls')),
    path('', include('documentManager.urls')),
    path('', include('zipManager.urls')),
    # path('logs/', include('logManager.urls')),
    # path('notifications/', include('logManager.urls')),
    
    # 聚合查询接口
    # path('dashboard/overview/', views.DashboardOverviewView.as_view()),
    # path('search/', views.GlobalSearchView.as_view()),
    
    # 数据同步接口
    # path('admin/sync/export/', views.ExportProjectDataView.as_view()),
    # path('admin/sync/import/', views.ImportProjectDataView.as_view()),
]

