from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'manager', 'manager_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DepartmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'code', 'manager']

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'gender', 'position', 'department', 'department_name',
            'role', 'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name',
            'phone', 'gender', 'position', 'department', 'role', 'is_active'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

class DepartmentTransferSerializer(serializers.Serializer):
    target_manager_id = serializers.UUIDField(help_text="新负责人的ID")

class DepartmentMergeSerializer(serializers.Serializer):
    source_department_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="要合并的部门ID列表"
    )
    target_department_name = serializers.CharField(help_text="合并后的新部门名称")
    target_department_code = serializers.CharField(help_text="合并后的新部门编号")
    manager_id = serializers.UUIDField(help_text="新部门负责人ID", required=False)

class DepartmentAddMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        help_text="List of User IDs to add to the department"
    )
