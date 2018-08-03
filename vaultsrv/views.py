from rest_framework import viewsets

from vaultsrv.models.services import (
    Customer,
    Service,
    ServiceGroup,
    ServiceGroupMembership
)
from vaultsrv.models.users import Account, AccountGroup, GroupMembership
from vaultsrv.serializers import (
    AccountGroupSerializer,
    AccountSerializer,
    CustomerSerializer,
    GroupMembershipSerializer,
    ServiceGroupMembershipSerializer,
    ServiceGroupSerializer,
    ServiceSerializer
)


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ServiceGroupView(viewsets.ModelViewSet):
    queryset = ServiceGroup.objects.all()
    serializer_class = ServiceGroupSerializer


class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceGroupMembershipView(viewsets.ModelViewSet):
    queryset = ServiceGroupMembership.objects.all()
    serializer_class = ServiceGroupMembershipSerializer


class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountGroupView(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer


class GroupMembershipView(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
