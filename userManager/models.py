"""
用户管理模型
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import UUIDModel, TimeStampedModel


class Department(UUIDModel, TimeStampedModel):
    """部门表（公司只有一级部门，所有部门归总经理管）"""
    
    name = models.CharField(
        max_length=100,
        verbose_name='部门名称'
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='部门编号'
    )
    manager = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name='部门负责人'
    )
    
    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class User(AbstractUser, UUIDModel, TimeStampedModel):
    """用户表（扩展Django默认用户）"""
    
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    ]
    
    ROLE_CHOICES = [
        ('super_admin', '超级管理员'),
        ('general_manager', '总经理'),
        ('dept_manager', '部门经理'),
        ('employee', '普通员工'),
    ]
    
    # AbstractUser 已包含 username, email, password, is_active 等字段
    # username 和 email 在 AbstractUser 中已设置为唯一
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='电话号码'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        verbose_name='性别'
    )
    position = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='岗位'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='所属部门'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='角色'
    )
    last_operation_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后操作时间'
    )
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name='创建人'
    )
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return self.username
