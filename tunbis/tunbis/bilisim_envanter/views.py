from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from api.services import run_powershell_and_import_data
from bilisim_envanter.forms import ReservationForm
from tunbisapp.models import Computer_Informations, DevicePlan, DeviceType, Reservation, TebsUser, Unit, computer_action, PrinterScannerInformation,FaultAction,DeviceRequest
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
import tempfile
from collections import defaultdict
from io import BytesIO
import json
from django.views.decorators.csrf import csrf_exempt



def index(request):
    context = {
        "total_computers": Computer_Informations.objects.count(),
        "polnet_computers": Computer_Informations.objects.filter(network_used="polnet").count(),
        "internet_computers": Computer_Informations.objects.filter(network_used="internet").count(),

        "total_printers": PrinterScannerInformation.objects.count(),
        "black_white_printers": PrinterScannerInformation.objects.filter(color_mode="Siyah-Beyaz").count(),
        "color_printers": PrinterScannerInformation.objects.filter(color_mode="Renkli").count(),

        "total_faults": FaultAction.objects.count(),
        "pending_faults": FaultAction.objects.filter(is_active=True).count(),
    }
    return render(request, "bilisim_envanter/dashboard.html", context)


def computer_statistics(request):
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


def all_device_requests(request):
     # Bütün birimleri al
    units = Unit.objects.all()

    # Talepleri olan birimleri önce sıralayalım
    sorted_units = sorted(units, key=lambda unit: DeviceRequest.objects.filter(unit=unit).count(), reverse=True)

    # Her bir birime ait talepleri dictionary olarak toplayalım
    unit_requests = {unit: DeviceRequest.objects.filter(unit=unit, is_active = True).order_by("-request_date") for unit in sorted_units}

    # Sayfalama işlemi için bir liste oluşturalım (her birim taleplerini bir listeye koyacağız)
    paginated_data = []
    for unit, requests in unit_requests.items():
        if requests.exists():  # Eğer birimde talep varsa listeye ekle
            paginated_data.append((unit, requests))

    # Sayfalama için Django Paginator kullan
    page_number = request.GET.get("page", 1)  # URL'den sayfa numarasını al
    paginator = Paginator(paginated_data, 30)  # Her sayfada 5 birim gösterelim

    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)  # Geçersiz sayfa olursa ilk sayfayı göster

    return render(request, "bilisim_envanter/all_device_requests.html", {"page_obj": page_obj})

def device_request(request):
    if request.method == "POST":
        unit_id = request.POST.get("unit")
        device_type = request.POST.get("device_type")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")

        # Birimi getir
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            messages.error(request, "Seçilen birim bulunamadı.")
            return redirect("device_request_create")
        
          # "Bilgi İşlem Yöneticisi" olan kullanıcıyı çek
        try:
            admin_user = TebsUser.objects.get(username="1")
        except TebsUser.DoesNotExist:
            messages.error(request, "Bilgi İşlem Yöneticisi bulunamadı.")
            return redirect("device_request_create")

        # Talebi oluştur
        DeviceRequest.objects.create(
            unit=unit,
            requester=admin_user,  # Admin kendisi oluşturuyor
            device_type=device_type,
            quantity=quantity,
            description=description,
            status="Bekliyor",
        )

        messages.success(request, "Talep başarıyla oluşturuldu.")
        return redirect("all_device_requests")

    units = Unit.objects.all()
    device_types = DeviceType.choices  # Modelde tanımlı cihaz türlerini al

    return render(request, "bilisim_envanter/device_request_create.html", {"units": units, "device_types": device_types})



@csrf_exempt
def update_device_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request_id = data.get("request_id")
            new_status = data.get("new_status")

            device_request = get_object_or_404(DeviceRequest, id=request_id)
            device_request.status = new_status
            device_request.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Geçersiz istek"}, status=400)

def device_request_summary(request):
    # Tüm birimleri al
    units = Unit.objects.all()

    # Cihaz tiplerine göre talepleri gruplayarak say
    device_types = dict(DeviceType.choices)  # Cihaz türleri
    requests_by_unit = DeviceRequest.objects.filter(is_active=True).values('unit__name', 'device_type')\
        .annotate(total=Sum('quantity'))\
        .order_by('unit__name')

    # Verileri işleyerek bir sözlük yapısına dönüştür
    unit_data = {unit.name: {device: 0 for device in device_types.values()} for unit in units}
    
    for entry in requests_by_unit:
        unit_name = entry['unit__name']
        device_name = device_types.get(entry['device_type'])
        unit_data[unit_name][device_name] = entry['total']

    context = {
        'unit_data': unit_data,
        'device_types': device_types.values()
    }
    return render(request, 'bilisim_envanter/device_request_summary.html', context)

