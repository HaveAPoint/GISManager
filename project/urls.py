from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectMemberPermissionViewSet, MemberJoinApprovalViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
# 这里的路由比较特殊，因为 ProjectMemberPermissionViewSet 是针对单个成员的操作，
# 但通常我们通过 /projects/{id}/members/{user_id}/ 来操作。
# 为了简化，我们这里先注册一个扁平的路由，或者依赖 ProjectViewSet 的子路由。
# 根据 plan.md: DELETE /api/v1/projects/{id}/members/{user_id}/
# 这需要嵌套路由或者自定义 lookup。
# 暂时我们注册一个辅助路由，或者在 ProjectViewSet 中处理。
# 鉴于 DRF 的限制，我们这里注册 member-approvals
router.register(r'member-approvals', MemberJoinApprovalViewSet)

# 对于 /projects/{id}/members/{user_id}/ 这种深层嵌套，
# 我们可以使用 drf-nested-routers，或者手动写 path。
# 这里为了简单，我们手动添加一些 path 到 urlpatterns

urlpatterns = [
    path('', include(router.urls)),
    # 手动添加成员移除和权限更新的路由，映射到 ProjectMemberPermissionViewSet
    # 注意：这里的 pk 实际上是 ProjectMemberPermission 的 ID，或者我们需要通过 project_id 和 user_id 查找
    # 根据 plan.md: DELETE /api/v1/projects/{id}/members/{user_id}/
    # 我们可以在 ProjectViewSet 中实现这个 delete 动作
]
