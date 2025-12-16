from rest_framework import viewsets, status, decorators, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Document, DocumentApproval, DocumentTag, DocumentTagRelation
from .serializers import (
    DocumentSerializer, DocumentCreateUpdateSerializer, DocumentUploadSerializer,
    DocumentApprovalSerializer, DocumentApprovalActionSerializer,
    DocumentTagSerializer, DocumentTagRelationSerializer, DocumentTagAttachSerializer
)

class DocumentViewSet(viewsets.ModelViewSet):
    """文件管理接口"""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DocumentCreateUpdateSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    @swagger_auto_schema(
        operation_description="上传文件",
        request_body=DocumentUploadSerializer,
        responses={201: DocumentSerializer}
    )
    @decorators.action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        # TODO: Implement upload logic (handle file, save to storage, create record)
        return Response({"message": "Upload logic not implemented yet"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="下载文件",
        responses={200: "Binary content"}
    )
    @decorators.action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        # TODO: Implement download streaming
        return Response({"message": "Download logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="文件预览",
        responses={200: "Preview content"}
    )
    @decorators.action(detail=True, methods=['get'], url_path='preview')
    def preview(self, request, pk=None):
        # TODO: Implement preview logic
        return Response({"message": "Preview logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="获取文件版本历史",
        responses={200: DocumentSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'], url_path='versions')
    def versions(self, request, pk=None):
        # TODO: Implement version listing
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="版本回滚",
        responses={200: DocumentSerializer}
    )
    @decorators.action(detail=True, methods=['post'], url_path='rollback')
    def rollback(self, request, pk=None):
        # TODO: Implement rollback
        return Response({"message": "Rollback logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="审批文件",
        request_body=DocumentApprovalActionSerializer,
        responses={200: DocumentApprovalSerializer}
    )
    @decorators.action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        # TODO: Implement approval flow
        return Response({"message": "Approve logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="获取审批历史",
        responses={200: DocumentApprovalSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'], url_path='approval-history')
    def approval_history(self, request, pk=None):
        # TODO: Implement approval history
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="为文件添加标签",
        request_body=DocumentTagAttachSerializer,
        responses={200: DocumentTagRelationSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['post'], url_path='tags')
    def add_tags(self, request, pk=None):
        # TODO: Implement tag attach
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="移除文件标签",
        responses={204: "Success"}
    )
    @decorators.action(detail=True, methods=['delete'], url_path='tags/(?P<tag_id>[^/.]+)')
    def remove_tag(self, request, pk=None, tag_id=None):
        # TODO: Implement tag removal
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentTagViewSet(viewsets.ModelViewSet):
    """标签管理接口"""

    queryset = DocumentTag.objects.all()
    serializer_class = DocumentTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']


class DocumentApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    """文件审批记录查询接口"""

    queryset = DocumentApproval.objects.all()
    serializer_class = DocumentApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
