from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tunbisapp.models import FaultAction, Computer_Informations, PrinterScannerInformation



# Create your views here.
@login_required
def index(request):
    # Kullanıcının birimi
    user_unit = getattr(request.user, "unit", None)

    # Kullanıcının birimine göre cihazları al
    computers = Computer_Informations.objects.filter(unit=user_unit) if user_unit else []
    printers = PrinterScannerInformation.objects.filter(unit=user_unit) if user_unit else []


    context = {
        "unit": user_unit,
        "computers": computers,
        "printers": printers,
    
    }
    return render(request, "ariza_takip/fault_index.html", context)


@login_required
def fault_create(request, pk):
    # GET parametresinden cihaz tipini alıyoruz
    device_type = request.GET.get('type')

    # Cihaz tipine göre ilgili modeli kontrol et ve cihaz bilgilerini düzenle
    if device_type == "computer":
        device = get_object_or_404(Computer_Informations, pk=pk)
        device_data = {
            'name': device.computer_name,
            'ip_address': device.ip_address,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'image': device.image.url if device.image else None,
        }
    elif device_type == "printer":
        device = get_object_or_404(PrinterScannerInformation, pk=pk)
        device_data = {
            'name': device.device_name,
            'ip_address': device.ip_address,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'image': device.image.url if device.image else None,
        }
    else:
        device_data = None

    # Eğer cihaz tipi geçersizse, hata sayfasına yönlendir
    if not device_data:
        return redirect('error_page')  # Hata sayfası veya uygun yönlendirme yapılabilir

    # Mevcut bir arıza kaydı olup olmadığını kontrol et
    existing_fault_action = None
    if device_type == "computer":
        existing_fault_action = FaultAction.objects.filter(computer=device,is_active=True).first()
    elif device_type == "printer":
        existing_fault_action = FaultAction.objects.filter(printer=device, is_active=True).first()
    if existing_fault_action:
        requester_notes = existing_fault_action.requester_notes
        messages.warning(request, f"{device_data['name']} cihazı için {existing_fault_action.requester_date.strftime('%d-%m-%Y')} tarihinde açılmış bir arıza kaydınız bulunmaktadır.")
    # Eğer POST isteği varsa, formu işleyelim
    if request.method == "POST":
        requester_notes = request.POST.get('requester_notes')

        if existing_fault_action:
            # Eğer daha önce bir kayıt varsa, güncelleme işlemi yapalım
            existing_fault_action.requester_notes = requester_notes
            existing_fault_action.save()
            messages.success(request, f"{device_data['name']} cihazı için {existing_fault_action.requester_date.strftime('%d-%m-%Y')} tarihinde açılmış arıza kaydınız başarıyla güncellenmiştir.")
        else:
            # Yeni bir arıza kaydı oluştur
            fault_action = FaultAction(
                device_type=device_type,
                requester_notes=requester_notes,
                requester=request.user,
                is_active=True
            )

            # Cihaz tipine göre ilgili cihazı ilişkilendir
            if device_type == "computer":
                fault_action.computer = device
            elif device_type == "printer":
                fault_action.printer = device

            fault_action.save()
            messages.success(request, 'Yeni Arıza Kaydınız Başarıyla Oluşturuldu')

     

    # Eğer GET isteği ise, cihaz ve kullanıcı bilgileri ile template'e render edelim
    context = {
        'device': device_data,
        'user_data': {
            'registration_number': request.user.registration_number if hasattr(request.user, 'registration_number') else '-',
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        },
        'device_type': device_type,  # Cihaz tipini de ekledik
        'existing_fault_action': existing_fault_action,  # Mevcut kaydı template'e gönderiyoruz
    }

    return render(request, 'ariza_takip/fault_create.html', context)


def fault_create_save(request):
    pass

@login_required
def fault_tracking(request):
    # Kullanıcının birim bilgisi
    user_unit = request.user.unit if hasattr(request.user, 'unit') else None

    # Eğer kullanıcı birime bağlı değilse tüm arızaları göster
    if not user_unit:
        return render(request, 'ariza_takip/fault_tracking.html', {'error': 'Birime bağlı değilsiniz.'})

    # Aktif arızalar
    active_faults = []
    active_actions = FaultAction.objects.filter(is_active=True)

    for action in active_actions:
        requester = action.requester
        device_info = {
            'id': None,
            'image_url': None,
            'name': None,
            'manufacturer': None,
            'model': None,
            'unit_name': None,
            'network_used': None
        }

        # Cihazın birimi kontrol edilerek filtreleme yapılır
        if action.device_type == 'computer' and action.computer and action.computer.unit == user_unit:
            device = action.computer
            device_info.update({
                'id': device.id,
                'image_url': device.image.url if device.image else None,
                'name': device.computer_name,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'unit_name': device.unit.name if device.unit else None,
                'network_used': device.network_used,
            })

        elif action.device_type == 'printer' and action.printer and action.printer.unit == user_unit:
            device = action.printer
            device_info.update({
                'id': device.id,
                'image_url': device.image.url if device.image else None,
                'name': device.device_name,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'unit_name': device.unit.name if device.unit else None,
                'network_used': device.network_used,
            })

        # Eğer cihaz kullanıcının birimine ait değilse ekleme yapılmaz
        if device_info['id']:
            fault_dto = {
                'device_type': action.device_type,
                'device_id': device_info['id'],
                'requester_username': requester.username if requester else None,
                'requester_notes': action.requester_notes,
                'requester_first_name': requester.first_name if requester else None,
                'requester_last_name': requester.last_name if requester else None,
                'device_image': device_info['image_url'],
                'device_name': device_info['name'],
                'manufacturer': device_info['manufacturer'],
                'model': device_info['model'],
                'unit_name': device_info['unit_name'],
                'network_used': device_info['network_used'],
                'action_pk': action.pk,
            }
            active_faults.append(fault_dto)

    # Geçmiş arızalar
    completed_faults = []
    completed_actions = FaultAction.objects.filter(is_active=False).order_by('-completed_date')[:10]

    for action in completed_actions:
        requester = action.requester
        performer = action.performer
        device_info = {
            'id': None,
            'image_url': None,
            'name': None,
            'manufacturer': None,
            'model': None,
            'unit_name': None,
            'network_used': None
        }

        if action.device_type == 'computer' and action.computer and action.computer.unit == user_unit:
            device = action.computer
            device_info.update({
                'id': device.id,
                'image_url': device.image.url if device.image else None,
                'name': device.computer_name,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'unit_name': device.unit.name if device.unit else None,
                'network_used': device.network_used,
            })

        elif action.device_type == 'printer' and action.printer and action.printer.unit == user_unit:
            device = action.printer
            device_info.update({
                'id': device.id,
                'image_url': device.image.url if device.image else None,
                'name': device.device_name,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'unit_name': device.unit.name if device.unit else None,
                'network_used': device.network_used,
            })

        if device_info['id']:
            fault_dto = {
                'device_type': action.device_type,
                'device_id': device_info['id'],
                'performer_username': performer.username if performer else None,
                'action_notes': action.action_notes,
                'performer_first_name': performer.first_name if performer else None,
                'performer_last_name': performer.last_name if performer else None,
                'device_image': device_info['image_url'],
                'device_name': device_info['name'],
                'manufacturer': device_info['manufacturer'],
                'model': device_info['model'],
                'unit_name': device_info['unit_name'],
                'network_used': device_info['network_used'],
                'action_pk': action.pk,
            }
            completed_faults.append(fault_dto)

    context = {
        'active_faults': active_faults,
        'completed_faults': completed_faults
    }
    return render(request, 'ariza_takip/fault_tracking.html', context)
