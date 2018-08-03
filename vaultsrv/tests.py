import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

import factory

from .factories import (
    AccountFactory,
    AccountGroupFactory,
    CustomerFactory,
    GroupMembershipFactory,
    ServiceFactory,
    ServiceGroupFactory,
    ServiceGroupMembershipFactory,
    UserFactory
)
from .models.services import (
    Customer,
    Service,
    ServiceGroup,
    ServiceGroupMembership
)
from .models.users import Account, AccountGroup, GroupMembership


class TestAccount(TestCase):

    def setUp(cls):
        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )
        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

    def test_public_key_is_not_none(self):
        self.assertIsNotNone(self.test_account.pubkey)

    def test_user_is_not_none(self):
        self.assertIsNotNone(self.test_account.user)

    def test_department_is_not_none(self):
        self.assertIsNotNone(self.test_account.department)

    def test_user(self):
        self.assertEqual(self.test_account.user.username, 'admin')

    def test_public_key(self):
        self.assertEqual(self.test_account.pubkey, '123')

    def test_department(self):
        self.assertEqual(self.test_account.department, '123')


class TestCustomer(TestCase):

    def setUp(cls):
        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )
        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

        cls.test_customer = CustomerFactory(
            created_by=cls.test_account,
            name='test customer'
        )

    def test_date(self):
        self.assertEqual(self.test_customer.created, datetime.date.today())

    def test_name(self):
        self.assertEqual(self.test_customer.name, 'test customer')

    def test_created_by(self):
        self.assertEqual(self.test_customer.created_by.user.username, 'admin')


class TestAccountGroup(TestCase):

    def setUp(cls):
        cls.test_account_group = AccountGroupFactory(
            name='test',
            is_hidden=False,
            pubkey='123'
        )

        cls.test_account_group_hidden = AccountGroupFactory(
            name='test',
            is_hidden=True,
            pubkey='123'
        )

    def test_account_group_is_hidden(self):
        self.assertEqual(self.test_account_group_hidden.is_hidden, True)

    def test_account_is_not_hidden(self):
        self.assertEqual(self.test_account_group.is_hidden, False)

    def test_account_group_name(self):
        self.assertEqual(self.test_account_group.name, 'test')

    def test_account_group_pubkey(self):
        self.assertEqual(self.test_account_group.pubkey, '123')


class TestServiceGroup(TestCase):

    def setUp(cls):
        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )
        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

        cls.test_customer = CustomerFactory(
            created_by=cls.test_account,
            name='test customer'
        )

        cls.test_service_group = ServiceGroupFactory(
            customer=cls.test_customer,
            created=datetime.date.today(),
            fqdn='https://example.com',
            ip='192.168.0.1',
            location='Test Location',
            name='Test Service',
            notes='Test'
        )

    def test_service_group_customer(self):
        self.assertEqual(self.test_service_group.customer.name, 'test customer')

    def test_service_group_created(self):
        self.assertEqual(self.test_service_group.created, datetime.date.today())

    def test_service_group_fqdn(self):
        self.assertEqual(self.test_service_group.fqdn, 'https://example.com')

    def test_service_group_ip(self):
        self.assertEqual(self.test_service_group.ip, '192.168.0.1')

    def test_service_group_location(self):
        self.assertEqual(self.test_service_group.location, 'Test Location')

    def test_service_group_name(self):
        self.assertEqual(self.test_service_group.name, 'Test Service')

    def test_service_group_notes(self):
        self.assertEqual(self.test_service_group.notes, 'Test')


