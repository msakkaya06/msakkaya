from datetime import date, timedelta
from django.db import models
from django.utils.text import slugify 
from django.utils.formats import number_format
from django.contrib.auth.models import AbstractUser,Group
from django.utils import timezone


# Create your models here.
class InfoCard(models.Model):
    title = models.CharField(max_length=100)
    description=models.TextField()
    imageUrl=models.CharField(max_length=50,blank=False,null=True)
    date=models.DateField()
    isActive=models.BooleanField()
    slug=models.SlugField(default="",blank=True, null=False,unique=True,db_index=True)
    totalBudget=models.DecimalField(null=True,max_digits=11,decimal_places=2)
    spentBudget=models.DecimalField(null=True,max_digits=11,decimal_places=2)
    remainingBudget=models.DecimalField(null=True,max_digits=11,decimal_places=2)
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        if self.totalBudget != 0:
            self.remainingBudget=self.totalBudget-self.spentBudget
        super().save(args,kwargs)

    def __str__(self):
        return f"{self.title} {self.date} {number_format(self.totalBudget, use_l10n=True)}"
class TebsGroup(models.Model):
    original_group = models.OneToOneField(Group, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'tebs_group'

    def __str__(self):
        return self.display_name or self.original_group.name
    

class Unit(models.Model):
    name=models.TextField()
    parent_unit=models.IntegerField(null=True)
    super_unit=models.BooleanField(default=False) # Şube Müdürlükleri ve İl Emniyet Müdürlüğü için bu alan kullanılacak.
    is_active=models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
    def __str__(self):
        return self.name



class TebsUser(AbstractUser):
    image = models.ImageField(null=True, upload_to="img", blank=True)
    registration_number = models.CharField(max_length=8)
    telephone_number = models.CharField(max_length=20)
    is_passive = models.BooleanField(default=False, null=True)
    passive_description = models.TextField(null=True, blank=True)
    temp_duty_station = models.TextField(null=True, blank=True)
    rank = models.CharField(max_length=50, null=True)
    birthday = models.DateField(default=date.today, blank=True,null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Şifre yönetimi için ek alanlar
    password_last_changed = models.DateField(auto_now_add=True)  # Şifrenin en son ne zaman değiştirildiğini kaydeder
    force_password_change = models.BooleanField(default=False)  # İlk girişte parola değişikliği zorunlu mu?
    SECURITY_QUESTIONS = [
        ('food', 'En Sevdiğiniz Yemek'),
        ('book', 'En Sevdiğiniz Kitap'),
        ('teacher', 'İlkokul Öğretmeninizin Adı'),
        ('car', 'İlk Arabanızın Markası'),
        ('movie', 'En Sevdiğiniz Film'),
        ('friend', 'En Yakın Arkadaşınızın Adı'),
    ]
    
    security_question = models.CharField(max_length=50, choices=SECURITY_QUESTIONS, blank=True, null=True)
    security_answer = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Kullanıcı kaydı sırasında registration_number'ı username olarak ayarla
        if self.registration_number:
            self.username = self.registration_number

        # Şifre hashlenmemişse, set_password metodunu çağırarak hashle
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

        super().save(*args, **kwargs)

    def check_password_expiration(self):
        """Şifre değişim periyodu dolmuş mu kontrol eder (örneğin, 90 gün)"""
        expiration_period = timedelta(days=90)
        if date.today() - self.password_last_changed >= expiration_period:
            return True
        return False




class Personnel_Assignment(models.Model):
    national_identity_number=models.CharField(max_length=11)
    registration_number=models.CharField(max_length=10)
    rank=models.CharField(max_length=50)
    first_last_name=models.CharField(max_length=150)
    assigned_unit=models.TextField()
    def save(self, *args, **kwargs):
        super().save(args,kwargs)



class Computer_Informations(models.Model):
    computer_name = models.CharField(max_length=75)
    manufacturer = models.CharField(max_length=75, blank=True, null=True)
    model = models.CharField(max_length=75, blank=True, null=True)
    number_of_processors = models.CharField(max_length=75, blank=True, null=True)
    system_type = models.CharField(max_length=75, blank=True, null=True)
    serial_number = models.CharField(max_length=75, blank=True, null=True)
    processor_name = models.CharField(max_length=75, blank=True, null=True)
    number_of_cores = models.CharField(max_length=75, blank=True, null=True)
    max_clock_speed_ghz = models.CharField(max_length=75, blank=True, null=True)
    graphics_card = models.CharField(max_length=75, blank=True, null=True)
    bios_version = models.CharField(max_length=75, blank=True, null=True)
    product = models.CharField(max_length=75, blank=True, null=True)
    base_board_serial_number = models.CharField(max_length=75, blank=True, null=True)
    number_of_memory_slots = models.CharField(max_length=75, blank=True, null=True)
    total_ram_gb = models.CharField(max_length=75, blank=True, null=True)
    used_ram_slots = models.CharField(max_length=75, blank=True, null=True)
    ip_address = models.CharField(max_length=75, blank=True, null=True)
    disk_drive_model = models.CharField(max_length=75, blank=True, null=True)
    disk_size_gb = models.CharField(max_length=75, blank=True, null=True)
    media_type = models.CharField(max_length=75, blank=True, null=True)
    disk_partition_name = models.CharField(max_length=75, blank=True, null=True)
    operating_system = models.CharField(max_length=75, blank=True, null=True)
    os_version = models.CharField(max_length=75, blank=True, null=True)
    os_build_number = models.CharField(max_length=75, blank=True, null=True)
    office_version = models.CharField(max_length=75, blank=True, null=True)
    office_license_status = models.CharField(max_length=75, blank=True, null=True)
    disk_usage_percentage = models.CharField(max_length=75, blank=True, null=True)
    ram_brands = models.CharField(max_length=75, blank=True, null=True)
    average_ram_speed = models.CharField(max_length=75, blank=True, null=True)
    ram_slot_types = models.CharField(max_length=75, blank=True, null=True)
    image = models.ImageField(null=True, upload_to="img", blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    network_used = models.CharField(max_length=75, blank=True, null=True, choices=(
        ('Internet', 'Internet'),
        ('PolNet', 'PolNet'),
        ('KGYS', 'KGYS')
    ))

    def __str__(self):
        return self.computer_name + self.manufacturer

    def save(self, *args, **kwargs):
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)



class computer_action(models.Model):
    computer = models.ForeignKey(Computer_Informations, on_delete=models.CASCADE, related_name='actions')
    part_installed = models.BooleanField(default=False, verbose_name="Parça Takıldı")
    os_installed = models.BooleanField(default=False, verbose_name="İşletim Sistemi Kuruldu")
    other=models.BooleanField(default=False, verbose_name="Diğer İşlemler")
    # Diğer işlemler için gerekli boolean alanlar buraya eklenebilir
    requester_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    performer = models.ForeignKey(TebsUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_actions')
    requester = models.ForeignKey(TebsUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_actions')
    action_notes = models.TextField(blank=True)
    requester_notes=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"Işlemler for {self.computer.computer_name}"

    class Meta:
        verbose_name_plural = "Computer Actions"



class FaultAction(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('computer', 'Bilgisayar'),
        ('printer', 'Yazıcı/Tarayıcı'),
        ('tablet', 'Tablet'),
    ]

    # Cihaz türü ve cihaz ile ilişkili alanlar
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    computer = models.ForeignKey('Computer_Informations', on_delete=models.CASCADE, null=True, blank=True, related_name='fault_actions')
    printer = models.ForeignKey('PrinterScannerInformation', on_delete=models.CASCADE, null=True, blank=True, related_name='fault_actions')
    
    # Bilgisayar için özel alanlar
    part_installed = models.BooleanField(default=False, null=True, verbose_name="Parça Takıldı")
    os_installed = models.BooleanField(default=False, null=True, verbose_name="İşletim Sistemi Kuruldu")

    # Yazıcı için özel alanlar
    ink_replaced = models.BooleanField(default=False,null=True, verbose_name="Kartuş Değiştirildi")
    paper_jam_fixed = models.BooleanField(default=False,null=True, verbose_name="Kağıt Sıkışması Giderildi")
    hardware_fixed = models.BooleanField(default=False,null=True, verbose_name="Donanım Sorunu Giderildi")
    software_fixed = models.BooleanField(default=False,null=True, verbose_name="Yazılım Sorunu Giderildi")



    # Ortak işlemler
    other = models.BooleanField(default=False, verbose_name="Diğer İşlemler",null=True)
    action_notes = models.TextField(blank=True, verbose_name="İşlem Notları",null=True)
    requester_notes = models.TextField(blank=True, verbose_name="Talep Eden Notları")
    requester_date = models.DateTimeField(auto_now_add=True, verbose_name="Talep Tarihi")
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name="Tamamlanma Tarihi")
    performer = models.ForeignKey('TebsUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_fault_actions', verbose_name="İşlemi Yapan")
    requester = models.ForeignKey('TebsUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_fault_actions', verbose_name="Talep Eden")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    def __str__(self):
        if self.device_type == 'computer' and self.computer:
            return f"FaultAction for Computer: {self.computer.computer_name}"
        elif self.device_type == 'printer' and self.printer:
            return f"FaultAction for Printer: {self.printer.device_name}"
        return "FaultAction"

    class Meta:
        verbose_name_plural = "Fault Actions"




class PrinterScannerInformation(models.Model):
    DEVICE_TYPE_CHOICES = (
        ('Printer', 'Printer'),
        ('Scanner', 'Scanner'),
        ('Printer-Scanner', 'Printer-Scanner'),
        ('All-In-One Printers', 'All-In-One Printers'),
    )
    
    COLOR_MODE_CHOICES = (
        ('Renkli', 'Color'),
        ('Siyah-Beyaz', 'Monochrome'),
    )

    NETWORK_CHOICES = (
        ('Internet', 'Internet'),
        ('PolNet', 'PolNet'),
        ('KGYS', 'KGYS'),
    )

    CONNECTION_INTERFACE_CHOICES = (
        ('LAN', 'LAN'),
        ('USB', 'USB'),
    )

    device_type = models.CharField(max_length=75, choices=DEVICE_TYPE_CHOICES, default='Printer')
    device_name = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=75, blank=True, null=True)
    serial_number = models.CharField(max_length=75, blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    network_used = models.CharField(max_length=75, blank=True, null=True, choices=NETWORK_CHOICES)
    
    color_mode = models.CharField(max_length=20, choices=COLOR_MODE_CHOICES, default='Siyah-Beyaz')
    print_speed_ppm = models.IntegerField(blank=True, null=True, help_text="Dakikada basılan sayfa sayısı (PPM)")
    scan_speed_ipm = models.IntegerField(blank=True, null=True, help_text="Dakikada taranan görüntü sayısı (IPM)")
    max_resolution_dpi = models.IntegerField(blank=True, null=True, help_text="Maksimum çözünürlük (DPI)")
    
    duplex = models.BooleanField(default=False, help_text="Çift taraflı baskı/tarama desteği var mı?")
    wireless_capability = models.BooleanField(default=False, help_text="Kablosuz bağlantı desteği var mı?")
    paper_capacity = models.IntegerField(blank=True, null=True, help_text="Kağıt kapasitesi (sayfa)")
    connection_interface = models.CharField(max_length=10, choices=CONNECTION_INTERFACE_CHOICES, default='LAN', help_text="Bağlantı Arayüzü")
    
    toner_level = models.CharField(max_length=10, blank=True, null=True, help_text="Toner doluluk oranı (%)")
    drum_unit_life_remaining = models.CharField(max_length=10, blank=True, null=True, help_text="Drum ünitesinin kalan ömrü (%)")
    scan_unit_life_remaining = models.CharField(max_length=10, blank=True, null=True, help_text="Tarayıcı ünitesinin kalan ömrü (%)")
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(null=True, upload_to="img", blank=True)

    def save(self, *args, **kwargs):
        # Bağlantı arayüzü USB ise IP adresini 127.0.0.1 olarak ayarla
        if self.connection_interface == 'USB':
            self.ip_address = '127.0.0.1'
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device_name} ({self.device_type})"

class PrinterAction(models.Model):
    FAULT_TYPE_CHOICES = (
        ('paper_jam', 'Kağıt Sıkışması'),
        ('ink_toner', 'Toner veya Kartuş Sorunu'),
        ('hardware', 'Donanım Arızası'),
        ('software', 'Yazılım Sorunu'),
        ('network', 'Ağ Bağlantı Sorunu'),
        ('other', 'Diğer'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Beklemede'),
        ('in_progress', 'İşlemde'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    )
    
    printer = models.ForeignKey(PrinterScannerInformation, on_delete=models.CASCADE, related_name='actions', verbose_name="Yazıcı")
    fault_type = models.CharField(max_length=20, choices=FAULT_TYPE_CHOICES, default='other', verbose_name="Arıza Türü")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Arıza Durumu")
    toner_replaced = models.BooleanField(default=False, verbose_name="Toner Değiştirildi")
    firmware_updated = models.BooleanField(default=False, verbose_name="Firmware Güncellendi")
    other = models.BooleanField(default=False, verbose_name="Diğer İşlemler")
    requester_date = models.DateTimeField(auto_now_add=True, verbose_name="Talep Tarihi")
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name="Tamamlanma Tarihi")
    performer = models.ForeignKey(TebsUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_printer_actions', verbose_name="İşlem Yapan")
    requester = models.ForeignKey(TebsUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='requested_printer_actions', verbose_name="Talep Eden")
    action_notes = models.TextField(blank=True, verbose_name="İşlem Notları")
    requester_notes = models.TextField(blank=True, verbose_name="Talep Notları")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    def __str__(self):
        return f"Printer Action for {self.printer.printer_name} - {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "Printer Actions"


class DeviceType(models.TextChoices):
    COMPUTER = "computer", "Bilgisayar"
    DISPLAY = "display", "Monitör"
    PRINTER = "printer", "Yazıcı"
    COLOR_PRINTER = "color_printer", "Renkli Yazıcı"
    SCANNER = "scanner", "Tarayıcı"
    COLOR_PRINTER_SCANNER = 'color_printer_scanner', 'Çok Fonksiyonlu Renkli Yazıcı / Tarayıcı'
    PRINTER_SCANNER = "printer_scanner",'Çok Fonksiyonlu Siyah Beyaz Yazıcı / Tarayıcı'
    TABLET = 'tablet', 'Tablet Bilgisayar'
    SWITCH = 'switch',"Network Switch Cihazı"



class DeviceRequest(models.Model):
    """Birimlerin yaptığı cihaz taleplerini yönetir"""

    # Talep Durumları (RequestStatus yerine)
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
        ('delivered', 'Teslim Edildi'),
    ]

    requester = models.ForeignKey('TebsUser', on_delete=models.CASCADE)  # Talebi yapan kullanıcı
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)  # Talep hangi birim tarafından yapıldı?
    device_type = models.CharField(max_length=50, choices=DeviceType.choices)  # **GÜNCELLENDİ**
    quantity = models.PositiveIntegerField(default=1)  # Talep edilen cihaz adedi
    description = models.TextField(blank=True, null=True)  # Açıklama (Opsiyonel)
    request_date = models.DateTimeField(default=timezone.now)  # Talep oluşturulma zamanı
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Talep durumu
    response_note = models.TextField(blank=True, null=True)  # Talep onay/red notu
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    def __str__(self):
        return f"{self.unit} - {self.get_device_type_display()} ({self.quantity})"

class Reservation(models.Model):
    device_type = models.CharField(max_length=50, choices=DeviceType.choices)
    brand = models.CharField(max_length=100,null=True)  # Marka
    model = models.CharField(max_length=100, null=True)  # Model
    serial_number = models.CharField(max_length=100, null=True)  # Seri numarası
    quantity = models.PositiveIntegerField()
    received_date = models.DateTimeField(auto_now_add=True)  # Depoya giriş tarihi
    is_allocated = models.BooleanField(default=False)  # Tahsis edildi mi?

    def __str__(self):
        return f"{self.brand} {self.model} ({self.get_device_type_display()}) - {self.quantity} adet (Depoda)"

class Inventory(models.Model):
    device_type = models.CharField(max_length=50, choices=DeviceType.choices)
    brand = models.CharField(max_length=100,null=True)  # Marka
    model = models.CharField(max_length=100, null=True)  # Model
    serial_number = models.CharField(max_length=100, null=True)  # Seri numarası
    quantity = models.PositiveIntegerField()
    allocated_to = models.ForeignKey("Unit", on_delete=models.CASCADE)  # Hangi birime tahsis edildi?
    allocated_date = models.DateTimeField(auto_now_add=True)  # Tahsis tarihi

    def __str__(self):
        return f"{self.allocated_to} - {self.brand} {self.model} ({self.get_device_type_display()}) ({self.quantity} adet)"


class DevicePlan(models.Model):
    """Planlanan tahsisleri yönetir"""
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)  # Hangi birime tahsis yapıldı?
    device_type = models.CharField(max_length=50, choices=DeviceType.choices)  # Cihaz türü
    requested_quantity = models.PositiveIntegerField()  # Talep edilen adet
    allocated_quantity = models.PositiveIntegerField(default=0)  # Tahsis edilen adet
    is_active = models.BooleanField(default=True)  # Planın tamamlanıp tamamlanmadığını kontrol eder
    created_at = models.DateTimeField(auto_now_add=True)  # Planlama tarihi

    def __str__(self):
        return f"{self.unit} - {self.get_device_type_display()} ({self.allocated_quantity}/{self.requested_quantity})"