def device_request_pdf(request):
    # Cihaz türleri ve birimler
    units = Unit.objects.all()
    device_types = dict(DeviceType.choices)
    
    # Talepleri gruplandır
    requests_by_unit = DeviceRequest.objects.filter(is_active=True).values('unit__name', 'device_type')\
        .annotate(total=Sum('quantity'))\
        .order_by('unit__name')

    # Verileri işleyerek toplamları hesapla
    unit_data = {unit.name: {device: 0 for device in device_types.values()} for unit in units}
    total_per_device = {device: 0 for device in device_types.values()}  # Cihaz bazlı toplam
    
    for entry in requests_by_unit:
        unit_name = entry['unit__name']
        device_name = device_types.get(entry['device_type'])
        unit_data[unit_name][device_name] = entry['total']
        total_per_device[device_name] += entry['total']  # Toplamları hesapla

    # Tüm satırların toplam değerini kontrol ederek 0 olanları filtrele
    filtered_unit_data = {unit: devices for unit, devices in unit_data.items() if any(value > 0 for value in devices.values())}

    context = {
        'unit_data': filtered_unit_data,
        'device_types': device_types.values(),
        'total_per_device': total_per_device,  # PDF'de göstermek için toplamları gönder
        'current_date': timezone.now()
    }

    # HTML to PDF
    html_string = render_to_string("bilisim_envanter/_pdf/device_request_pdf.html", context)
    pdf = HTML(string=html_string).write_pdf()

    # HTTP Response
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=request_summary.pdf"

    return response



def add_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_reservation')  # Başarılı ekleme sonrası aynı sayfaya dön
    else:
        form = ReservationForm()

    reservations = Reservation.objects.all().order_by('-received_date')  # Son eklenenler üstte
    return render(request, 'bilisim_envanter/add_reserv_device.html', {'form': form, 'reservations': reservations})

def warehouse_inventory(request):
# Depodaki aktif cihazları listele (adet > 0)
    inventory = Reservation.objects.filter(quantity__gt=0).order_by('device_type', 'brand')

    return render(request, 'bilisim_envanter/warehouse_inventory.html', {'inventory': inventory})

def edit_reservation(request):
    pass
def delete_reservation(request):
    pass

def planning_list(request):
    """Planlama geçmişini listeler"""
    plans = DevicePlan.objects.filter(is_active=True).order_by('-created_at')  # Sadece aktif planları getir
    return render(request, 'bilisim_envanter/planning_list.html', {'plans': plans})

def delivered(request, plan_id):
    """Planı tamamlanmış olarak işaretler"""
    plan = get_object_or_404(DevicePlan, id=plan_id)
    plan.is_active = False
    plan.save()
    return redirect('planlama_list')


def allocation_screen(request):
    """Tahsis ekranını gösterir"""
    units = Unit.objects.all()
    selected_unit = None
    existing_computers = []
    existing_printers = []
    unit_requests = []
    
    if request.method == "POST":
        unit_id = request.POST.get("unit_id")
        device_type = request.POST.get("device_type")
        quantity = int(request.POST.get("tahsis_adedi", 0))

        if unit_id and device_type and quantity > 0:
            unit = get_object_or_404(Unit, id=unit_id)
            
    # Talebi kontrol et, yoksa 0 döndür
            requested = DeviceRequest.objects.filter(device_type=device_type, unit=unit_id).first()
    
    # Eğer talep bulunmazsa, requested.quantity 0 olarak ayarlanır
            requested_quantity = requested.quantity if requested else 0
            
            # Yeni DevicePlan kaydı oluştur
            device_plan = DevicePlan.objects.create(
                unit=unit,
                device_type=device_type,
                requested_quantity=requested_quantity,
                allocated_quantity=quantity
            )

            # Depodaki rezervleri düş
            available_reservations = Reservation.objects.filter(device_type=device_plan.device_type, is_allocated=False)
            for reservation in available_reservations:
                if quantity <= 0:
                    break
                if reservation.quantity <= quantity:
                    quantity -= reservation.quantity
                    reservation.is_allocated = True
                    reservation.save()
                else:
                    reservation.quantity -= quantity
                    reservation.save()
                    quantity = 0

            return redirect('planning_list')

    return render(request, 'bilisim_envanter/allocation_screen.html', {
        "units": units,
        "selected_unit": selected_unit,
        "existing_computers": existing_computers,
        "existing_printers": existing_printers,
        "unit_requests": unit_requests
    })


