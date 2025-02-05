from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from tunbisapp.models import Computer_Informations, TebsUser, Unit, computer_action, PrinterScannerInformation,FaultAction
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # Üretici firmaların bilgileri
    manufacturers = Computer_Informations.objects.values('manufacturer').annotate(total=Count('manufacturer')).order_by('-total')
    network_computer_counts = Computer_Informations.objects.values('network_used').annotate(total=Count('network_used')).order_by('-total')
    units = Unit.objects.filter(is_active=True)
    unit_data = []
    
    count = {}
    for network in network_computer_counts:
        count[network['network_used'].lower()] = network['total']
    polnet_count = count.get('polnet', 0)
    internet_count = count.get('internet', 0)
    kgys_count = count.get('kgys', 0)
    
    count = {
        "polnet": polnet_count,
        "kgys": kgys_count,
        "internet": internet_count
    }

    # Renk paleti ve üreticilere renk sınıfı atama
    COLOR_CLASSES = ['primary', 'success', 'info', 'warning', 'danger']
    for i, manufacturer in enumerate(manufacturers):
        manufacturer['color_class'] = COLOR_CLASSES[i % len(COLOR_CLASSES)]
    
    # Birimlere göre bilgisayar sayıları
    for unit in units:
        polnet = Computer_Informations.objects.filter(unit=unit, network_used='PolNet').count()
        internet = Computer_Informations.objects.filter(unit=unit, network_used='Internet').count()
        if polnet > 0 or internet > 0:
            unit_data.append({
                "id": unit.pk,
                "name": unit.name,
                "polnet": polnet,
                "internet": internet,
            })
    
    context = {
        'manufacturers': manufacturers,
        'count': count,
        'unit_data': unit_data
    }
    return render(request, 'bilisim_envanter/envanter_index.html', context)




def computer_detail_for_unit(request, pk):
    # İlgili birimi getir
    unit = get_object_or_404(Unit, pk=pk)
    # Birime ait bilgisayarları filtrele
    computers = Computer_Informations.objects.filter(unit=unit)

    context = {
        'unit': unit,
        'computers': computers,
    }
    return render(request, 'bilisim_envanter/computer_detail_for_unit.html', context)


def fault_tracking(request):
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
        
        if action.device_type == 'computer' and action.computer:
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
        
        elif action.device_type == 'printer' and action.printer:
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

        if action.device_type == 'computer' and action.computer:
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

        elif action.device_type == 'printer' and action.printer:
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
    return render(request, 'bilisim_envanter/fault_tracking.html', context)

