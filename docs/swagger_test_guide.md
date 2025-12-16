# Swagger 测试指南

## 📋 已完成的工作

### ✅ 第一步：依赖安装
- `drf_yasg` 已在 `INSTALLED_APPS` 中配置

### ✅ 第二步：基础配置
- `SWAGGER_SETTINGS` 已配置（包含 JWT 认证）
- Swagger 路由已配置在 `config/urls.py`

### ✅ 第三步：创建示例 API
- 创建了 `api/gateway/views.py`，包含两个示例接口：
  - `/api/v1/health/` - 健康检查接口
  - `/api/v1/info/` - API 信息接口

### ✅ 第四步：路由配置
- 在 `api/gateway/urls.py` 中注册了示例接口

---

## 🚀 第六步：测试 Swagger

### 1. 启动开发服务器

```bash
# 激活虚拟环境（如果使用）
source venv/bin/activate

# 启动 Django 开发服务器
python manage.py runserver
```

服务器将在 `http://127.0.0.1:8000` 启动

### 2. 访问 Swagger UI

打开浏览器，访问以下地址：

#### Swagger UI（推荐）
```
http://127.0.0.1:8000/swagger/
```

#### ReDoc（备选）
```
http://127.0.0.1:8000/redoc/
```

#### JSON Schema（用于集成）
```
http://127.0.0.1:8000/swagger.json
```

#### YAML Schema（用于集成）
```
http://127.0.0.1:8000/swagger.yaml
```

### 3. 在 Swagger UI 中测试 API

#### 3.1 查看 API 文档
- 打开 Swagger UI 后，你会看到：
  - **系统** 标签下有两个接口：
    - `GET /api/v1/health/` - 健康检查
    - `GET /api/v1/info/` - API 信息

#### 3.2 测试接口
1. 点击任意接口展开详情
2. 点击 **"Try it out"** 按钮
3. 点击 **"Execute"** 执行请求
4. 查看响应结果

#### 3.3 测试健康检查接口
- 接口路径：`GET /api/v1/health/`
- 无需认证（`AllowAny` 权限）
- 预期响应：
```json
{
  "status": "ok",
  "message": "API 服务运行正常"
}
```

#### 3.4 测试 API 信息接口
- 接口路径：`GET /api/v1/info/`
- 无需认证（`AllowAny` 权限）
- 预期响应：
```json
{
  "version": "v1",
  "name": "GIS文件管理系统 API",
  "description": "GIS文件管理系统的 RESTful API 接口"
}
```

### 4. 测试 JWT 认证（当有需要认证的接口时）

1. 在 Swagger UI 右上角点击 **"Authorize"** 按钮
2. 在弹出的对话框中：
   - 在 **Value** 输入框中输入：`Bearer <your_jwt_token>`
   - 例如：`Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. 点击 **"Authorize"** 确认
4. 点击 **"Close"** 关闭对话框
5. 现在所有需要认证的接口都会自动携带这个 Token

---

## 📝 验证清单

- [ ] 能够访问 `http://127.0.0.1:8000/swagger/`
- [ ] 能看到 "GIS文件管理系统 API" 标题
- [ ] 能看到 "系统" 标签
- [ ] 能看到两个接口：`/api/v1/health/` 和 `/api/v1/info/`
- [ ] 能够成功执行健康检查接口
- [ ] 能够成功执行 API 信息接口
- [ ] 响应格式符合预期

---

## 🎯 下一步：为你的 API 添加 Swagger 文档

当你创建新的 API 视图时，参考以下模式：

### 示例：函数视图

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response

@swagger_auto_schema(
    method='get',
    operation_summary="接口摘要",
    operation_description="接口详细描述",
    responses={
        200: openapi.Response(description="成功响应"),
    },
    tags=['标签名']
)
@api_view(['GET'])
def my_view(request):
    return Response({'data': 'example'})
```

### 示例：ViewSet

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets

class MyViewSet(viewsets.ModelViewSet):
    """
    视图集文档字符串
    """
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    
    @swagger_auto_schema(
        operation_summary="获取列表",
        tags=['我的模块']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

---

## ❓ 常见问题

### Q: 访问 `/swagger/` 显示 404？
**A:** 确保 `settings.DEBUG = True`，Swagger 路由只在 DEBUG 模式下启用。

### Q: Swagger 页面空白或加载失败？
**A:** 
1. 检查 `drf_yasg` 是否已安装：`pip list | grep drf-yasg`
2. 检查浏览器控制台是否有错误
3. 尝试清除浏览器缓存

### Q: 接口没有出现在 Swagger 中？
**A:**
1. 确保视图已正确注册到 URL 路由
2. 确保视图继承自 `APIView` 或使用 `@api_view` 装饰器
3. 检查是否有语法错误：`python manage.py check`

### Q: 如何添加更多 API 信息（联系方式、许可证等）？
**A:** 编辑 `config/urls.py` 中的 `openapi.Info` 对象，取消注释并填写相应字段。

---

## 📚 参考资源

- [drf-yasg 官方文档](https://drf-yasg.readthedocs.io/)
- [OpenAPI 规范](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

