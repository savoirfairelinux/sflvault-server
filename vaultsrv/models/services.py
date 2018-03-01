from django.contrib.postgres.fields import JSONField
from django.db import models
from vaultsrv.models import users
from django.utils.translation import ugettext_lazy as _

__all__ = ['Customer', 'ServiceGroup', 'Service', 'ServiceGroupMembership']


class Customer(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(
        users.Account, related_name="customers", null=True, blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='service_groups', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True, blank=True)
    fqdn = models.CharField(
        max_length=255, verbose_name=_("Name or domain"), null=True,
        blank=True
    )
    ip = models.CharField(
        max_length=39, null=True, blank=True,
        help_text=_("IP address of the server")
    )
    location = models.CharField(
        max_length=255, null=True, blank=True, help_text=_("Physical place")
    )
    notes = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Service group')
        verbose_name_plural = _('Service groups')
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    service_group = models.ForeignKey(
        ServiceGroup, related_name="services", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        ServiceGroup, null=True, blank=True, on_delete=models.SET_NULL,
        help_text=_("The group this service belongs to")
    )
    created = models.DateField(auto_now_add=True, blank=True)
    updated = models.DateField(auto_now=True, blank=True)
    url = models.URLField()
    metadata = JSONField(
        blank=True, default={}, help_text=_("Accept JSON format")
    )
    notes = models.TextField(null=True, blank=True)
    secret = models.TextField(help_text=_("Service's password"))

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['created']

    def __str__(self):
        return "{} - [{}]".format(self.service_group, self.url)


class ServiceGroupMembership(models.Model):
    group = models.ForeignKey(
        users.AccountGroup, related_name="service_group_memberships",
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service, related_name="service_group_memberships",
        on_delete=models.CASCADE
    )
    cryptsymkey = models.TextField(verbose_name=_("Cryptography sym key"))

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Service group membership')
        verbose_name_plural = _('Service group memberships')
        ordering = ['service']

    def __str__(self):
        return "{} - {}".format(self.group, self.service)