def fault_summary(request):
    # Bilgisayar arızaları ve tamamlanmış arıza sayısı
    total_computer_faults = FaultAction.objects.filter(device_type = 'computer').count()
    completed_computer_faults = FaultAction.objects.filter(device_type='computer',is_active=False).count()

    # Yazıcı-Tarayıcı verileri (örnek)
    total_printer_faults = FaultAction.objects.filter(device_type = 'printer').count()
    completed_printer_faults = FaultAction.objects.filter(device_type='printer',is_active=False).count()

    # Son 12 ayda tamamlanmış arızaların istatistiği
    completed_faults_per_month = []
    months = []

    for i in range(12):
        month = datetime.now() - timedelta(days=i * 30)
        start_month = month.replace(day=1)
        end_month = (start_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        completed_fault_count = FaultAction.objects.filter(
            completed_date__range=[start_month, end_month], is_active=False
        ).count()
        
        completed_faults_per_month.append(completed_fault_count)
        months.append(start_month.strftime("%Y-%m"))

    stats = {
        'total_computer_faults': total_computer_faults,
        'completed_computer_faults': completed_computer_faults,
        'total_printer_faults': total_printer_faults,
        'completed_printer_faults': completed_printer_faults,
        'completed_faults_per_month': completed_faults_per_month,
        'months': months,
    }

    return render(request, 'bilisim_envanter/fault_summary.html', {'stats': stats})


def fault_tracking_detail(request, pk):
    action = get_object_or_404(FaultAction, pk=pk)
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

    if action.device_type == 'computer' and action.computer:
        device = action.computer
        last_actions=FaultAction.objects.filter(computer=action.computer)
        device_info.update({
            'id': device.id,
            'image_url': device.image.url if device.image else None,
            'name': device.computer_name,
            'serial_number': device.serial_number,
            'id_address': device.ip_address,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'processor_name': device.processor_name,
            'total_ram_gb': device.total_ram_gb,
            'disk_size_gb': device.disk_size_gb,
            'media_type': device.media_type,
            'unit_name': device.unit.name,
            'network_used': device.network_used,
            
        })

    elif action.device_type == 'printer' and action.printer:
        device = action.printer
        last_actions=FaultAction.objects.filter(printer=action.printer)
        device_info.update({
            'id': device.id,
            'image_url': device.image.url if device.image else None,
            'name': device.device_name,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'unit_name': device.unit.name if device.unit else None,
            'network_used': device.network_used,
        })
  

    fault_dto = {
        'device_id':device_info['id'],
        'action_id':action.pk,
        'device_type': action.device_type,
        'requester_username': requester.username if requester else None,
        'performer_username': performer.username if performer else None,
        'requester_notes': action.requester_notes,
        'action_notes': action.action_notes,
        'part_installed':action.part_installed,
        'os_installed':action.os_installed,
        'ink_replaced' : action.ink_replaced,
        'paper_jam_fixed' : action.paper_jam_fixed,
        'hardware_fixed' : action.hardware_fixed,
        'software_fixed' : action.software_fixed,
        'is_active':action.is_active,
        'requester_registration_number': requester.registration_number if requester else None,
        'requester_first_name': requester.first_name if requester else None,
        'requester_last_name': requester.last_name if requester else None,
        'performer_first_name': performer.first_name if performer else None,
        'performer_last_name': performer.last_name if performer else None,
        'device_image': device_info['image_url'],
        'device_name': device_info['name'],
        'device_manufacturer': device_info['manufacturer'],
        'device_model': device_info['model'],
        'device_unit_name': device_info['unit_name'],
        'device_serial_number': device_info['serial_number'] if action.device_type == "computer" else None,
        'device_ip_address': device_info['id_address'] if action.device_type == "computer" else None,
        'device_manufacturer': device_info['manufacturer'],
        'device_model': device_info['model'],
        'device_processor_name': device_info['processor_name'] if action.device_type == "computer" else None,
        'device_total_ram_gb': device_info['total_ram_gb'] if action.device_type == "computer" else None,
        'device_disk_size_gb': device_info['disk_size_gb'] if action.device_type == "computer" else None,
        'device_media_type': device_info['media_type'] if action.device_type == "computer" else None,
        'device_network_used': device_info['network_used'],
        'device_requester_date': action.requester_date,
    }
    context = {
        'fault_detail': fault_dto,
        'last_actions':last_actions
    }

    return render(request, 'bilisim_envanter/fault_detail.html', context)

def computer(request):
    computers = Computer_Informations.objects.filter(is_active=True)
    paginator=Paginator(computers,30)
    page=request.GET.get('page',1)
    page_obj=paginator.get_page(page)
    context={
        "page_obj":page_obj,
        "computers":page_obj
    }
    return render(request, 'bilisim_envanter/computer_list.html',context)
def computer_detail(request, pk):
    computer = get_object_or_404(Computer_Informations, pk=pk)
    return render(request, 'bilisim_envanter/computer_details.html', {'computer': computer})


def search_name(request):
    computer_name = request.GET['computer_name']
    computers = Computer_Informations.objects.filter(computer_name__icontains=computer_name)
    return render(request, 'bilisim_envanter/computer_list.html', {'computers': computers})

def search_name_fault_temp(request):
    fault_dto=None
    computer_name = request.GET['computer_name']
    if computer_name == '':
        messages.add_message(request,messages.ERROR,"Bilgisayar Adı Boş Olamaz")
        return redirect("fault_record_create")
    computer = Computer_Informations.objects.get(computer_name=computer_name)
    existing_action = FaultAction.objects.filter(computer=computer, is_active=True).first()
    if existing_action is not None:
        requester=TebsUser.objects.get(username=existing_action.requester.username)
        fault_dto ={
            'requester_username':existing_action.requester,
            'requester_notes':existing_action.requester_notes,
            'requester_first_name':requester.first_name,
            'requester_last_name':requester.last_name,
        }

    if computer is None:
          return JsonResponse({'error': 'Bilgisayar Bulunamadı. İsmi kontrol edin'}, status=200)
    return render(request, 'bilisim_envanter/fault_record_create.html', {'computer': computer,'fault':fault_dto})


def search_name_fault(request):
    device_id = request.GET.get('device_id')
    device_type = request.GET.get('device_type')  # Cihaz türü bilgisi
    print(device_id)
    print(device_type)
    if not device_id or not device_type:
        return JsonResponse({'error': 'Cihaz ID veya türü eksik!'}, status=400)
    
    if device_type == 'computer':
        try:
            device = Computer_Informations.objects.get(id=device_id)
            fault = None
        except Computer_Informations.DoesNotExist:
            return JsonResponse({'error': 'Bilgisayar bulunamadı!'}, status=404)
    elif device_type == 'printer':
        try:
            device = PrinterScannerInformation.objects.get(id=device_id)
            fault = None
        except PrinterScannerInformation.DoesNotExist:
            return JsonResponse({'error': 'Yazıcı bulunamadı!'}, status=404)
    else:
        return JsonResponse({'error': 'Geçersiz cihaz türü!'}, status=400)

    # Geri döndürülen JSON verisi
    return JsonResponse({
        'device': {
            'id': device.pk,
            'type':device_type,
            'name': device.device_name if device_type == 'printer' else device.computer_name,
            'manufacturer': device.manufacturer,
            'model': device.model,
            'unit': device.unit.name if device.unit else "Belirtilmemiş",
            'image':device.image.url,
            'network_used': device.network_used
        },
        'fault': fault  # Örnek fault verisi (isteğe bağlı)
    })


def search_computer(request):
    computer_name = request.GET.get('computer_name', '')
    if not computer_name:
        return JsonResponse({'error': 'Bilgisayar Adı Boş Olamaz'}, status=400)
    
    # Bilgisayarları isme göre filtreleme
    computers = Computer_Informations.objects.filter(computer_name__icontains=computer_name)
    computer_data = [
        {
        'id': computer.id,
        'computer_name': computer.computer_name or "Belirtilmemiş",
        'manufacturer': computer.manufacturer or "Belirtilmemiş",
        'model': computer.model or "Belirtilmemiş",
        'unit': computer.unit.name if computer.unit else "Belirtilmemiş",
        'network_used': computer.network_used or "Belirtilmemiş"
        }
        for computer in computers
    ]
    return JsonResponse(computer_data, safe=False)

def search_device(request):
    device_name = request.GET.get('device_name', '')
    if not device_name:
        return JsonResponse({'error': 'Cihaz Adı Boş Olamaz'}, status=400)
    
    # Bilgisayarları ve yazıcıları isme göre filtreleme
    computers = Computer_Informations.objects.filter(computer_name__icontains=device_name)
    printers = PrinterScannerInformation.objects.filter(device_name__icontains=device_name)
    
    # Bilgisayar verileri
    computer_data = [
        {
            'id': computer.id,
            'type': 'computer',  # Tip bilgisini ekledik
            'name': computer.computer_name or "Belirtilmemiş",
            'manufacturer': computer.manufacturer or "Belirtilmemiş",
            'model': computer.model or "Belirtilmemiş",
            'unit': computer.unit.name if computer.unit else "Belirtilmemiş",
            'network_used': computer.network_used or "Belirtilmemiş"
        }
        for computer in computers
    ]
    
    # Yazıcı verileri
    printer_data = [
        {
            'id': printer.id,
            'type': 'printer',  # Tip bilgisini ekledik
            'name': printer.device_name or "Belirtilmemiş",
            'manufacturer': printer.manufacturer or "Belirtilmemiş",
            'model': printer.model or "Belirtilmemiş",
            'unit': printer.unit.name if printer.unit else "Belirtilmemiş",
            'network_used': printer.network_used or "Belirtilmemiş"
        }
        for printer in printers
    ]
    
    # Bilgisayar ve yazıcı verilerini birleştirme
    device_data = computer_data + printer_data
    
    # JSON yanıtı
    return JsonResponse(device_data, safe=False)


def search_serial(request):
    serial_number = request.GET['serial_number']
    computers = Computer_Informations.objects.filter(serial_number__icontains=serial_number)
    return render(request, 'bilisim_envanter/computer_list.html', {'computers': computers})

def search_unit(request):
    unit_id = request.GET['unit']
    if unit_id is None or not unit_id.isdigit():       
        computers=Computer_Informations.objects.all()
        paginator=Paginator(computers,30)
        page=request.GET.get('page',1)
        page_obj=paginator.get_page(page)
        context={
            "computers":computers
        }
    else:
        computers = Computer_Informations.objects.filter(unit_id=unit_id)
        context={
            "computers":computers
            }
    return render(request, 'bilisim_envanter/computer_list.html', context)

def search_network_used(request):
    pass

def fault_record_create(request):
    return render(request,'bilisim_envanter/fault_record_create.html')

def save_device_action(request):
    if request.method == "POST":
        # Form verilerini alın
        device_id = request.POST.get("device_id")  # Hem bilgisayar hem de yazıcı için kullanılacak ID
        device_type = request.POST.get("device_type")  # 'computer' veya 'printer'
        request_username = request.POST.get("request_username")
        requester_notes = request.POST.get("requester_notes")
        print(device_id + device_type)
        # Cihazı bulun
        if device_type == "computer":
            device = Computer_Informations.objects.get(pk=device_id)
        elif device_type == "printer":
            device = PrinterScannerInformation.objects.get(pk=device_id)
        else:
            return JsonResponse({'error': 'Geçersiz cihaz türü.'}, status=400)

        # Var olan arıza kaydını kontrol et
        existing_action = FaultAction.objects.filter(
            device_type=device_type, 
            **{f"{device_type}": device}, 
            is_active=True
        ).first()

        # Kullanıcıyı bulun
        try:
            requester = TebsUser.objects.get(username=request_username)
        except TebsUser.DoesNotExist:
            return JsonResponse({'error': 'Geçersiz kullanıcı adı.'}, status=404)

        if existing_action is not None:
            # Açık arıza kaydını güncelle
            existing_action.requester = requester
            existing_action.requester_notes = requester_notes
            existing_action.save()
            return JsonResponse({'success': 'Açık arıza kaydı güncellendi.'}, status=200)

        # Yeni bir arıza kaydı oluştur
        action = FaultAction.objects.create(
            device_type=device_type,
            requester=requester,
            requester_notes=requester_notes,
            **{f"{device_type}": device}  # 'computer' veya 'printer' ilişkisini dinamik olarak ayarla
        )
        action.save()

        return JsonResponse({'success': 'İşlem başarıyla kaydedildi.'}, status=200)

    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)



