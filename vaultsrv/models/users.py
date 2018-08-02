from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ['Account', 'AccountGroup', 'GroupMembership']


class Account(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='account'
    )
    groups = models.ManyToManyField(
        'AccountGroup', through='GroupMembership', related_name="accounts"
    )
    department = models.CharField(
        max_length=255, verbose_name=_("Company department")
    )
    pubkey = models.TextField(verbose_name=_("Public key"))

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['user']

    def __str__(self):
        return "{} - {}".format(self.user, self.department)


class AccountGroup(models.Model):
    name = models.CharField(max_length=255)
    is_hidden = models.BooleanField(default=False)
    pubkey = models.TextField()

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Account group')
        verbose_name_plural = _('Account groups')
        ordering = ['name']

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    cryptgroupkey = models.TextField(verbose_name=_("Cryptography group key"))

    class Meta:
        app_label = "vaultsrv"
        verbose_name = _('Group membership')
        verbose_name_plural = _('Group memberships')
        unique_together = (('account', 'account_group'),)

    def __str__(self):
        return "{} [{}]".format(self.account, self.account_group)
