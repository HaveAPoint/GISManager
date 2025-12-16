from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ZipFileViewSet

router = DefaultRouter()
router.register(r'zip-files', ZipFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
