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
    # Aktif arızaları çekiyoruz
    active_faults = []
    active_actions = FaultAction.objects.filter(is_active=True,device_type='computer')

    for action in active_actions:
        requester = action.requester
        computer = action.computer
        
        fault_dto = {
            'computer_id': computer.id,
            'requester_username': requester.username if requester else None,
            'requester_notes': action.requester_notes,
            'requester_first_name': requester.first_name if requester else None,
            'requester_last_name': requester.last_name if requester else None,
            'computer_image': computer.image.url if computer.image else None,
            'computer_name': computer.computer_name,
            'computer_manufacturer': computer.manufacturer,
            'computer_model': computer.model,
            'computer_unit_name': computer.unit.name if computer.unit else None,
            'computer_network_used': computer.network_used,
            'action_pk': action.pk
        }
        active_faults.append(fault_dto)

    # Geçmiş arızaları (tamamlanmış son 10 arıza) çekiyoruz
    completed_faults = []
    completed_actions = FaultAction.objects.filter(is_active=False,device_type='computer').order_by('-completed_date')[:10]

    for action in completed_actions:
        requester = action.requester
        performer = action.performer
        computer = action.computer

        
        fault_dto = {
            'computer_id': computer.id,
            'performer_username': performer.username if performer else None,
            'action_notes': action.action_notes,
            'performer_first_name': performer.first_name if performer else None,
            'performer_last_name': performer.last_name if performer else None,
            'computer_image': computer.image.url if computer.image else None,
            'computer_name': computer.computer_name,
            'computer_manufacturer': computer.manufacturer,
            'computer_model': computer.model,
            'computer_unit_name': computer.unit.name if computer.unit else None,
            'computer_network_used': computer.network_used,
            'action_pk': action.pk
        }
        completed_faults.append(fault_dto)

    context = {
        'active_faults': active_faults,
        'completed_faults': completed_faults
    }
    return render(request, 'bilisim_envanter/fault_tracking.html', context)
def fault_summary(request):
    # Bilgisayar arızaları ve tamamlanmış arıza sayısı
    total_computer_faults = FaultAction.objects.all().count()
    completed_computer_faults = FaultAction.objects.filter(is_active=False).count()

    # Yazıcı-Tarayıcı verileri (örnek)
    total_printer_faults = 5  # Örnek sayı
    completed_printer_faults = 2  # Örnek sayı

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
    fault_detail=FaultAction.objects.get(pk=pk)
    print(fault_detail.computer.id)
    return render(request, 'bilisim_envanter/fault_detail.html', {'fault_detail': fault_detail})

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
    fault_dto = None
    computer_id = request.GET.get('computer_id')
    if not computer_id:
        return JsonResponse({'error': 'Bilgisayar ID bulunamadı.'}, status=400)
    
    try:
        computer = Computer_Informations.objects.get(id=computer_id)
    except Computer_Informations.DoesNotExist:
        return JsonResponse({'error': 'Bilgisayar Bulunamadı. İsmi kontrol edin'}, status=404)

    existing_action = FaultAction.objects.filter(computer=computer, is_active=True).first()
    if existing_action:
        requester = TebsUser.objects.get(username=existing_action.requester.username)
        fault_dto = {
            'requester_username': existing_action.requester.username,
            'requester_notes': existing_action.requester_notes,
            'requester_first_name': requester.first_name,
            'requester_last_name': requester.last_name,
        }
    computer_data = {
    'computer_name': computer.computer_name or "Belirtilmemiş",
    'manufacturer': computer.manufacturer if computer.manufacturer else "Belirtilmemiş",
    'model': computer.model or "Belirtilmemiş",
    'unit': computer.unit.name if computer.unit else "Belirtilmemiş",
    'network_used': computer.network_used or "Belirtilmemiş",
    'disk_drive_model': computer.disk_drive_model or "Belirtilmemiş",
    'disk_size_gb': computer.disk_size_gb or "Belirtilmemiş",
    'processor_name': computer.processor_name or "Belirtilmemiş",
    'total_ram_gb': computer.total_ram_gb or "Belirtilmemiş",
    'id': computer.id,
    'image': computer.image.url if computer.image else "Resim yok"
}


    return JsonResponse({'computer': computer_data, 'fault': fault_dto}, status=200)

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



def save_computer_action(request):
    if request.method == "POST":
        # Form verilerini alın
        computer_id = request.POST.get("computer_id")
        request_username = request.POST.get("request_username")
        requester_notes = request.POST.get("requester_notes")
        computer=Computer_Informations.objects.get(pk=computer_id)      
        # Var olan arıza kaydını kontrol et
        existing_action = FaultAction.objects.filter(computer=computer, is_active=True).first()
        # Kullanıcıları bul
        requester = TebsUser.objects.get(username=request_username)
        if existing_action is not None:
            existing_action.device_type='computer'
            existing_action.requester = requester
            existing_action.requester_notes = requester_notes
            existing_action.save()
            return JsonResponse({'success': 'Açık arıza kaydı güncellendi.'}, status=200)
        # Talep edilen işlemi kaydet
        action = FaultAction.objects.create(
            device_type='computer',
            computer=computer,
            requester=requester,
            requester_notes=requester_notes
        )
        action.save() 
        return JsonResponse({'success': 'İşlem başarıyla kaydedildi.'}, status=200)
    else:
        return JsonResponse({'error': 'Geçersiz istek.'}, status=400)



def finalize_computer_action(request):
    if request.method == "POST":
        computer_id = request.POST.get("computer_id")
        part_installed = request.POST.get("partInstalled") == 'on'
        os_installed = request.POST.get("osInstalled") == 'on'
        other = request.POST.get("other") == 'on'
        action_username = request.POST.get("action_username")
        action_notes = request.POST.get("action_notes")
        print(computer_id,action_notes,action_username)
        # Check if all required fields are filled
        if not all([computer_id, action_username, action_notes]):
            return JsonResponse({'error': 'Lütfen tüm alanları doldurun.'}, status=200)

        computer = Computer_Informations.objects.get(pk=computer_id)
        performer = TebsUser.objects.get(username=action_username)
        existing_action = FaultAction.objects.filter(computer=computer, is_active=True).first()
        
        if existing_action is None:
            return JsonResponse({'error': 'Aktif arıza kaydı bulunamadı.'}, status=200)
        
        existing_action.part_installed = part_installed
        existing_action.os_installed = os_installed
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