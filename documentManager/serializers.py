from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Document, DocumentApproval, DocumentTag, DocumentTagRelation

User = get_user_model()

class DocumentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    uploader_name = serializers.CharField(source='uploader.get_full_name', read_only=True)
    parent_version_name = serializers.CharField(source='parent_version.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'original_name', 'file_type', 'category',
            'minio_path', 'minio_bucket', 'file_size', 'mime_type',
            'version', 'parent_version', 'parent_version_name',
            'project', 'project_name', 'uploader', 'uploader_name',
            'related_files', 'created_at', 'updated_at', 'is_deleted'
        ]
        read_only_fields = ['id', 'version', 'created_at', 'updated_at', 'is_deleted']

class DocumentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'name', 'original_name', 'file_type', 'category',
            'minio_path', 'minio_bucket', 'file_size', 'mime_type',
            'project', 'related_files'
        ]

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text="要上传的文件")
    project = serializers.UUIDField(help_text="所属项目ID")
    category = serializers.CharField(help_text="文件分类，例如 bidding/contract 等")
    file_type = serializers.ChoiceField(choices=['file', 'zip'])

class DocumentApprovalSerializer(serializers.ModelSerializer):
    approver_name = serializers.CharField(source='approver.get_full_name', read_only=True)

    class Meta:
        model = DocumentApproval
        fields = [
            'id', 'document', 'approver', 'approver_name',
            'approval_status', 'approval_comment', 'approval_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'approval_time', 'created_at', 'updated_at']

class DocumentApprovalActionSerializer(serializers.Serializer):
    approval_status = serializers.ChoiceField(choices=['approved', 'rejected'])
    approval_comment = serializers.CharField(required=False, allow_blank=True)

class DocumentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTag
        fields = ['id', 'name', 'description', 'color', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DocumentTagRelationSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = DocumentTagRelation
        fields = ['id', 'document', 'tag', 'tag_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DocumentTagAttachSerializer(serializers.Serializer):
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="要关联的标签ID列表"
    )
