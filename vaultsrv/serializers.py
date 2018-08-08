from rest_framework import serializers

from vaultsrv.models.services import (
    Customer,
    Service,
    ServiceGroup,
    ServiceGroupMembership
)
from vaultsrv.models.users import Account, AccountGroup, GroupMembership


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroup
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceGroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroupMembership
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = '__all__'


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'
