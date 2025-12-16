"""
项目管理模型
"""
from django.db import models
from django.conf import settings
from common.models import UUIDModel, TimeStampedModel, SoftDeleteModel


class Project(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """项目表"""
    
    STATUS_CHOICES = [
        ('approval', '立项'),
        ('bidding', '招投标'),
        ('implementation', '实施'),
        ('delivery', '交付'),
        ('completion', '结项'),
        ('archived', '归档'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='项目名称'
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='项目编号'
    )
    description = models.TextField(
        blank=True,
        verbose_name='项目描述'
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_projects',
        verbose_name='项目负责人'
    )
    department = models.ForeignKey(
        'userManager.Department',
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
        verbose_name='所属部门'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='approval',
        verbose_name='项目状态'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='项目开始时间'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='项目结束时间'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects',
        verbose_name='创建人'
    )
    
    class Meta:
        db_table = 'project'
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['code']),
            models.Index(fields=['manager']),
        ]
    
    def __str__(self):
        return self.name


class ProjectMemberPermission(UUIDModel, TimeStampedModel):
    """项目成员权限表"""
    
    PERMISSION_STATUS_CHOICES = [
        ('active', '有效'),
        ('disabled', '已禁用'),
        ('pending', '待审批'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_permissions',
        verbose_name='用户'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='member_permissions',
        verbose_name='项目'
    )
    permission_status = models.CharField(
        max_length=20,
        choices=PERMISSION_STATUS_CHOICES,
        default='active',
        verbose_name='权限状态'
    )
    position = models.CharField(
        max_length=50,
        default='项目成员',
        verbose_name='项目内职位'
    )
    permissions = models.JSONField(
        default=list,
        help_text='权限操作类型：["view", "download", "upload", "modify", "delete"]',
        verbose_name='权限'
    )
    valid_from = models.DateTimeField(
        auto_now_add=True,
        verbose_name='有效期开始时间'
    )
    valid_to = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='有效期结束时间'
    )
    
    class Meta:
        db_table = 'project_member_permission'
        verbose_name = '项目成员权限'
        verbose_name_plural = verbose_name
        unique_together = [('user', 'project')]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['project']),
            models.Index(fields=['user', 'project', 'permission_status']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.project.name}'


class MemberJoinApproval(UUIDModel, TimeStampedModel):
    """成员加入审批表"""
    
    JOIN_TYPE_CHOICES = [
        ('user_apply', '用户申请'),
        ('admin_invite', '管理员邀请'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='join_approvals',
        verbose_name='申请/被邀请用户'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='join_approvals',
        verbose_name='项目'
    )
    join_type = models.CharField(
        max_length=20,
        choices=JOIN_TYPE_CHOICES,
        verbose_name='加入类型'
    )
    admin_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='管理员审批状态'
    )
    user_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name='用户确认状态'
    )
    admin_approval_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='管理员审批时间'
    )
    user_approval_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='用户确认时间'
    )
    admin_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_approvals',
        verbose_name='管理员审批人'
    )
    
    class Meta:
        db_table = 'member_join_approval'
        verbose_name = '成员加入审批'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', 'project']),
            models.Index(fields=['admin_approval_status', 'user_approval_status']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.project.name} - {self.join_type}'
