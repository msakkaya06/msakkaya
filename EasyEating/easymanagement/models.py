import asyncio
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Business(models.Model):
    name=models.CharField(max_length=150)
    telephone=models.CharField(max_length=30)
    adress=models.TextField(null=True)
    isActive=models.BooleanField()
    registerDate=models.DateField(auto_now=True)
    slug=models.SlugField(default="",blank=True, null=False,unique=True,db_index=True)

    def save(self, *args):
        self.slug=slugify(self.name)
        self.create_group()
        super().save(args)
        
        if self.pk is None:
            # Yeni bir işletme oluşturulursa WebSocket grubu oluştur
            self.create_group()

    def create_group(self):
        channel_layer = get_channel_layer()
        group_name = f"business_{self.id}"
        # Grubu oluşturmak için basit bir mesaj gönderimi
        try:
            async_to_sync(channel_layer.group_add)(group_name, "dummy_channel")
        except:
            pass

    def __str__(self):
        return f"{self.name}"
    


class EEUser(AbstractUser):
    image = models.ImageField(null=True, upload_to="img")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    is_manager = models.BooleanField(default=0)
    is_desk = models.BooleanField(default=0)
    token = models.CharField(max_length=255, null=True, blank=True)  # unique=True kullanmayın

    def save(self, *args, **kwargs):
        if not self.pk or self.password:# Şifre düz metin olarak mı?
                self.password=make_password(self.password)
        super().save(*args, **kwargs)

        

class Desk(models.Model):
    name = models.CharField(max_length=50)
    isReserve=models.BooleanField(default=False)
    isActive=models.BooleanField(default=True)
    slug=models.SlugField(default="",blank=True, null=False,unique=True,db_index=True)
    business=models.ForeignKey(Business, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new_desk=False
        self.slug = slugify(f"{self.business}  {self.name}")
        if self.pk is None:
            is_new_desk = True # Masa yeni mi oluşturuluyor?


        super().save(*args, **kwargs)  # Masa nesnesini önce kaydet
        if is_new_desk:
            # Eğer masa yeni oluşturuluyorsa veya 'update_fields' belirtilmemişse veya 'isReserve' güncellenmemişse
            password = "kolaymasa"
            EEUser.objects.create(username=self.slug, password=password, is_desk=True, business=self.business)
    

    def __str__(self):
        return f"{self.name}"
    

class WebSocketGroup(models.Model):
    name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(EEUser, related_name='websocket_groups')

    def __str__(self):
        return self.name
    
    
class ProduceType(models.Model):
    name=models.CharField(max_length=25)
    isActive=models.BooleanField()
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True, max_length=150)
    business=models.ForeignKey(Business, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"{self.name}"
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.business}  {self.name}")
        super().save(*args, **kwargs)

# Düşük boyutlu bir resim için bir fonksiyon
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    # resmi RGB moduna dönüştürme (gerektiğinde)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    # resmi boyutlandırma ve kaydetme
    im.thumbnail((300, 300))
    im.save(im_io, format='JPEG', quality=70) # kaliteyi 70 olarak ayarladık
    new_image = InMemoryUploadedFile(im_io, None, 'foo.jpg', 'image/jpeg', sys.getsizeof(im_io), None)
    return new_image

class Produce(models.Model):
    name = models.CharField(max_length=75)
    produceType = models.ForeignKey(ProduceType, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, max_digits=11, decimal_places=2)
    image = models.ImageField(null=True, upload_to="img")
    description=models.TextField(default="")
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProduceStock(models.Model):
    piece = models.IntegerField()
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE, related_name='stocks')

    def __str__(self):
        return f"{self.produce.name} - Stock: {self.piece}"


class Order(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    produces = models.ManyToManyField(Produce, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    STATUS_CHOICES = (
        ('preparing', 'Hazırlanıyor'),
        ('serving', 'Servis Edildi'),
        ('completed', 'Tamamlandı'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')

    payment_status = models.BooleanField(default=False)  # Ödeme yapıldı mı?
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_total_price(self):
        """Order'ın total_price değerini günceller."""
        self.total_price = sum([item.quantity * item.unit_price for item in self.orderitem_set.all()])
        self.save(update_fields=['total_price'])  # Sadece total_price alanını güncelle

    

    def __str__(self):
        return f"Sipariş {self.id} - Masa: {self.desk}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    isRead = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # O anki ürün fiyatı

    def __str__(self):
        return f"Order: {self.order.id}, Produce: {self.produce.name}, Quantity: {self.quantity}"


class Cart(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    produces = models.ManyToManyField(Produce, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    isConfirm=models.BooleanField(default=False)
    isActive=models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Toplam ödeme
    

    def __str__(self):
        return f"Sepet {self.id} - Masa: {self.desk}"
    
    def calculate_total_price(self):
        # Her sipariş kaleminin fiyatını ve miktarını alarak toplam fiyatı hesaplar
        self.total_price = sum([item.quantity * item.unit_price for item in self.cartitem_set.all()])
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    isConfirm=models.BooleanField(default=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # O anki ürün fiyatı

    def __str__(self):
        return f"Cart: {self.cart.id}, Produce: {self.produce.name}, Quantity: {self.quantity}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Her ödeme bir siparişe bağlı
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Ödeme tutarı
    method = models.CharField(max_length=10, choices=[
        ('cash', 'Nakit'),
        ('card', 'Kredi/Banka Kartı'),
        ('other', 'Diğer')
    ],default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Kart ödemelerinde işlem ID
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ödeme kaydedildiğinde siparişin ödeme durumunu güncelle
        self.order.payment_status = True
        super().save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        return f"Ödeme: {self.amount} TL - {self.method} - Sipariş {self.order.id}"