def finalize_fault_action(request):
    if request.method == "POST":
        action_id = request.POST.get("action_id")
        part_installed = request.POST.get("partInstalled") == 'on'
        os_installed = request.POST.get("osInstalled") == 'on'
        other = request.POST.get("other") == 'on'
        ink_replaced = request.POST.get("ink_replaced") == 'on'
        paper_jam_fixed = request.POST.get("paper_jam_fixed") == 'on'
        hardware_fixed = request.POST.get("hardware_fixed") == 'on'
        software_fixed = request.POST.get("software_fixed") == 'on'
        action_username = request.POST.get("action_username")
        action_notes = request.POST.get("action_notes")
        print(action_id,action_notes,action_username)
        # Check if all required fields are filled
        if not all([action_id, action_username, action_notes]):
            return JsonResponse({'error': 'Lütfen tüm alanları doldurun.'}, status=200)

       
        performer = TebsUser.objects.get(username=action_username)
        existing_action = FaultAction.objects.filter(pk=action_id, is_active=True).first()
        
        if existing_action is None:
            return JsonResponse({'error': 'Aktif arıza kaydı bulunamadı.'}, status=200)
        
        existing_action.part_installed = part_installed
        existing_action.os_installed = os_installed
        existing_action.paper_jam_fixed=paper_jam_fixed
        existing_action.ink_replaced=ink_replaced
        existing_action.hardware_fixed=hardware_fixed
        existing_action.software_fixed=software_fixed
        existing_action.other = other
        existing_action.performer = performer
        existing_action.action_notes = action_notes
        existing_action.is_active = False
        existing_action.completed_date = timezone.now()
        existing_action.save()
        return JsonResponse({'success': 'Arıza kaydı başarıyla sonuçlandırıldı.'}, status=200)
    else:
        return JsonResponse({'error': 'Geçersiz istek.'}, status=400)


