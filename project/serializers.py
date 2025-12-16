from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, ProjectMemberPermission, MemberJoinApproval
from userManager.serializers import UserSerializer

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'code', 'description', 'manager', 'manager_name',
            'department', 'department_name', 'status', 'start_date', 'end_date',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'code', 'description', 'manager', 'department',
            'status', 'start_date', 'end_date'
        ]

class ProjectMemberPermissionSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = ProjectMemberPermission
        fields = [
            'id', 'user', 'user_info', 'project', 'project_name',
            'permission_status', 'position', 'permissions',
            'valid_from', 'valid_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProjectMemberAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMemberPermission
        fields = ['user', 'position', 'permissions', 'valid_to']

class ProjectMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMemberPermission
        fields = ['position', 'permissions', 'valid_to', 'permission_status']

class MemberJoinApprovalSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    admin_approver_name = serializers.CharField(source='admin_approver.get_full_name', read_only=True)
    
    class Meta:
        model = MemberJoinApproval
        fields = [
            'id', 'user', 'user_name', 'project', 'project_name',
            'join_type', 'admin_approval_status', 'user_approval_status',
            'admin_approval_time', 'user_approval_time',
            'admin_approver', 'admin_approver_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'admin_approval_time', 'user_approval_time',
            'admin_approver', 'created_at', 'updated_at'
        ]

class MemberApplySerializer(serializers.Serializer):
    project_id = serializers.UUIDField(help_text="申请加入的项目ID")

class MemberInviteSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(help_text="邀请的用户ID")

class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, help_text="审批意见")

class BatchRemoveMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="要移除的用户ID列表"
    )
