from rest_framework.routers import SimpleRouter

from .views import (
    AccountGroupView,
    AccountView,
    CustomerView,
    GroupMembershipView,
    ServiceGroupMembershipView,
    ServiceGroupView,
    ServiceView
)

router = SimpleRouter()
router.register('accounts', AccountView)
router.register('account_groups', AccountGroupView)
router.register('customers', CustomerView)
router.register('group_memberships', GroupMembershipView)
router.register('service_group_memberships', ServiceGroupMembershipView)
router.register('service_groups', ServiceGroupView)
router.register('services', ServiceView)
urlpatterns = router.urls
