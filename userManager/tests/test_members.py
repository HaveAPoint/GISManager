from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from userManager.models import Department

User = get_user_model()


class DepartmentMembersAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='pass', is_staff=True)
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.department = Department.objects.create(name='DeptA', code='DPT001', manager=self.admin)
        self.client.force_authenticate(user=self.admin)

    def test_add_and_remove_members(self):
        url = f'/api/v1/departments/{self.department.id}/members/'
        resp = self.client.post(url, {'user_ids': [str(self.user1.id), str(self.user2.id)]}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.department.id, self.department.id)
        self.assertEqual(self.user2.department.id, self.department.id)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any(u['id'] == str(self.user1.id) for u in data))
        self.assertTrue(any(u['id'] == str(self.user2.id) for u in data))

        del_url = f'/api/v1/departments/{self.department.id}/members/{self.user1.id}/'
        resp = self.client.delete(del_url)
        self.assertEqual(resp.status_code, 200, resp.content)
        self.user1.refresh_from_db()
        self.assertIsNone(self.user1.department)
