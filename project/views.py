from rest_framework import viewsets, status, decorators, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Project, ProjectMemberPermission, MemberJoinApproval
from .serializers import (
    ProjectSerializer, ProjectCreateUpdateSerializer,
    ProjectMemberPermissionSerializer, ProjectMemberAddSerializer,
    ProjectMemberUpdateSerializer, MemberJoinApprovalSerializer,
    MemberApplySerializer, MemberInviteSerializer,
    ApprovalActionSerializer, BatchRemoveMemberSerializer
)
from documentManager.models import Document
from documentManager.serializers import DocumentSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    项目管理接口
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        operation_description="更新项目状态",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['approval', 'bidding', 'implementation', 'delivery', 'completion', 'archived'])
            },
            required=['status']
        ),
        responses={200: ProjectSerializer}
    )
    @decorators.action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        # TODO: Implement status update logic
        return Response({"message": "Status update logic not implemented yet"}, status=status.HTTP_200_OK)

    # --- 成员管理相关接口 ---

    @swagger_auto_schema(
        operation_description="获取项目成员列表",
        responses={200: ProjectMemberPermissionSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        project = self.get_object()
        members = ProjectMemberPermission.objects.filter(project=project)
        serializer = ProjectMemberPermissionSerializer(members, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="获取项目文件列表",
        responses={200: DocumentSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'], url_path='documents')
    def documents(self, request, pk=None):
        project = self.get_object()
        docs = Document.objects.filter(project=project)
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="添加项目成员",
        request_body=ProjectMemberAddSerializer,
        responses={201: ProjectMemberPermissionSerializer}
    )
    @members.mapping.post
    def add_member(self, request, pk=None):
        # TODO: Implement add member logic
        return Response({"message": "Add member logic not implemented yet"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="批量移除成员",
        request_body=BatchRemoveMemberSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'], url_path='members/batch-remove')
    def batch_remove_members(self, request, pk=None):
        # TODO: Implement batch remove logic
        return Response({"message": "Batch remove logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="用户申请加入项目",
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'], url_path='members/apply')
    def apply_join(self, request, pk=None):
        # TODO: Implement apply join logic
        return Response({"message": "Apply join logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="邀请成员加入项目",
        request_body=MemberInviteSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'], url_path='members/invite')
    def invite_member(self, request, pk=None):
        # TODO: Implement invite member logic
        return Response({"message": "Invite member logic not implemented yet"}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="移除项目成员",
        responses={204: "Success"}
    )
    @decorators.action(detail=True, methods=['delete'], url_path='members/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        # TODO: Implement remove member logic
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="更新成员权限",
        request_body=ProjectMemberUpdateSerializer,
        responses={200: ProjectMemberPermissionSerializer}
    )
    @decorators.action(detail=True, methods=['patch'], url_path='members/(?P<user_id>[^/.]+)/permissions')
    def update_member_permissions(self, request, pk=None, user_id=None):
        # TODO: Implement update permissions logic
        return Response({"message": "Update permissions logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="获取成员加入审批列表",
        responses={200: MemberJoinApprovalSerializer(many=True)}
    )
    @decorators.action(detail=True, methods=['get'], url_path='members/approvals')
    def member_approvals(self, request, pk=None):
        # TODO: Implement get approvals logic
        return Response([], status=status.HTTP_200_OK)


class ProjectMemberPermissionViewSet(viewsets.ModelViewSet):
    """
    项目成员权限管理 (针对单个成员的操作)
    """
    queryset = ProjectMemberPermission.objects.all()
    serializer_class = ProjectMemberPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['delete', 'patch'] # 只允许删除和更新权限

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return ProjectMemberUpdateSerializer
        return ProjectMemberPermissionSerializer

    @swagger_auto_schema(
        operation_description="更新成员权限",
        request_body=ProjectMemberUpdateSerializer,
        responses={200: ProjectMemberPermissionSerializer}
    )
    @decorators.action(detail=True, methods=['patch'], url_path='permissions')
    def update_permissions(self, request, pk=None):
        # TODO: Implement update permissions logic
        return Response({"message": "Update permissions logic not implemented yet"}, status=status.HTTP_200_OK)


class MemberJoinApprovalViewSet(viewsets.ModelViewSet):
    """
    成员加入审批处理接口
    """
    queryset = MemberJoinApproval.objects.all()
    serializer_class = MemberJoinApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post'] # 只允许POST操作

    @swagger_auto_schema(
        operation_description="审批通过",
        request_body=ApprovalActionSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        # TODO: Implement approve logic
        return Response({"message": "Approve logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="审批驳回",
        request_body=ApprovalActionSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        # TODO: Implement reject logic
        return Response({"message": "Reject logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="催办",
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'])
    def remind(self, request, pk=None):
        # TODO: Implement remind logic
        return Response({"message": "Remind logic not implemented yet"}, status=status.HTTP_200_OK)
