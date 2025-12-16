import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 根据环境变量选择配置
ENVIRONMENT = os.getenv('ENVIRONMENT', 'INTRANET').upper()

if ENVIRONMENT == 'EXTRANET':
    from .extranet import *
else:
    from .intranet import *

