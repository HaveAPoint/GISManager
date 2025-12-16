"""
生成测试数据的管理命令
用于前端开发和测试

使用方法：
    python manage.py create_test_data
    python manage.py create_test_data --clear  # 清除现有测试数据后重新创建
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from userManager.models import Department, User
from project.models import Project, ProjectMemberPermission
from documentManager.models import Document

User = get_user_model()


class Command(BaseCommand):
    help = '生成测试数据（部门、项目、文档等）用于前端开发和测试'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清除现有测试数据后重新创建',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始生成测试数据...'))
        
        if options['clear']:
            self.clear_test_data()
        
        # 1. 创建或获取部门
        departments = self.create_departments()
        
        # 2. 创建测试用户（如果不存在）
        users = self.create_test_users(departments)
        
        # 3. 创建项目
        projects = self.create_projects(users, departments)
        
        # 4. 创建项目成员关系
        self.create_project_members(projects, users)
        
        # 5. 创建文档（mock 数据）
        self.create_documents(projects, users)
        
        self.stdout.write(self.style.SUCCESS('\n✅ 测试数据生成完成！'))
        self.stdout.write(self.style.SUCCESS('\n📝 测试账号信息：'))
        self.stdout.write(self.style.WARNING('  用户名: testuser1, 密码: test123456'))
        self.stdout.write(self.style.WARNING('  用户名: testuser2, 密码: test123456'))
        self.stdout.write(self.style.WARNING('  用户名: manager1, 密码: test123456'))

    def clear_test_data(self):
        """清除测试数据"""
        self.stdout.write(self.style.WARNING('清除现有测试数据...'))
        
        # 删除测试文档（名称包含 "测试" 的）
        Document.objects.filter(name__contains='测试').delete()
        self.stdout.write('  - 已删除测试文档')
        
        # 删除测试项目（名称包含 "测试" 的）
        Project.objects.filter(name__contains='测试').delete()
        self.stdout.write('  - 已删除测试项目')
        
        # 注意：不删除用户和部门，因为它们可能被其他数据引用

    def create_departments(self):
        """创建测试部门"""
        self.stdout.write('\n📁 创建部门...')
        
        departments_data = [
            {'name': '技术部', 'code': 'TECH001'},
            {'name': '市场部', 'code': 'MARKET001'},
            {'name': '财务部', 'code': 'FINANCE001'},
            {'name': '人事部', 'code': 'HR001'},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'  ✅ 创建部门: {dept.name}')
            else:
                self.stdout.write(f'  ⏭️  部门已存在: {dept.name}')
        
        return departments

    def create_test_users(self, departments):
        """创建测试用户"""
        self.stdout.write('\n👥 创建测试用户...')
        
        users_data = [
            {
                'username': 'testuser1',
                'email': 'testuser1@example.com',
                'first_name': '测试',
                'last_name': '用户1',
                'role': 'employee',
                'department': departments[0] if departments else None,
            },
            {
                'username': 'testuser2',
                'email': 'testuser2@example.com',
                'first_name': '测试',
                'last_name': '用户2',
                'role': 'employee',
                'department': departments[1] if len(departments) > 1 else None,
            },
            {
                'username': 'manager1',
                'email': 'manager1@example.com',
                'first_name': '测试',
                'last_name': '经理',
                'role': 'dept_manager',
                'department': departments[0] if departments else None,
            },
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'role': user_data['role'],
                    'department': user_data['department'],
                    'is_active': True,
                }
            )
            if created:
                # 设置密码
                user.set_password('test123456')
                user.save()
                self.stdout.write(f'  ✅ 创建用户: {user.username} (密码: test123456)')
            else:
                self.stdout.write(f'  ⏭️  用户已存在: {user.username}')
            users.append(user)
        
        return users

    def create_projects(self, users, departments):
        """创建测试项目"""
        self.stdout.write('\n📋 创建项目...')
        
        project_names = [
            '测试项目-智慧城市GIS系统',
            '测试项目-地理信息数据管理平台',
            '测试项目-三维可视化系统',
            '测试项目-土地资源管理系统',
            '测试项目-环境监测平台',
        ]
        
        statuses = ['approval', 'bidding', 'implementation', 'delivery', 'completion']
        
        projects = []
        for i, name in enumerate(project_names):
            code = f'TEST{str(i+1).zfill(3)}'
            project, created = Project.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'description': f'{name}的详细描述，用于测试前端功能。',
                    'manager': users[2] if len(users) > 2 else users[0],  # manager1
                    'department': departments[0] if departments else None,
                    'status': statuses[i % len(statuses)],
                    'start_date': timezone.now().date() - timedelta(days=random.randint(30, 180)),
                    'end_date': timezone.now().date() + timedelta(days=random.randint(60, 365)),
                    'created_by': users[0],
                }
            )
            projects.append(project)
            if created:
                self.stdout.write(f'  ✅ 创建项目: {project.name} ({project.code})')
            else:
                self.stdout.write(f'  ⏭️  项目已存在: {project.name}')
        
        return projects

    def create_project_members(self, projects, users):
        """创建项目成员关系"""
        self.stdout.write('\n👤 创建项目成员...')
        
        permissions_list = [
            ['view', 'download'],
            ['view', 'download', 'upload'],
            ['view', 'download', 'upload', 'modify'],
            ['view', 'download', 'upload', 'modify', 'delete'],
        ]
        
        member_count = 0
        for project in projects:
            # 项目负责人自动有所有权限
            if project.manager:
                ProjectMemberPermission.objects.get_or_create(
                    user=project.manager,
                    project=project,
                    defaults={
                        'permission_status': 'active',
                        'position': '项目负责人',
                        'permissions': ['view', 'download', 'upload', 'modify', 'delete'],
                    }
                )
            
            # 为其他用户添加成员关系
            for user in users[:2]:  # testuser1, testuser2
                if user != project.manager:
                    perm, created = ProjectMemberPermission.objects.get_or_create(
                        user=user,
                        project=project,
                        defaults={
                            'permission_status': 'active',
                            'position': '项目成员',
                            'permissions': random.choice(permissions_list),
                        }
                    )
                    if created:
                        member_count += 1
        
        self.stdout.write(f'  ✅ 创建了 {member_count} 个项目成员关系')

    def create_documents(self, projects, users):
        """创建测试文档（mock 数据，不包含真实文件）"""
        self.stdout.write('\n📄 创建测试文档...')
        
        file_types = ['file', 'zip']
        file_categories = ['bidding', 'contract', 'achievement', 'process', 'original']
        zip_categories = ['dif', 'dwg', 'other']
        
        document_names = [
            '测试文档-项目需求文档.docx',
            '测试文档-技术方案.pdf',
            '测试文档-合同文件.pdf',
            '测试文档-成果报告.docx',
            '测试文档-原始数据.zip',
            '测试文档-设计图纸.dwg',
            '测试文档-数据包.zip',
        ]
        
        doc_count = 0
        for project in projects:
            # 每个项目创建 3-5 个文档
            num_docs = random.randint(3, 5)
            for i in range(num_docs):
                file_type = random.choice(file_types)
                if file_type == 'file':
                    category = random.choice(file_categories)
                    name = random.choice([d for d in document_names if not d.endswith('.zip')])
                else:
                    category = random.choice(zip_categories)
                    name = random.choice([d for d in document_names if d.endswith('.zip')])
                
                # 生成 mock 的 MinIO 路径
                minio_path = f"projects/{project.code}/documents/{name}"
                minio_bucket = 'documents' if file_type == 'file' else 'zip-files'
                
                # 为每个文档生成唯一的名称（添加项目代码前缀）
                unique_name = f"{project.code}-{name}"
                
                doc, created = Document.objects.get_or_create(
                    name=unique_name,
                    project=project,
                    defaults={
                        'original_name': name,
                        'file_type': file_type,
                        'category': category,
                        'minio_path': minio_path,
                        'minio_bucket': minio_bucket,
                        'file_size': random.randint(1024, 10 * 1024 * 1024),  # 1KB - 10MB
                        'mime_type': 'application/pdf' if name.endswith('.pdf') else 'application/zip' if name.endswith('.zip') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'version': 1,
                        'uploader': random.choice(users),
                    }
                )
                if created:
                    doc_count += 1
        
        self.stdout.write(f'  ✅ 创建了 {doc_count} 个测试文档')
        self.stdout.write(self.style.WARNING('  ⚠️  注意：这些文档只有数据库记录，没有真实文件'))

