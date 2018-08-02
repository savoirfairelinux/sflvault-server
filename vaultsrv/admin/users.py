from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

from vaultsrv.models import (
    Account, AccountGroup, GroupMembership
)


class AccountTabularInline(admin.TabularInline):
    model = Account
    can_delete = False
    verbose_name_plural = _("Account")


class UserAdmin(BaseUserAdmin):
    inlines = [AccountTabularInline]
    readonly_fields = ['last_login', 'date_joined']


class AccountGroupAdmin(admin.ModelAdmin):
    model = AccountGroup
    search_fields = ('name',)
    list_filter = ('is_hidden',)
    list_display = ('name', 'is_hidden')
    list_editable = ['is_hidden']


class GroupMembershipAdmin(admin.ModelAdmin):
    model = GroupMembership
    list_filter = ('account', 'account_group', 'is_admin')
    list_display = ('account', 'account_group', 'is_admin')
    list_editable = ['is_admin']


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
admin.site.register(AccountGroup, AccountGroupAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)