class GroupMembershipTest(TestCase):

    def setUp(cls):

        cls.test_account_group = AccountGroupFactory(
            name='test',
            is_hidden=False,
            pubkey='123'
        )

        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )

        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

        cls.test_group_membership = GroupMembershipFactory(
            account=cls.test_account,
            account_group=cls.test_account_group,
            cryptgroupkey='123',
            is_admin=True
        )

    def test_group_membership_account(self):
        self.assertEqual(self.test_group_membership.account.user.username, 'admin')

    def test_group_membership_account_group(self):
        self.assertEqual(self.test_group_membership.account_group.name, 'test')

    def test_group_membership_is_admin(self):
        self.assertEqual(self.test_group_membership.is_admin, True)

    def test_group_membership_cryptgroupkey(self):
        self.assertEqual(self.test_group_membership.cryptgroupkey, '123')


class ServiceTest(TestCase):

    def setUp(cls):

        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )

        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

        cls.test_customer = CustomerFactory(
            created_by=cls.test_account,
            name='test customer'
        )

        cls.test_service_group = ServiceGroupFactory(
            customer=cls.test_customer,
            created=datetime.date.today(),
            fqdn='https://example.com',
            ip='192.168.0.1',
            location='Test Location',
            name='Test Service',
            notes='Test'
        )

        cls.test_service = ServiceFactory(
            parent=cls.test_service_group,
            service_group=cls.test_service_group,
            created=datetime.date.today(),
            metadata='{test: test}',
            notes='test',
            secret='test secret',
            updated=datetime.date.today(),
            url='https://www.example.com'
        )

    def test_service_parent(self):
        self.assertEqual(self.test_service.parent.name, 'Test Service')

    def test_service_group(self):
        self.assertEqual(self.test_service.service_group.name, 'Test Service')

    def test_service_created(self):
        self.assertEqual(self.test_service.created, datetime.date.today())

    def test_service_metadata(self):
        self.assertEqual(self.test_service.metadata, '{test: test}')

    def test_service_notes(self):
        self.assertEqual(self.test_service.notes, 'test')

    def test_service_secret(self):
        self.assertEqual(self.test_service.secret, 'test secret')

    def test_service_updated(self):
        self.assertEqual(self.test_service.updated, datetime.date.today())

    def test_service_url(self):
        self.assertEqual(self.test_service.url, 'https://www.example.com')


class ServiceGroupMembershipTest(TestCase):

    def setUp(cls):
        cls.test_user = User.objects.create_superuser(
            username='admin',
            email='testadmin@example.com',
            password='test1234'
        )

        cls.test_account = AccountFactory(
            user=cls.test_user,
            department='123',
            pubkey='123'
        )

        cls.test_customer = CustomerFactory(
            created_by=cls.test_account,
            name='test customer'
        )

        cls.test_service_group = ServiceGroupFactory(
            customer=cls.test_customer,
            created=datetime.date.today(),
            fqdn='https://example.com',
            ip='192.168.0.1',
            location='Test Location',
            name='Test Service',
            notes='Test'
        )

        cls.test_service = ServiceFactory(
            parent=cls.test_service_group,
            service_group=cls.test_service_group,
            created=datetime.date.today(),
            metadata='{test: test}',
            notes='test',
            secret='test secret',
            updated=datetime.date.today(),
            url='https://www.example.com'
        )

        cls.test_account_group = AccountGroupFactory(
            name='test',
            is_hidden=False,
            pubkey='123'
        )

        cls.test_service_group_membership = ServiceGroupMembershipFactory(
            group=cls.test_account_group,
            service=cls.test_service,
            cryptsymkey='123'
        )

    def test_service_group_membership_group(self):
        self.assertEqual(self.test_service_group_membership.group.name, 'test')

    def test_service_group_membership_service(self):
        self.assertEqual(self.test_service_group_membership.service.notes, 'test')

    def test_service_group_membership_cryptsymkey(self):
        self.assertEqual(self.test_service_group_membership.cryptsymkey, '123')


