from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from geostore.models import Layer

from .. import models

User = get_user_model()


class CrudGroupAdminTestCase(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='admin',
                                              is_active=True,
                                              is_staff=True,
                                              is_superuser=True)
        self.group = models.CrudGroupView.objects.create(name="group", order=0)
        self.client.force_login(self.user_admin)

    def test_list_endpoint(self):
        response = self.client.get(reverse('admin:terra_crud_crudgroupview_changelist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_endpoint(self):
        response = self.client.get(reverse('admin:terra_crud_crudgroupview_change', args=(self.group.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CrudViewAdminTestCase(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='admin',
                                              is_active=True,
                                              is_staff=True,
                                              is_superuser=True)
        self.group_1 = models.CrudGroupView.objects.create(name="group 1", order=0)
        self.group_2 = models.CrudGroupView.objects.create(name="group 2", order=1)
        self.view_1 = models.CrudView.objects.create(name="View 1", order=0, group=self.group_1,
                                                     layer=Layer.objects.create(name=1))
        self.view_2 = models.CrudView.objects.create(name="View 2", order=0, group=self.group_2,
                                                     layer=Layer.objects.create(name=2))
        self.view_3 = models.CrudView.objects.create(name="View 3", order=1, group=self.group_2,
                                                     layer=Layer.objects.create(name=3))
        self.client.force_login(self.user_admin)

    def test_list_endpoint(self):
        response = self.client.get(reverse('admin:terra_crud_crudview_changelist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_endpoint(self):
        response = self.client.get(reverse('admin:terra_crud_crudview_change', args=(self.view_1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
