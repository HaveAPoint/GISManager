## GISManager 本地开发启动指南

### 环境要求
- Ubuntu/WSL，PostgreSQL 16
- PostGIS（`postgis`, `postgresql-16-postgis-3`, `postgresql-16-postgis-3-scripts`）
- Python 3.12，已创建虚拟环境 `venv`

### 一次性准备
1. 安装 PostGIS：
   ```bash
   sudo apt update
   sudo apt install postgis postgresql-16-postgis-3 postgresql-16-postgis-3-scripts
   ```
2. 确保数据库和角色存在（如需）：
   ```bash
   sudo -u postgres psql -c "CREATE ROLE gis_user LOGIN PASSWORD 'gis_password';"
   sudo -u postgres psql -c "CREATE DATABASE gis_manager OWNER gis_user;"
   sudo -u postgres psql -d gis_manager -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```
3. 在项目根目录创建 `.env`（不要提交到仓库）：
   ```bash
   cat > .env <<'EOF'
   DB_NAME=gis_manager
   DB_USER=gis_user
   DB_PASSWORD=gis_password
   DB_HOST=localhost
   DB_PORT=5433
   USE_POSTGIS=True
   EOF
   ```

### 每次开机/开发会话
1. 启动 PostgreSQL（如果未自动启动）：
   ```bash
   sudo systemctl start postgresql
   ```
2. 进入项目并激活虚拟环境、加载环境变量：
   ```bash
   cd /home/crh/company/projdatamanage/backend/GISManager
   source venv/bin/activate
   source .env
   ```
3. 运行迁移（仅当模型有变更时）：
   ```bash
   python manage.py migrate
   ```
4. （可选）生成测试数据（用于前端开发和测试）：
   ```bash
   python manage.py create_test_data
   # 或清除后重新生成：
   python manage.py create_test_data --clear
   ```
   这会创建：
   - 4 个测试部门（技术部、市场部、财务部、人事部）
   - 3 个测试用户（testuser1, testuser2, manager1，密码都是 `test123456`）
   - 5 个测试项目
   - 项目成员关系
   - 测试文档（mock 数据，只有数据库记录，没有真实文件）
5. 启动开发服务：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### 快捷命令（可选）
可在 `~/.bashrc` 追加：
```bash
alias pgstart="sudo systemctl start postgresql"
proj_gis() {
  cd /home/crh/company/projdatamanage/backend/GISManager || return
  source venv/bin/activate
  [ -f .env ] && source .env
  echo "env loaded. run: python manage.py runserver"
}
```
使用：
- `pgstart` 启动数据库
- `proj_gis` 进入项目并加载环境

### 前端接入说明

#### API 基础信息
- **Base URL**: `http://localhost:8000/api/v1/`
- **Swagger UI**: `http://localhost:8000/swagger/`
- **认证方式**: JWT Bearer Token

#### 快速开始
1. **登录获取 Token**：
   - 调用 `POST /api/v1/auth/login/`，传入用户名和密码
   - 返回格式：
     ```json
     {
       "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
       "user": { ... }
     }
     ```
   - 保存 `access` token

2. **使用 Token**：
   - 在请求头中添加：`Authorization: Bearer <your_access_token>`
   - 在 Swagger UI 中，点击右上角 "Authorize" 按钮，输入：`Bearer <your_access_token>`

3. **测试账号**（运行 `create_test_data` 后可用）：
   - `testuser1` / `test123456`
   - `testuser2` / `test123456`
   - `manager1` / `test123456`

#### 主要接口模块
- **认证**: `/api/v1/auth/login/`, `/api/v1/auth/logout/`, `/api/v1/auth/me/`, `/api/v1/auth/refresh/`
- **用户管理**: `/api/v1/users/`, `/api/v1/departments/`
- **项目管理**: `/api/v1/projects/`
- **文档管理**: `/api/v1/documents/`

### 常见问题
- 报 `password authentication failed for user "gis_user"`：确认 `.env` 中密码与数据库一致，可用 `PGPASSWORD=... psql -h localhost -p 5433 -U gis_user -d gis_manager` 测试。
- 报 `extension "postgis" is not available`：确认已安装 PostGIS 包，并执行 `CREATE EXTENSION IF NOT EXISTS postgis;`。
- Swagger 中看不到 "Authorize" 按钮：确保 `SWAGGER_SETTINGS` 中配置了 `SECURITY_DEFINITIONS`，并且接口有 `permission_classes=[permissions.IsAuthenticated]`。

## 给同事的使用说明

本项目不提供现成的数据库文件，每个开发者在本机按以下步骤自建数据库环境。下述内容与前文“本地开发启动指南”一致，这里是给协作同事的简版 checklist。

### 1. 克隆代码并准备环境

```bash
git clone <repo-url>
cd backend/GISManager

# 推荐创建并激活虚拟环境（如已有可跳过）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # 如果存在
```

### 2. 准备 PostgreSQL + PostGIS

在本机（或统一的开发数据库）安装 PostgreSQL 16 和 PostGIS（如前文所述）：

```bash
sudo apt update
sudo apt install postgis postgresql-16-postgis-3 postgresql-16-postgis-3-scripts

sudo -u postgres psql -c "CREATE ROLE gis_user LOGIN PASSWORD 'gis_password';"
sudo -u postgres psql -c "CREATE DATABASE gis_manager OWNER gis_user;"
sudo -u postgres psql -d gis_manager -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### 3. 配置本地环境变量（每个人都有自己的 `.env`）

在项目根目录创建 `.env`（不要提交到 Git）：

```bash
cat > .env <<'EOF'
DB_NAME=gis_manager
DB_USER=gis_user
DB_PASSWORD=gis_password
DB_HOST=localhost
DB_PORT=5433
USE_POSTGIS=True
EOF
```

### 4. 初始化数据库结构 + 测试数据

```bash
cd backend/GISManager
source venv/bin/activate
source .env

# 创建表结构
python manage.py migrate

# 生成测试数据（部门 / 用户 / 项目 / 文档）
python manage.py create_test_data
# 如需清空并重建：
# python manage.py create_test_data --clear
```

生成的测试账号（仅用于开发环境）：

- `testuser1` / `test123456`
- `testuser2` / `test123456`
- `manager1` / `test123456`

也可以自行创建超级管理员账号：

```bash
python manage.py createsuperuser
```

### 5. 启动服务与测试接口

```bash
python manage.py runserver 0.0.0.0:8000
```

- Swagger UI: `http://localhost:8000/swagger/`
- API Base URL: `http://localhost:8000/api/v1/`

登录流程：

1. 调用 `POST /api/v1/auth/login/` 获取 `access` / `refresh` token；
2. 在 Swagger 右上角点击 “Authorize”，输入：`Bearer <access_token>`；
3. 之后即可调用需要认证的接口（如 `/api/v1/auth/me/`、项目 / 文档等）。