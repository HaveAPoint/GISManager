from rest_framework import viewsets, status, decorators, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from documentManager.models import Document
from documentManager.serializers import DocumentSerializer
from .serializers import (
    ZipDocumentSerializer,
    ZipFileUploadSerializer,
    ZipFileValidateSerializer,
    ZipFileContentsResponseSerializer,
)

class ZipFileViewSet(viewsets.ModelViewSet):
    """地理数据(zip)管理接口"""

    queryset = Document.objects.filter(file_type='zip')
    serializer_class = ZipDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # 普通 create 作为兜底（不推荐前端直接用），推荐使用 projects/{id}/zip-files/upload
        return Response({"message": "Use /projects/{id}/zip-files/upload/"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="上传zip文件到指定项目",
        request_body=ZipFileUploadSerializer,
        responses={201: ZipDocumentSerializer}
    )
    @decorators.action(detail=False, methods=['post'], url_path='projects/(?P<project_id>[^/.]+)/zip-files/upload')
    def upload_to_project(self, request, project_id=None):
        # TODO: Implement upload and create Document with file_type='zip'
        return Response({"message": "Upload logic not implemented yet"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="获取项目zip文件列表",
        responses={200: ZipDocumentSerializer(many=True)}
    )
    @decorators.action(detail=False, methods=['get'], url_path='projects/(?P<project_id>[^/.]+)/zip-files')
    def list_by_project(self, request, project_id=None):
        qs = self.get_queryset().filter(project_id=project_id)
        serializer = ZipDocumentSerializer(qs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="下载zip文件",
        responses={200: "Binary content"}
    )
    @decorators.action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        # TODO: Implement download streaming
        return Response({"message": "Download logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="校验zip文件",
        request_body=ZipFileValidateSerializer,
        responses={200: "Validation result"}
    )
    @decorators.action(detail=True, methods=['post'], url_path='validate')
    def validate_zip(self, request, pk=None):
        # TODO: Implement validation logic
        return Response({"message": "Validate logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="获取zip文件内容列表",
        responses={200: ZipFileContentsResponseSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'], url_path='contents')
    def contents(self, request, pk=None):
        # TODO: Implement list contents
        return Response([], status=status.HTTP_200_OK)
