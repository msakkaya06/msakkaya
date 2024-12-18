from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.core.paginator import Paginator
from tunbisapp.models import TebsUser, Unit
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required




# Create your views here.
def index(req):
     print(req.path)
     return render(req,'personel/personel_index.html')

def assignment(req):
     print(req.path)
     return render(req,'personel/personel_atama.html')

@login_required
@permission_required('personel.can_access_operations', raise_exception=True)
def personnel_operations(request):
     users = []
     personnels = []


     context = {
        'page_obj': personnels,
        'personnels':personnels
    }
     return render(request, 'personel/personnel_operations.html', context)
    

@login_required
@permission_required('personel.can_search_registration_number', raise_exception=True)
def search_registration_number(request):
    reg_number = request.GET.get('registration_number')
    users = TebsUser.objects.filter(registration_number__icontains=reg_number)
    personnels = []
    for user in users:
          unit_name = "Birim Bilgisi Boş"  # Varsayılan birim adı
          try:
        # Kullanıcının bağlı olduğu birimi al
               parent_unit_id = user.unit.parent_unit
               parent_unit = Unit.objects.get(pk=parent_unit_id)
               unit_id = user.unit.id
               unit = Unit.objects.get(pk=unit_id)
               if parent_unit is not None:
                    if unit.id  != 1: # Birimi Tepe birim olan Tunceli İl Emniyet Müdürlüğünden farklı ise hem üst birimi hem de alt birimi göster
                         unit_name = parent_unit.name + " - " + unit.name  # Birim adını al
                    else: # Birimi tepe birim ise sadece Tunceli İl Emniyet Müdürlüğü yaz
                         unit_name = unit.name  # Birim adını al

          except ObjectDoesNotExist:
               pass
    # Personel veri transfer nesnesi oluştur
          personnel_dto = {
               "registration_number": user.registration_number,
               "first_name": user.first_name,
               "last_name": user.last_name,
               "rank":user.rank,
               "unit": unit_name  # Birim bilgisini ekle
          }
          personnels.append(personnel_dto)
    parent_units = []
    context = {
        'personnels': personnels
    }
    return render(request, 'personel/personnel_operations.html', context)

@login_required
@permission_required('personel.can_search_name', raise_exception=True)
def search_name(request):
    name = request.GET.get('first_name_last_name')
    users = TebsUser.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    personnels = []
    for user in users:
          unit_name = "Birim Bilgisi Boş"  # Varsayılan birim adı
          try:
        # Kullanıcının bağlı olduğu birimi al
               parent_unit_id = user.unit.parent_unit
               parent_unit = Unit.objects.get(pk=parent_unit_id)
               unit_id = user.unit.id
               unit = Unit.objects.get(pk=unit_id)
               if parent_unit is not None:
                    if unit.id  != 1: # Birimi Tepe birim olan Tunceli İl Emniyet Müdürlüğünden farklı ise hem üst birimi hem de alt birimi göster
                         unit_name = parent_unit.name + " - " + unit.name  # Birim adını al
                    else: # Birimi tepe birim ise sadece Tunceli İl Emniyet Müdürlüğü yaz
                         unit_name = unit.name  # Birim adını al

          except ObjectDoesNotExist:
               pass
    
    # Personel veri transfer nesnesi oluştur
          personnel_dto = {
               "registration_number": user.registration_number,
               "first_name": user.first_name,
               "last_name": user.last_name,
               "rank":user.rank,
               "unit": unit_name  # Birim bilgisini ekle
          }
          personnels.append(personnel_dto)
    context = {
        'personnels': personnels
    }
    return render(request, 'personel/personnel_operations.html', context)

@login_required
@permission_required('personel.can_search_all', raise_exception=True)
def search_all(request):
    # Tüm personelleri getir ve her biri için parent_unit'ı kontrol et
    users = TebsUser.objects.all()
    context = {
        'personnels': users,
    }
    return render(request, 'personel/personnel_operations.html', context)
