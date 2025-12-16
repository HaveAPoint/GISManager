# plan.plan.md 对照：业务需求 → 表/接口映射

## 项目与进度 / 里程碑
- 业务：项目生命周期、进度条、外网可见性/展示状态、里程碑管理
- 表：Project（external_display_status, progress_percent, is_external_visible）、Milestone
- API：项目 CRUD + PATCH `/status/` `/progress/` `/external-visibility/`；里程碑 CRUD/complete

## 项目成员与权限 / 临时权限
- 业务：成员增删改、批量移除、权限（view/download/upload/modify/delete）、有效期
- 表：ProjectMemberPermission（permissions JSONB、valid_from/valid_to、status、position）
- API：成员 CRUD、batch-remove、PATCH `/permissions/`

## 成员加入审批（双路径）
- 业务：用户申请 / 管理员邀请，两条审批链
- 表：MemberJoinApproval（join_type，admin_approval_status，user_approval_status）
- API：apply/invite/approvals/approve/reject/remind

## 文件管理（普通文档）
- 业务：上传/下载/预览/删除，版本历史、回滚，标签，审批，分类（招投标/合同/成果/过程/原始/交接/zip）
- 表：Document（分类、版本链 parent_version_id、tags/related_files JSONB、approval、MinIO 路径、项目、审批人/状态等），DocumentTag/Relation，DocumentApproval
- API：上传/下载/预览，文件 CRUD，版本列表/对比/回滚，标签 CRUD，审批接口

## ZIP 地理数据
- 业务：ZIP 上传/下载/校验/列目录，可存空间范围
- 表：Document（file_type=zip），ZipSpatialData（description, envelope）
- API：zip upload/list/download/validate/contents

## 跨部门文件引用审批
- 业务：跨部门引用申请/审批/撤销
- 表：DocumentCrossDeptReference
- API：apply/list/detail/approve/reject/delete

## 部门/团队管理
- 业务：部门 CRUD、移交/合并/解散、成员列表
- 表：Department
- API：部门 CRUD + transfer/merge/dissolve；members 列表

## 用户管理
- 业务：用户 CRUD、角色/状态调整、当前用户、自身项目列表、改密码
- 表：User（扩展 role、department_id 等）
- API：用户 CRUD、PATCH role/status、`/users/me/`、`/users/me/password/`、`/users/{id}/projects/`

## 日志 / 通知
- 业务：操作/审计日志，通知与未读数
- 表：OperationLog、Notification
- API：日志列表/详情/导出/统计；通知列表/未读数/详情/已读/批量已读/删除

## 聚合 / 搜索 / 概览
- 业务：仪表盘概览、全局搜索、项目汇总
- API：`/dashboard/overview/`、`/search/`、`/projects/{id}/summary/`

## 内外网隔离与只读
- 业务：外网只读、禁用文件上传/下载，屏蔽 document/zip 路由；账号同源但外网受限
- 配置/中间件：ENVIRONMENT=INTRANET/EXTRANET，DISABLED_ROUTES，READ_ONLY_MODE，EnvironmentRoutingMiddleware
- 外网暴露：项目只读、用户 me、同步导入等；内网全量

## 数据同步（内外网摆渡）
- 业务：内网导出可见项目进度 JSON，外网导入更新进度
- 服务/逻辑：DataSyncService export/import
- API：内网 `/admin/sync/export/`；外网 `/admin/sync/import/`

## 认证与安全
- 业务：JWT 认证；开发环境 Swagger；CORS/ALLOWED_HOSTS 按前端域名配置
- 配置：SIMPLE_JWT，Swagger DEBUG 开启，CORS_ALLOWED_ORIGINS，ALLOWED_HOSTS

