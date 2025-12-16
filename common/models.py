"""
通用基类模型
"""
import uuid
from django.db import models


class UUIDModel(models.Model):
    """UUID 主键基类"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """时间戳基类"""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """软删除管理器 - 默认过滤已删除数据"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    """软删除基类"""
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='是否删除'
    )
    
    # 默认管理器 - 过滤已删除
    objects = SoftDeleteManager()
    # 包含已删除的管理器
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """软删除方法"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def restore(self):
        """恢复删除"""
        self.is_deleted = False
        self.save(update_fields=['is_deleted'])
