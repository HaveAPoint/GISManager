from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, UserViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'users', UserViewSet)
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
