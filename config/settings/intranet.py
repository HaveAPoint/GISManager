"""
内网环境配置
"""
from .base import *
import os
from pathlib import Path

# 环境标识
ENVIRONMENT = 'INTRANET'

# 文件存储功能开关
ENABLE_FILE_STORAGE = True

# MinIO配置
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')
MINIO_USE_SSL = os.getenv('MINIO_USE_SSL', 'False') == 'True'
MINIO_BUCKETS = {
    'documents': 'documents',
    'zip-files': 'zip-files',
    'temp': 'temp',
}

# 数据同步配置
SYNC_EXPORT_ENABLED = os.getenv('SYNC_EXPORT_ENABLED', 'True') == 'True'
SYNC_IMPORT_ENABLED = os.getenv('SYNC_IMPORT_ENABLED', 'False') == 'True'

# 项目外网可见强制开关
ALWAYS_EXTERNAL_VISIBLE = os.getenv('ALWAYS_EXTERNAL_VISIBLE', 'True') == 'True'

# 禁用的路由（内网环境为空）
DISABLED_ROUTES = []

