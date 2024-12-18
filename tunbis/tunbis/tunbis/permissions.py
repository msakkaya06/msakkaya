from django.contrib.auth.models import Group, Permission

def assign_permissions_to_groups():
    # Özel izinleri oluşturun veya alın
    can_access_operations = Permission.objects.get(codename='can_access_operations')
    can_search_registration_number = Permission.objects.get(codename='can_search_registration_number')
    can_search_name = Permission.objects.get(codename='can_search_name')
    can_search_all = Permission.objects.get(codename='can_search_all')

    # Yetkilendirme gruplarını oluşturun veya alın
    personel_group, created = Group.objects.get_or_create(name='Personel')

    # Gruplara izinleri atayın
    personel_group.permissions.add(can_access_operations)
    personel_group.permissions.add(can_search_registration_number)
    personel_group.permissions.add(can_search_name)
    personel_group.permissions.add(can_search_all)
