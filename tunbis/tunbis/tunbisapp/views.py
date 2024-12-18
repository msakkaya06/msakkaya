from datetime import date
import datetime
from decimal import Decimal
from django.shortcuts import render
from .models import InfoCard, Personnel_Assignment, TebsUser
from django.contrib.auth.decorators import user_passes_test,login_required

# Create your views here.
@login_required
def index(request):
    groups = request.user.groups.all()
    print(groups)
    context = {'groups': groups}
    return render(request, './index.html', context)


def details(req):
    pass

@login_required
def birthday(req):
    today=date.today()
    users = TebsUser.objects.filter(birthday__day=today.day, birthday__month=today.month)
    print(users)
    user_dto = []
    index=0
    for item in users:
             index+=1
             birthday_dto = {
                'id':index,
                'reg_number': item.registration_number,
                'first_name': item.first_name,
                'last_name':item.last_name,
                'tel_number': item.telephone_number,
                'is_passive': item.is_passive,
                'rank': item.rank,
                'passive_desc':item.passive_description,
                'temp_station':item.temp_duty_station
             }
             user_dto.append(birthday_dto)  # Oluşturulan DTO'yu listeye ekle

    context={"data":user_dto}
    return render(req,"./birthday.html",context)


def personnel_assignment(req):
    personnel_assignment = "None"
    if req.method == 'POST':
        national_identity_number = req.POST.get('national_identity_number')
        registration_number = req.POST.get('registration_number')

        try:
            personnel_assignment = Personnel_Assignment.objects.get(national_identity_number=national_identity_number, registration_number=registration_number)
        except Personnel_Assignment.DoesNotExist:
            personnel_assignment = "DoesNotExist"

    return render(req, 'personnel_assignment.html', {'personnel_assignment': personnel_assignment})
