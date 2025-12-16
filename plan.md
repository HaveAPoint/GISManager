## 七、技术实现要点

### 7.1 数据库设计

#### 7.1.1 核心表结构

**项目表（Project）**
```sql
- id: UUID (主键)
- name: VARCHAR(200) (项目名称，必填)
- code: VARCHAR(50) (项目编号，唯一)
- description: TEXT (项目描述)
- manager_id: UUID (项目负责人ID，外键 → User.id)
- department_id: UUID (所属部门ID，外键 → Department.id)
- status: VARCHAR(20) (项目状态：approval/bidding/implementation/delivery/completion/archived，默认approval)
- start_date: DATE (项目开始时间，可为NULL)
- end_date: DATE (项目结束时间，可为NULL)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- created_by_id: UUID (创建人ID，外键 → User.id)
- is_deleted: BOOLEAN (软删除标记，默认False)
- 索引：(status)
- 注：code 的唯一约束会自动创建索引；manager_id、department_id、created_by_id 的外键会自动创建索引
```

**项目成员权限表（ProjectMemberPermission）**
```sql
- id: UUID (主键)
- user_id: UUID (用户ID，外键 → User.id)
- project_id: UUID (项目ID，外键 → Project.id)
- permission_status: VARCHAR(20) (权限状态：active/disabled/pending，默认active)
- position: VARCHAR(50) (项目内职位，默认'项目成员')
- permissions: JSONB (权限操作类型：["view", "download", "upload", "modify", "delete"]，默认[])
- valid_from: TIMESTAMP (有效期开始时间，自动添加)
- valid_to: TIMESTAMP (有效期结束时间，可为NULL表示永久)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- 唯一约束：(user_id, project_id)
- 索引：(user_id), (project_id), (user_id, project_id, permission_status)
```

**文件表（Document）**
```sql
- id: UUID (主键)
- name: VARCHAR(200) (文件名称，必填)
- original_name: VARCHAR(200) (原始文件名)
- file_type: VARCHAR(20) (文件类型：document/zip)
- category: VARCHAR(50) (文件分类：bidding/contract/achievement/process/original/handover)
- minio_path: VARCHAR(500) (MinIO存储路径)
- minio_bucket: VARCHAR(100) (MinIO存储桶)
- file_size: BIGINT (文件大小，字节)
- mime_type: VARCHAR(100) (MIME类型，可为空)
- version: INTEGER (版本号，默认1)
- parent_version_id: UUID (父版本ID，外键 → Document.id，用于版本链，可为NULL)
- project_id: UUID (所属项目ID，外键 → Project.id)
- uploader_id: UUID (上传人ID，外键 → User.id)
- approver_id: UUID (审批人ID，外键 → User.id，可为NULL)
- approval_status: VARCHAR(20) (审批状态：pending/approved/rejected，默认pending)
- approval_time: TIMESTAMP (审批时间，可为NULL)
- tags: JSONB (文件标签数组，默认[])
- related_files: JSONB (关联文件ID数组，默认[])
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- is_deleted: BOOLEAN (软删除标记，默认False)
- 复合索引：(project_id, category), (uploader_id), (approval_status)
```

**成员加入审批表（MemberJoinApproval）**
```sql
- id: UUID (主键)
- user_id: UUID (申请/被邀请用户ID，外键 → User.id)
- project_id: UUID (项目ID，外键 → Project.id)
- join_type: VARCHAR(20) (加入类型：user_apply/admin_invite)
- admin_approval_status: VARCHAR(20) (管理员审批状态：pending/approved/rejected)
- user_approval_status: VARCHAR(20) (用户确认状态：pending/approved/rejected)
- admin_approval_time: TIMESTAMP (管理员审批时间)
- user_approval_time: TIMESTAMP (用户确认时间)
- admin_approver_id: UUID (管理员审批人ID，外键 → User.id)
- created_at: TIMESTAMP (创建时间)
- updated_at: TIMESTAMP (更新时间)
- 索引：(user_id, project_id), (admin_approval_status, user_approval_status)
```

**文件审批表（DocumentApproval）**
```sql
- id: UUID (主键)
- document_id: UUID (文件ID，外键 → Document.id)
- approver_id: UUID (审批人ID，外键 → User.id)
- approval_status: VARCHAR(20) (审批状态：pending/approved/rejected，默认pending)
- approval_comment: TEXT (审批意见，可为空)
- approval_time: TIMESTAMP (审批时间，可为NULL)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- 索引：(document_id), (approver_id, approval_status)
```

**文件标签表（DocumentTag）**
```sql
- id: UUID (主键)
- name: VARCHAR(50) (标签名称，唯一)
- description: TEXT (标签描述，可为空)
- color: VARCHAR(20) (标签颜色，用于UI显示，可为空)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- 唯一约束：name
```

**文件标签关联表（DocumentTagRelation）**
```sql
- id: UUID (主键)
- document_id: UUID (文件ID，外键 → Document.id)
- tag_id: UUID (标签ID，外键 → DocumentTag.id)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- 唯一约束：(document_id, tag_id)
```

#### 7.1.2 用户和部门表（userManager模块）

