"""
外网环境配置
"""
from .base import *
import os

# 环境标识
ENVIRONMENT = 'EXTRANET'

# 文件存储功能关闭
ENABLE_FILE_STORAGE = False

# MinIO配置（无效配置，外网不连接MinIO）
MINIO_ENDPOINT = None
MINIO_ACCESS_KEY = None
MINIO_SECRET_KEY = None
MINIO_USE_SSL = False
MINIO_BUCKETS = {}

# 数据同步配置
SYNC_EXPORT_ENABLED = os.getenv('SYNC_EXPORT_ENABLED', 'False') == 'True'
SYNC_IMPORT_ENABLED = os.getenv('SYNC_IMPORT_ENABLED', 'True') == 'True'

# 外网只读模式
READ_ONLY_MODE = os.getenv('READ_ONLY_MODE', 'True') == 'True'

# 禁用的模块路由
DISABLED_ROUTES = os.getenv('DISABLED_ROUTES', 'documents,zip-files').split(',')

# 项目外网可见强制开关（保持与内网导出逻辑一致）
ALWAYS_EXTERNAL_VISIBLE = os.getenv('ALWAYS_EXTERNAL_VISIBLE', 'True') == 'True'