class AccountApiTest(APITestCase):

    def setUp(cls):
        cls.user = UserFactory(
            username=factory.Faker('first_name')
        )
        cls.second_user = UserFactory(
            username=factory.Faker('first_name')
        )
        cls.account = AccountFactory(
            user=cls.user,
            department='test department',
            pubkey='123'
        )

    def test_get_all_account(self):
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Account.objects.all().count())

    def test_get_single_account(self):
        url = reverse('account-detail', kwargs={'pk': self.account.id})
        response = self.client.get(url)
        self.assertEqual(response.data['id'], self.account.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        data = {'department': 'department test', 'pubkey': '123456', 'user': self.second_user.id}
        url = reverse('account-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_account(self):
        account = AccountFactory()
        url = reverse('account-detail', kwargs={'pk': account.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_account(self):
        url = reverse('account-detail', kwargs={'pk': self.account.id})
        data = {'department': 'test_department', 'pubkey': '123456', 'user': self.user.id}
        response = self.client.put(url, data)
        self.assertEqual(response.data['department'], data['department'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountGroupApiTest(APITestCase):

    def setUp(cls):
        cls.account_group = AccountGroupFactory()

    def test_get_all_account_group(self):
        url = reverse('accountgroup-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), AccountGroup.objects.all().count())

    def test_get_single_account_group(self):
        url = reverse('accountgroup-detail', kwargs={'pk': self.account_group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.account_group.name)

    def test_create_account(self):
        url = reverse('accountgroup-list')
        data = {'is_hidden': True, 'name': 'test account group', 'pubkey': '123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_account_group(self):
        account_group = AccountGroupFactory()
        url = reverse('accountgroup-detail', kwargs={'pk': account_group.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_account_group(self):
        account_group = AccountGroupFactory()
        url = reverse('accountgroup-detail', kwargs={'pk': account_group.id})
        data = {'is_hidden': True, 'name': 'test account group', 'pubkey': '123'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])


class CustomerApiTest(APITestCase):

    def setUp(cls):
        cls.customer = CustomerFactory()

    def test_get_all_customer(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customer.objects.all().count())

    def test_get_single_customer(self):

        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.customer.name)

    def test_create_customer(self):
        account = AccountFactory()
        url = reverse('customer-list')
        data = {'created_by': account.id, 'name': '123', 'created': datetime.date.today()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_customer(self):
        customer = CustomerFactory()
        url = reverse('customer-detail', kwargs={'pk': customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_customer(self):
        customer = CustomerFactory()
        account = AccountFactory()
        url = reverse('customer-detail', kwargs={'pk': customer.id})
        data = {'created_by': account.id, 'name': '123', 'created': datetime.date.today()}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])


class TestServiceGroupApi(APITestCase):

    def setUp(cls):
        cls.service_group = ServiceGroupFactory()

    def test_get_all_service_group(self):
        url = reverse('servicegroup-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ServiceGroup.objects.all().count())

    def test_get_single_service_group(self):
        url = reverse('servicegroup-detail', kwargs={'pk': self.service_group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.service_group.name)

    def test_create_service_group(self):
        customer = CustomerFactory()
        url = reverse('servicegroup-list')
        data = {
            'customer': customer.id, 'created': datetime.date.today(),
            'fqdn': 'https://example.com', 'ip': '192.168.0.1', 'location': 'test location',
            'name': 'Test', 'notes': 'note test'
        }
        response = self.client.post(url, data)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['name'], data['name'])

    def test_delete_service_group(self):
        service_group = ServiceGroupFactory()
        url = reverse('servicegroup-detail', kwargs={'pk': service_group.id})
        response = self.client.delete(url)
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_service_group(self):
        service_group = ServiceGroupFactory()
        customer = CustomerFactory()
        url = reverse('servicegroup-detail', kwargs={'pk': service_group.id})
        data = {
            'customer': customer.id, 'created': datetime.date.today(),
            'fqdn': 'https://example.com', 'ip': '192.168.0.1', 'location': 'test location',
            'name': 'Test', 'notes': 'note test'
        }
        response = self.client.put(url, data)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['name'], data['name'])


class TestServiceApi(APITestCase):

    def setUp(cls):
        cls.service = ServiceFactory()

    def test_get_all_service(self):
        url = reverse('service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Service.objects.all().count())

    def test_get_single_service_group(self):
        url = reverse('service-detail', kwargs={'pk': self.service.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], self.service.notes)

    def test_delete_service(self):
        service = ServiceFactory()
        url = reverse('service-detail', kwargs={'pk': service.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_service(self):
        service_group = ServiceGroupFactory()
        parent = ServiceGroupFactory()
        url = reverse('service-list')
        data = {
            'parent': parent.id, 'service_group': service_group.id,
            'created': datetime.date.today(), 'metadata': '{}',
            'notes': 'test note', 'secret': 'test secret',
            'updated': datetime.date.today(), 'url': 'http://example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['notes'], data['notes'])

    def test_update_service(self):
        service = ServiceFactory()
        parent = ServiceGroupFactory()
        service_group = ServiceGroupFactory()
        url = reverse('service-detail', kwargs={'pk': service.id})
        data = {
            'parent': parent.id, 'service_group': service_group.id,
            'created': datetime.date.today(), 'metadata': '{}',
            'notes': 'test note 1', 'secret': 'test secret',
            'updated': datetime.date.today(), 'url': 'http://example.com'
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], data['notes'])


class TestServiceGroupMembershipApi(APITestCase):

    def setUp(cls):
        cls.service_group_membership = ServiceGroupMembershipFactory()

    def test_get_all_service_group_membership(self):
        url = reverse('servicegroupmembership-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ServiceGroupMembership.objects.all().count())

    def test_get_single_service_group_membership(self):
        url = reverse(
            'servicegroupmembership-detail',
            kwargs={'pk': self.service_group_membership.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cryptsymkey'], self.service_group_membership.cryptsymkey)

    def test_delete_service_group_membership(self):
        service_group_membership = ServiceGroupMembershipFactory()
        url = reverse('servicegroupmembership-detail', kwargs={'pk': service_group_membership.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_service_group_membership(self):
        account_group = AccountGroupFactory()
        service = ServiceFactory()
        url = reverse('servicegroupmembership-list')
        data = {'group': account_group.id, 'service': service.id, 'cryptsymkey': '123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cryptsymkey'], data['cryptsymkey'])

    def test_update_service_group_membership(self):
        account_group = AccountGroupFactory()
        service = ServiceFactory()
        service_group_membership = ServiceGroupMembershipFactory()
        url = reverse('servicegroupmembership-detail', kwargs={'pk': service_group_membership.id})
        data = {'group': account_group.id, 'service': service.id, 'cryptsymkey': '123'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cryptsymkey'], data['cryptsymkey'])


class TestGroupMembershipApi(APITestCase):
    def setUp(cls):
        cls.group_membership = GroupMembershipFactory()

    def test_get_all_group_membership(self):
        url = reverse('groupmembership-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), GroupMembership.objects.all().count())

    def test_get_single_group_membership(self):
        url = reverse('groupmembership-detail', kwargs={'pk': self.group_membership.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cryptgroupkey'], self.group_membership.cryptgroupkey)

    def test_delete_group_membership(self):
        group_membership = GroupMembershipFactory()
        url = reverse('groupmembership-detail', kwargs={'pk': group_membership.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_group_membership(self):
        account_group = AccountGroupFactory()
        account = AccountFactory()
        url = reverse('groupmembership-list')
        data = {
            'account': account.id, 'account_group': account_group.id,
            'cryptgroupkey': '123', 'is_admin': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cryptgroupkey'], data['cryptgroupkey'])

    def test_update_group_membership(self):
        account_group = AccountGroupFactory()
        account = AccountFactory()
        group_membership = GroupMembershipFactory()
        url = reverse('groupmembership-detail', kwargs={'pk': group_membership.id})
        data = {
            'account': account.id, 'account_group': account_group.id,
            'cryptgroupkey': '1234567', 'is_admin': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cryptgroupkey'], data['cryptgroupkey'])
