"""
文档管理模型
"""
from django.db import models
from django.conf import settings
from common.models import UUIDModel, TimeStampedModel, SoftDeleteModel


class Document(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """文件表"""
    
    # 文件类型：第一层分类
    FILE_TYPE_CHOICES = [
        ('file', '文件'),
        ('zip', '压缩包'),
    ]
    
    # 文件分类：当 file_type='file' 时使用
    FILE_CATEGORY_CHOICES = [
        ('bidding', '招投标'),
        ('contract', '合同'),
        ('achievement', '成果资料'),
        ('process', '过程资料'),
        ('original', '原始资料'),
        ('handover', '资料交接清单'),
    ]
    
    # 压缩包分类：当 file_type='zip' 时使用
    ZIP_CATEGORY_CHOICES = [
        ('dif', 'DIF'),
        ('dwg', 'DWG'),
        ('other', '其他'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='文件名称'
    )
    original_name = models.CharField(
        max_length=200,
        verbose_name='原始文件名'
    )
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        verbose_name='文件类型',
        help_text='第一层分类：file 或 zip'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='文件分类',
        help_text='第二层分类：根据 file_type 选择对应的分类选项'
    )
    minio_path = models.CharField(
        max_length=500,
        verbose_name='MinIO存储路径'
    )
    minio_bucket = models.CharField(
        max_length=100,
        verbose_name='MinIO存储桶'
    )
    file_size = models.BigIntegerField(
        verbose_name='文件大小(字节)'
    )
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='MIME类型'
    )
    version = models.IntegerField(
        default=1,
        verbose_name='版本号'
    )
    parent_version = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_versions',
        verbose_name='父版本'
    )
    project = models.ForeignKey(
        'project.Project',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='所属项目'
    )
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name='上传人'
    )
    related_files = models.JSONField(
        default=list,
        blank=True,
        help_text='关联文件ID数组',
        verbose_name='关联文件'
    )
    
    class Meta:
        db_table = 'document'
        verbose_name = '文件'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['project', 'file_type', 'category']),
            models.Index(fields=['uploader']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name


class DocumentApproval(UUIDModel, TimeStampedModel):
    """文件审批表"""
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]
    
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='approval_records',
        verbose_name='文件'
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_approvals',
        verbose_name='审批人'
    )
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='审批状态'
    )
    approval_comment = models.TextField(
        blank=True,
        verbose_name='审批意见'
    )
    approval_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='审批时间'
    )
    
    class Meta:
        db_table = 'document_approval'
        verbose_name = '文件审批'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['document']),
            models.Index(fields=['approver', 'approval_status']),
        ]
    
    def __str__(self):
        return f'{self.document.name} - {self.approver.username if self.approver else "无"}'


class DocumentTag(UUIDModel, TimeStampedModel):
    """文件标签表"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='标签名称'
    )
    description = models.TextField(
        blank=True,
        verbose_name='标签描述'
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='标签颜色'
    )
    
    class Meta:
        db_table = 'document_tag'
        verbose_name = '文件标签'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class DocumentTagRelation(UUIDModel, TimeStampedModel):
    """文件标签关联表"""
    
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='tag_relations',
        verbose_name='文件'
    )
    tag = models.ForeignKey(
        DocumentTag,
        on_delete=models.CASCADE,
        related_name='document_relations',
        verbose_name='标签'
    )
    
    class Meta:
        db_table = 'document_tag_relation'
        verbose_name = '文件标签关联'
        verbose_name_plural = verbose_name
        unique_together = [('document', 'tag')]
    
    def __str__(self):
        return f'{self.document.name} - {self.tag.name}'
