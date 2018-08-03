import datetime

from django.contrib.auth.models import User

import factory

from .models.services import (
    Customer,
    Service,
    ServiceGroup,
    ServiceGroupMembership
)
from .models.users import Account, AccountGroup, GroupMembership


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda x: "user{}".format(x))


class AccountGroupFactory(factory.DjangoModelFactory):

    class Meta:
        model = AccountGroup

    name = "test group"
    is_hidden = False
    pubkey = "123456"


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)

    department = factory.Faker('first_name')

    pubkey = "123456"


class CustomerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Customer

    created_by = factory.SubFactory(AccountFactory)

    created = datetime.date.today()
    name = factory.Faker('first_name')


class ServiceGroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = ServiceGroup

    customer = factory.SubFactory(CustomerFactory)

    created = datetime.date.today()

    fqdn = "test_domain"
    ip = "192.168.0.1"
    location = "test location"
    name = "Test Service"
    notes = "Test"


class GroupMembershipFactory(factory.DjangoModelFactory):

    class Meta:
        model = GroupMembership

    account = factory.SubFactory(AccountFactory)
    account_group = factory.SubFactory(AccountGroupFactory)
    cryptgroupkey = "123"
    is_admin = False


class ServiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Service

    parent = factory.SubFactory(ServiceGroupFactory)
    service_group = factory.SubFactory(ServiceGroupFactory)

    created = datetime.date.today()

    metadata = "{test: test}"

    notes = "test"
    secret = "test secret"

    updated = datetime.date.today()

    url = "https://www.example.com"


class ServiceGroupMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = ServiceGroupMembership

    group = factory.SubFactory(AccountGroupFactory)
    service = factory.SubFactory(ServiceFactory)
    cryptsymkey = "123"
