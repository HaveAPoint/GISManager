from django.shortcuts import render
from rest_framework import viewsets, status, decorators, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Department
from .serializers import (
    DepartmentSerializer, DepartmentCreateUpdateSerializer,
    UserSerializer, UserCreateUpdateSerializer,
    LoginSerializer, ChangePasswordSerializer,
    DepartmentTransferSerializer, DepartmentMergeSerializer,
    DepartmentAddMemberSerializer
)

User = get_user_model()

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门管理接口
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentCreateUpdateSerializer
        return DepartmentSerializer

    @swagger_auto_schema(
        method='get',
        operation_description="获取部门成员列表",
        responses={200: UserSerializer(many=True)}
    )
    @swagger_auto_schema(
        method='post',
        operation_description="添加部门成员",
        request_body=DepartmentAddMemberSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['get', 'post'], url_path='members')
    def members(self, request, pk=None):
        department = self.get_object()
        if request.method == 'POST':
            serializer = DepartmentAddMemberSerializer(data=request.data)
            if serializer.is_valid():
                user_ids = serializer.validated_data['user_ids']
                users = User.objects.filter(id__in=user_ids)
                users.update(department=department)
                return Response({"message": "Members added successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        members = User.objects.filter(department=department)
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="移除部门成员",
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['delete'], url_path='members/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        department = self.get_object()
        try:
            user = User.objects.get(id=user_id, department=department)
            user.department = None
            user.save()
            return Response({"message": "Member removed successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found in this department"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="移交团队（变更部门负责人）",
        request_body=DepartmentTransferSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        # TODO: Implement transfer logic
        return Response({"message": "Transfer logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="合并团队",
        request_body=DepartmentMergeSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=False, methods=['post'])
    def merge(self, request):
        # TODO: Implement merge logic
        return Response({"message": "Merge logic not implemented yet"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="解散团队",
        responses={200: "Success"}
    )
    @decorators.action(detail=True, methods=['post'])
    def dissolve(self, request, pk=None):
        # TODO: Implement dissolve logic
        return Response({"message": "Dissolve logic not implemented yet"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理接口
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(
        operation_description="修改密码",
        request_body=ChangePasswordSerializer,
        responses={200: "Success"}
    )
    @decorators.action(detail=False, methods=['post'])
    def change_password(self, request):
        # TODO: Implement change password logic
        return Response({"message": "Change password logic not implemented yet"}, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ViewSet):
    """
    认证接口
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="用户登录，返回 JWT Token",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                '登录成功',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Access Token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Refresh Token'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='用户信息')
                    }
                )
            ),
            400: '用户名或密码错误'
        }
    )
    @decorators.action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                # 生成 JWT Token
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="刷新 JWT Token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh Token')
            }
        ),
        responses={
            200: openapi.Response(
                '刷新成功',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='新的 JWT Access Token')
                    }
                )
            ),
            400: 'Token 无效'
        }
    )
    @decorators.action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def refresh(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="用户登出（JWT 无状态，客户端删除 token 即可）",
        responses={200: "Success"}
    )
    @decorators.action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        # JWT 是无状态的，客户端删除 token 即可
        # 如果需要服务端黑名单功能，可以在这里实现 token 黑名单
        return Response({"message": "Logged out successfully"})

    @swagger_auto_schema(
        operation_description="获取当前用户信息",
        responses={200: UserSerializer}
    )
    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
