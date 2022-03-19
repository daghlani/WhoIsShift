from config.config import PRI_WEEK_MAP, owner_perms
from django.contrib.auth.models import Group, Permission


def group_init(sender, **kwargs):
    for perm in owner_perms:
        new_group, created = Group.objects.get_or_create(name='owners')
        permission = Permission.objects.get(name=perm)
        new_group.permissions.add(permission)