def get_unit_data(request, unit_id):
    """AJAX ile birim seçildiğinde ilgili verileri döner"""
    unit = get_object_or_404(Unit, id=unit_id)
    
    existing_computers = list(Computer_Informations.objects.filter(unit=unit, is_active=True).values(
        "computer_name", "model", "number_of_cores", "manufacturer", "serial_number","total_ram_gb","network_used"
    ))
    
    existing_printers = list(PrinterScannerInformation.objects.filter(unit=unit, is_active=True).values(
        "device_name", "model", "manufacturer", "serial_number"
    ))

    # DeviceRequest içindeki device_type stringini Türkçe label ile eşleştir
    unit_requests = list(DeviceRequest.objects.filter(unit=unit).values("device_type", "quantity"))

      # Depodaki cihazları çek (Dropdown için)
    stock_devices = Reservation.objects.filter(is_allocated=False).values("device_type", "brand", "model", "quantity")
    

    for request in unit_requests:
        request["device_type_name"] = DeviceType(request["device_type"]).label if request["device_type"] in DeviceType.values else "Bilinmeyen Cihaz"
    print(stock_devices)
    return JsonResponse({
        "computers": list(existing_computers),
        "printers": list(existing_printers),
        "requests": list(unit_requests),
        "stock_devices": list(stock_devices)
    })


def edit_plan(request, plan_id):
    plan = get_object_or_404(DevicePlan, id=plan_id)
    
    if request.method == 'POST':
        new_allocated_quantity = int(request.POST.get('allocated_quantity'))
        
        # Depodaki mevcut rezervasyonları geri al
        available_reservations = Reservation.objects.filter(device_type=plan.device_type)
        quantity_to_return = plan.allocated_quantity - new_allocated_quantity
        
        # Rezervasyonları geri al (tersine işlemler)
        for reservation in available_reservations:
            if quantity_to_return <= 0:
                break
            if reservation.quantity <= quantity_to_return:
                quantity_to_return -= reservation.quantity
                reservation.is_allocated = False
                reservation.save()
            else:
                reservation.quantity += quantity_to_return
                reservation.save()
                quantity_to_return = 0

        # Plan'ı güncelle
        plan.allocated_quantity = new_allocated_quantity
        plan.save()

        # Yeni rezervasyonları ekle
        available_reservations = Reservation.objects.filter(device_type=plan.device_type)
        quantity_to_allocate = new_allocated_quantity
        for reservation in available_reservations:
            if quantity_to_allocate <= 0:
                break
            if reservation.quantity <= quantity_to_allocate:
                quantity_to_allocate -= reservation.quantity
                reservation.is_allocated = True
                reservation.save()
            else:
                reservation.quantity -= quantity_to_allocate
                reservation.is_allocated = True
                reservation.save()
                quantity_to_allocate = 0

        return redirect('planning_list')  # Gerçekten geri gitmek istediğiniz sayfayı buraya yazabilirsiniz.

    return render(request, 'bilisim_envanter/edit_plan.html', {'plan': plan})
from collections import defaultdict
def cancel_plan(request, plan_id):
    plan = get_object_or_404(DevicePlan, id=plan_id)
    
    # Depodaki mevcut rezervasyonları geri ekle
    reservation = Reservation.objects.filter(device_type=plan.device_type).first()

    # Plan'dan tahsis edilen tüm cihazları geri ekle
    reservation.quantity += plan.allocated_quantity
    reservation.save()
    plan.is_active=False    
    plan.save()
    return redirect('planning_list')


def planning_pdf(request):
    # Monitör (display) hariç tüm planları getir
    plans = DevicePlan.objects.filter(
    Q(device_type='computer') | Q(device_type='color_printer_scanner'),
    is_active=True
)
    
    # DeviceType choices değerlerini al (MODEL ÜZERİNDE TANIMLI OLAN)
    DEVICE_TYPE_CHOICES = dict(DeviceType.choices)  # Örneğin: {'laptop': 'Laptop', 'printer': 'Yazıcı'}
    
    # Cihaz türlerini choices üzerinden al ve liste olarak oluştur
    device_types = [key for key in DEVICE_TYPE_CHOICES.keys() if key in ['computer', 'color_printer_scanner']]


    # Cihaz türüne göre toplam tahsis miktarlarını hesapla
    total_allocations = defaultdict(int)
    unit_data = {}

    for plan in plans:
        unit_name = plan.unit.name  # Birim adı
        device_type = plan.device_type  # Cihaz türü (örneğin 'laptop', 'printer')

        if unit_name not in unit_data:
            unit_data[unit_name] = {dtype: {'requested': 0, 'allocated': 0} for dtype in device_types}

        unit_data[unit_name][device_type]['requested'] += plan.requested_quantity
        unit_data[unit_name][device_type]['allocated'] += plan.allocated_quantity
        total_allocations[device_type] += plan.allocated_quantity

    # PDF şablonuna veri gönder
    html_template = 'bilisim_envanter/_pdf/planning_pdf.html'
    html_content = render(request, html_template, {
        'unit_data': unit_data,
        'device_types': device_types,
        'device_type_labels': DEVICE_TYPE_CHOICES,
        'current_date': timezone.now(),
        'total_allocations': total_allocations
    })

    # WeasyPrint ile PDF oluştur
    pdf_file = BytesIO()
    HTML(string=html_content.content.decode()).write_pdf(pdf_file)

    # PDF'yi HttpResponse ile döndür
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="planlama_gecmisi.pdf"'
    return response
