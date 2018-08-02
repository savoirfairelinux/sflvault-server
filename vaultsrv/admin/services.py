from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from vaultsrv.models import (
    Account, Customer, ServiceGroup, Service, ServiceGroupMembership
)


class AccountIsStaffListFilter(admin.SimpleListFilter):
    title = _('created by')
    parameter_name = 'created_by'

    def lookups(self, request, model_admin):
        return [
            (a.id, a.user) for a in Account.objects.filter(user__is_staff=True)
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_by__pk=self.value())


class CustomerModelForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'created_by': forms.widgets.Select(attrs={'disabled': True})
        }


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    form = CustomerModelForm
    search_fields = ('name',)
    list_filter = (AccountIsStaffListFilter,)
    list_display = ('name', 'created_by')
    readonly_fields = ['created']

    @staticmethod
    def _set_current_account_as_created_by(request):
        data = getattr(request, request.method).copy()
        # If the account is created by createsuperuser
        # the account relation DoesNotExist
        try:
            data['created_by'] = request.user.account.pk
        except Account.DoesNotExist:
            data['created_by'] = None
        setattr(request, request.method, data)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['queryset'] = Account.objects.filter(
                user__pk=request.user.pk
            )
        return super(CustomerAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def add_view(self, request, form_url='', extra_context=None):
        self._set_current_account_as_created_by(request)
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self._set_current_account_as_created_by(request)
        return super().change_view(request, object_id, form_url, extra_context)


class ServiceGroupAdmin(admin.ModelAdmin):
    model = ServiceGroup
    fieldsets = (
        (None, {
            'fields': ('name', 'customer', 'fqdn', 'ip', 'location', 'notes')
        }),
    )
    search_fields = ('name', 'fqdn', 'ip', 'location')
    list_filter = ('customer',)
    list_display = ('name', 'customer', 'fqdn', 'ip', 'location')


class ServiceAdmin(admin.ModelAdmin):
    model = Service
    fieldsets = (
        (None, {
            'fields': (
                'service_group', 'url', 'parent', 'secret', 'metadata', 'notes'
            )
        }),
    )
    search_fields = ('url',)
    list_filter = ('service_group', 'parent')
    list_display = ('service_group', 'url', 'parent')


class ServiceGroupMembershipAdmin(admin.ModelAdmin):
    model = ServiceGroupMembership
    list_filter = ('group', 'service')
    list_display = ('group', 'service')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceGroupMembership, ServiceGroupMembershipAdmin)
