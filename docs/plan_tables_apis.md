# plan.plan.md 对照：数据表 & API 清单

## 数据表（规划）
- Project：基础信息、外网展示状态、进度百分比、外网可见性
- Milestone：里程碑（含外网展示/进度/可见性）
- ProjectMemberPermission：成员权限（view/download/upload/modify/delete）、状态、有效期、职位
- MemberJoinApproval：成员加入审批（用户申请 / 管理员邀请，双状态）
- Document：文件（分类、版本链、标签、审批、MinIO 路径、项目、审批人/状态等）
- DocumentTag / DocumentTagRelation：标签与关联
- DocumentApproval：文件审批
- ZipSpatialData：ZIP 地理数据补充信息（描述、envelope）
- DocumentCrossDeptReference：跨部门文件引用审批
- Department：部门（层级、负责人等）
- User（扩展字段：role、department_id 等）
- OperationLog：操作/审计日志
- Notification：通知
- （同步可选）如无专表则在业务逻辑中处理导入/导出

## API（规划，均以 `/api/v1/` 开头）

### 项目 & 进度
- GET/POST/PUT/DELETE `/projects/`
- GET `/projects/{id}/`
- PATCH `/projects/{id}/status/`
- PATCH `/projects/{id}/progress/`
- PATCH `/projects/{id}/external-visibility/`

### 里程碑
- GET/POST `/projects/{id}/milestones/`
- PUT/DELETE `/milestones/{id}/`
- PATCH `/milestones/{id}/complete/`

### 项目成员与权限
- GET/POST `/projects/{id}/members/`
- DELETE `/projects/{id}/members/{user_id}/`
- POST `/projects/{id}/members/batch-remove/`
- PATCH `/projects/{id}/members/{user_id}/permissions/`

### 成员加入审批
- POST `/projects/{id}/members/apply/`
- POST `/projects/{id}/members/invite/`
- GET `/projects/{id}/members/approvals/`
- POST `/member-approvals/{id}/approve/`
- POST `/member-approvals/{id}/reject/`
- POST `/member-approvals/{id}/remind/`

### 文件（documentManager）
- 上传/下载/预览：POST `/documents/upload/`；GET `/documents/{id}/download/`；GET `/documents/{id}/preview/`
- 文件 CRUD：GET `/projects/{id}/documents/`；GET/PATCH/DELETE `/documents/{id}/`
- 版本：GET `/documents/{id}/versions/`；GET `/documents/{id}/versions/compare/`；POST `/documents/{id}/rollback/`
- 标签：GET/POST `/tags/`；POST `/documents/{id}/tags/`；DELETE `/documents/{id}/tags/{tag_id}/`
- 审批：POST `/documents/{id}/approve/`；GET `/documents/{id}/approval-history/`

### ZIP 地理数据（zipManager）
- POST `/projects/{id}/zip-files/upload/`
- GET `/projects/{id}/zip-files/`
- GET `/zip-files/{id}/download/`
- POST `/zip-files/{id}/validate/`
- GET `/zip-files/{id}/contents/`

### 跨部门文件引用
- POST `/documents/{id}/cross-dept-reference/apply/`
- GET `/documents/cross-dept-references/`
- GET `/document-references/{id}/`
- POST `/document-references/{id}/approve/`
- POST `/document-references/{id}/reject/`
- DELETE `/document-references/{id}/`

### 部门（team）
- GET/POST `/departments/`
- PUT `/departments/{id}/`
- DELETE `/departments/{id}/`
- POST `/departments/{id}/transfer/`
- POST `/departments/merge/`
- POST `/departments/{id}/dissolve/`
- GET `/departments/{id}/members/`

### 用户
- GET `/users/`
- GET `/users/{id}/`
- POST `/users/`
- PUT `/users/{id}/`
- DELETE `/users/{id}/`
- PATCH `/users/{id}/role/`
- PATCH `/users/{id}/status/`
- GET `/users/me/`
- PATCH `/users/me/password/`
- GET `/users/{id}/projects/`

### 日志 / 通知
- 日志：GET `/logs/`；GET `/logs/{id}/`；GET `/logs/export/`；GET `/logs/statistics/`
- 通知：GET `/notifications/`；GET `/notifications/unread-count/`；GET `/notifications/{id}/`；PATCH `/notifications/{id}/read/`；POST `/notifications/batch-read/`；DELETE `/notifications/{id}/`

### 聚合 / 搜索
- GET `/dashboard/overview/`
- GET `/search/`
- GET `/projects/{id}/summary/`

### 数据同步（内外网）
- 内网：POST `/admin/sync/export/`
- 外网：POST `/admin/sync/import/`

### 环境控制 / 只读
- 外网屏蔽 document/zip 路由；只读模式拦截写操作（除导入）