def search_user(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.GET.get('username', None)
        user = TebsUser.objects.filter(username=username).first()
        if user:
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'department': user.unit.name
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Kullanıcı bulunamadı.'}, status=404)
    else:
        return JsonResponse({'error': 'Geçersiz istek.'}, status=400)
# views.py



def printer_scanner_list(request):
    printers_scanners = PrinterScannerInformation.objects.filter(is_active=True)
    paginator = Paginator(printers_scanners, 30)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    context = {
        "page_obj": page_obj,
        "printers_scanners": page_obj
    }
    return render(request, 'bilisim_envanter/printer_scanner_list.html', context)

def printer_scanner_detail(request, pk):
    printer_scanner = get_object_or_404(PrinterScannerInformation, pk=pk)
    return render(request, 'bilisim_envanter/printer_scanner_details.html', {'printer_scanner': printer_scanner})

# Arama Fonksiyonları

def search_printer_name(request):
    device_name = request.GET.get('device_name')
    if device_name:
        printers_scanners = PrinterScannerInformation.objects.filter(device_name__icontains=device_name, is_active=True)
    else:
        printers_scanners = PrinterScannerInformation.objects.none()
    return render_printer_scanner_list(request, printers_scanners)

def search_printer_serial(request):
    serial_number = request.GET.get('serial_number')
    if serial_number:
        printers_scanners = PrinterScannerInformation.objects.filter(serial_number__icontains=serial_number, is_active=True)
    else:
        printers_scanners = PrinterScannerInformation.objects.none()
    return render_printer_scanner_list(request, printers_scanners)

def search_printer_unit(request):
    unit_id = request.GET.get('unit')
    if unit_id:
        printers_scanners = PrinterScannerInformation.objects.filter(unit__id=unit_id, is_active=True)
    else:
        printers_scanners = PrinterScannerInformation.objects.none()
    return render_printer_scanner_list(request, printers_scanners)

# Ortak Liste Görünümü Fonksiyonu

def render_printer_scanner_list(request, printers_scanners):
    paginator = Paginator(printers_scanners, 30)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    context = {
        "page_obj": page_obj,
        "printers_scanners": page_obj
    }
    return render(request, 'bilisim_envanter/printer_scanner_list.html', context)



def import_computer_info(request):
    try:
        # PowerShell betiğinin yolunu dışarıdan belirtin veya sabit bir yol kullanın
        powershell_script_path = r"C:\Users\Tunceli BT\Documents\GET.ps1" 
        run_powershell_and_import_data(powershell_script_path)
        return JsonResponse({"status": "success", "message": "Bilgisayar bilgileri başarıyla içe aktarıldı."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
    
def add_printer_scanner(request):
    if request.method == "POST":
        device_name = request.POST.get('device_name')
        manufacturer = request.POST.get('manufacturer')
        model = request.POST.get('model')
        serial_number = request.POST.get('serial_number')
        ip_address = request.POST.get('ip_address')
        connection_interface = request.POST.get('connection_interface')
        unit_id = request.POST.get('unit')
        device_type = request.POST.get('device_type')
        toner_level = request.POST.get('toner_level')
        image = request.FILES.get('image')

        # Unit doğrulama
        unit = Unit.objects.get(pk=unit_id)

        # Yeni cihaz kaydetme
        PrinterScannerInformation.objects.create(
            device_name=device_name,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
            ip_address=ip_address,
            connection_interface=connection_interface,
            unit=unit,
            device_type=device_type,
            toner_level=toner_level,
            image=image
        )

        messages.success(request, "Cihaz başarıyla eklendi!")
        return redirect('printer_scanner_list')  # Liste sayfasına yönlendirin

    units = Unit.objects.all()  # Birimlerin listesini alın
    return render(request, 'bilisim_envanter/add_printer_scanner.html', {'units': units})