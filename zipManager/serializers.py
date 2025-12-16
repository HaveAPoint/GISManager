from rest_framework import serializers
from documentManager.serializers import DocumentSerializer
from documentManager.models import Document

class ZipDocumentSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        model = Document
        fields = DocumentSerializer.Meta.fields
        read_only_fields = DocumentSerializer.Meta.read_only_fields

class ZipFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text="要上传的zip文件")
    project_id = serializers.UUIDField(help_text="所属项目ID")
    category = serializers.CharField(help_text="zip分类，如 dif/dwg/other")

class ZipFileValidateSerializer(serializers.Serializer):
    rules = serializers.JSONField(required=False, help_text="可选的校验规则参数")

class ZipFileContentsResponseSerializer(serializers.Serializer):
    path = serializers.CharField(help_text="文件/目录路径")
    size = serializers.IntegerField(help_text="大小，字节")
    type = serializers.ChoiceField(choices=['file', 'dir'])
