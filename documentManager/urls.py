from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentTagViewSet, DocumentApprovalViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'tags', DocumentTagViewSet)
router.register(r'document-approvals', DocumentApprovalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