**用户表（User）**
```sql
- id: UUID (主键)
- username: VARCHAR(150) (用户名，唯一)
- password: VARCHAR(128) (密码哈希)
- email: VARCHAR(254) (邮箱，可为空)
- first_name: VARCHAR(150) (名，可为空)
- last_name: VARCHAR(150) (姓，可为空)
- is_staff: BOOLEAN (是否员工，默认False)
- is_active: BOOLEAN (是否激活，默认True)
- is_superuser: BOOLEAN (是否超级用户，默认False)
- date_joined: TIMESTAMP (加入时间)
- last_login: TIMESTAMP (最后登录时间，可为NULL)
- phone: VARCHAR(20) (电话号码，可为空)
- gender: VARCHAR(10) (性别：male/female/other，可为空)
- position: VARCHAR(50) (岗位，可为空)
- department_id: UUID (所属部门ID，外键 → Department.id，可为NULL)
- role: VARCHAR(20) (角色：super_admin/general_manager/dept_manager/employee，默认employee)
- last_operation_time: TIMESTAMP (最后操作时间，可为NULL)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- created_by_id: UUID (创建人ID，外键 → User.id，可为NULL)
- 索引：(department_id), (email)
- 注：继承自 Django AbstractUser，包含完整的认证功能
```

**部门表（Department）**
```sql
- id: UUID (主键)
- name: VARCHAR(100) (部门名称)
- code: VARCHAR(50) (部门编号，唯一)
- manager_id: UUID (部门负责人ID，外键 → User.id，可为NULL)
- created_at: TIMESTAMP (创建时间，自动添加)
- updated_at: TIMESTAMP (更新时间，自动更新)
- 注：公司只有一级部门，所有部门归总经理管理
```

### 7.2 API接口设计

#### 7.2.1 RESTful API规范

**基础URL**: `/api/v1/`

**统一响应格式**:
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**错误响应格式**:
```json
{
  "code": 400,
  "message": "错误描述",
  "errors": {
    "field_name": ["错误详情"]
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 7.2.2 项目管理接口（project模块）

**项目CRUD**
- `GET /api/v1/projects/` - 获取项目列表（支持分页、筛选、排序）
- `GET /api/v1/projects/{id}/` - 获取项目详情
- `POST /api/v1/projects/` - 创建项目
- `PUT /api/v1/projects/{id}/` - 更新项目信息
- `DELETE /api/v1/projects/{id}/` - 删除项目（软删除）
- `PATCH /api/v1/projects/{id}/status/` - 更新项目状态（生命周期）

**项目成员管理**
- `GET /api/v1/projects/{id}/members/` - 获取项目成员列表
- `POST /api/v1/projects/{id}/members/` - 添加项目成员
- `DELETE /api/v1/projects/{id}/members/{user_id}/` - 移除项目成员
- `POST /api/v1/projects/{id}/members/batch-remove/` - 批量移除成员
- `PATCH /api/v1/projects/{id}/members/{user_id}/permissions/` - 更新成员权限

**成员加入审批**
- `POST /api/v1/projects/{id}/members/apply/` - 用户申请加入项目
- `POST /api/v1/projects/{id}/members/invite/` - 项目负责人邀请成员
- `GET /api/v1/projects/{id}/members/approvals/` - 获取审批列表
- `POST /api/v1/member-approvals/{id}/approve/` - 审批通过
- `POST /api/v1/member-approvals/{id}/reject/` - 审批驳回
- `POST /api/v1/member-approvals/{id}/remind/` - 催办

#### 7.2.3 文件管理接口（documentManager模块）

**文件上传下载**
- `POST /api/v1/documents/upload/` - 上传文件
- `GET /api/v1/documents/{id}/download/` - 下载文件
- `GET /api/v1/documents/{id}/preview/` - 文件预览
- `DELETE /api/v1/documents/{id}/` - 删除文件

**文件管理**
- `GET /api/v1/projects/{id}/documents/` - 获取项目文件列表
- `GET /api/v1/documents/{id}/` - 获取文件详情
- `PATCH /api/v1/documents/{id}/` - 更新文件信息（名称、标签等）
- `GET /api/v1/documents/{id}/versions/` - 获取文件版本历史
- `POST /api/v1/documents/{id}/rollback/` - 版本回滚

**文件审批**
- `POST /api/v1/documents/{id}/approve/` - 审批文件
- `GET /api/v1/documents/{id}/approval-history/` - 获取审批历史

**文件标签**
- `GET /api/v1/tags/` - 获取标签列表
- `POST /api/v1/tags/` - 创建标签
- `POST /api/v1/documents/{id}/tags/` - 为文件添加标签
- `DELETE /api/v1/documents/{id}/tags/{tag_id}/` - 移除文件标签

#### 7.2.4 地理数据管理接口（zipManager模块）

- `POST /api/v1/projects/{id}/zip-files/upload/` - 上传zip文件
- `GET /api/v1/projects/{id}/zip-files/` - 获取项目zip文件列表
- `GET /api/v1/zip-files/{id}/download/` - 下载zip文件
- `POST /api/v1/zip-files/{id}/validate/` - 校验zip文件
- `GET /api/v1/zip-files/{id}/contents/` - 获取zip文件内容列表

#### 7.2.5 团队管理接口（userManager模块）

- `GET /api/v1/departments/` - 获取部门列表
- `POST /api/v1/departments/` - 创建部门
- `PUT /api/v1/departments/{id}/` - 更新部门
- `DELETE /api/v1/departments/{id}/` - 删除部门
- `POST /api/v1/departments/{id}/transfer/` - 移交团队
- `POST /api/v1/departments/merge/` - 合并团队
- `POST /api/v1/departments/{id}/dissolve/` - 解散团队
- `GET /api/v1/departments/{id}/members/` - 获取部门成员列表
- `POST /api/v1/departments/{id}/members/` - 添加部门成员
- `DELETE /api/v1/departments/{id}/members/{user_id}/` - 移除部门成员