from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from easymanagement.models import CartItem, Desk, Order, OrderItem, Produce, ProduceType,Cart
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from logging_helper.performance_logger import log_performance

def isDesk(user):
    return user.is_desk


# Create your views here.
@login_required
@user_passes_test(isDesk)
@log_performance('Order_Index')
def index(req):
    business = req.user.business
    username = Desk.objects.get(slug=req.user.username)
    produce_types = ProduceType.objects.filter(business=business)
    cart_exist = Cart.objects.filter(desk__slug=req.user.username, isActive=True).exists()

    if not cart_exist:  # Eğer mevcut bir sepet yoksa
        cart_result = create_cart(req)  # Sepeti oluştur
        if cart_result != "success":  # Sepet oluşturma başarısız olduysa
            return JsonResponse({'success': False, 'message': 'Sepet oluşturma işleminde hata oluştu. Restoran yetkilisi ile görüşün'})

    # Sepeti oluşturmak için gerekli diğer işlemler
    produce_dict = {}
    for produce_type in produce_types:
        produces = Produce.objects.filter(produceType=produce_type)
        produce_dict[produce_type] = produces

    context = {"produce_dict": produce_dict, "business": business, "username": username}
    return render(req, "order/order_list.html", context)
 

@login_required
@user_passes_test(isDesk)
@log_performance('Order_Add_To_Cart')
def add_to_cart(request):
    if request.method == "POST":
        # İsteğin AJAX olup olmadığını kontrol edin
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Sepete eklenecek ürün ve miktarını al
            product_id = request.POST.get("produce_id")
            quantity = request.POST.get("quantity")

            # Sepeti al
            cart = Cart.objects.get(desk__slug=request.user.username, isActive=True)

            # Sepette aynı ürün var mı kontrol et
            cart_item = CartItem.objects.filter(cart=cart, produce_id=product_id,isConfirm=False).first()

            if cart_item:
                # Sepette aynı ürün varsa, miktarı güncelle
                cart_item.quantity += int(quantity)
                cart_item.is_service=False
                cart_item.unit_price=cart_item.produce.price
                cart_item.save()
            else:
                # Sepette aynı ürün yoksa, yeni bir öğe ekle
                cart_item = CartItem(cart=cart, produce_id=product_id, quantity=quantity)
                cart_item.unit_price=cart_item.produce.price
                cart_item.save()

            return JsonResponse({'success': True})  # AJAX isteğine başarılı bir yanıt gönder
        else:
            # AJAX isteği değilse hata döndür
            return JsonResponse({'error': 'Bu görünüm yalnızca AJAX isteklerini destekler.'}, status=400)
    else:
        return HttpResponseNotAllowed(["POST"])  # Sadece POST isteklerine izin ver
@log_performance('Create_Cart')
def create_cart(req):
    try:
        # Masayı kullanıcının ismine göre alıyoruz
        desk = Desk.objects.get(slug=req.user.username)
        
        # Masa rezerve ediliyor ve status_code güncelleniyor
        desk.isReserve = True
        desk_status_code = 2  # Örneğin, 2 status_code rezerve edilmiş durumu gösteriyor
        cart_data = Cart(desk=desk)
        # Masa kaydediliyor
        desk.save(update_fields=['isReserve',])  # isReserve alanları güncelleniyor
        cart_data.save()
        
        # WebSocket aracılığıyla masa bilgisi gönderiliyor
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'business_{desk.business.id}',  # İşletmeye özel WebSocket grubu
            {
                'type': 'send_desk_update',
                'desk_data': {
                    'desk_id': desk.id,
                    'desk_name': desk.name,
                    'status_code': desk_status_code,  # Masanın yeni durumu
                    'is_reserve': desk.isReserve,
                }
            }
        )
        
        # Eğer her şey başarılıysa "success" döndürülüyor
        return "success"
    except Exception as e:
        print(e.args)
        return "error"

    
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def desk_is_logout(req):
    try:
        # Veritabanı işlemlerini bir atomic blok içinde yapıyoruz
        with transaction.atomic():
            desk = Desk.objects.get(slug=req.user.username)
            desk.isReserve = False
            
            # Sepeti kontrol et
            cart = Cart.objects.filter(desk=desk, isActive=True).first()  
            if cart:
                cart.isActive = False  # Sepeti pasif hale getir
            
            # Siparişi kontrol et
            order = Order.objects.filter(desk=desk, isActive=True).first()  
            if order:
                order.status = 'completed'  # Sipariş tamamlandı
                order.isActive = False
                order.calculate_total_price()  # Toplam fiyatı hesapla
            
            # Tüm değişiklikleri kaydet
            desk.save(update_fields=['isReserve'])  # Sadece 'isReserve' alanını güncelle
            if cart:
                cart.save()  # Sepeti kaydet
            if order:
                order.save()  # Siparişi kaydet

            # WebSocket ile masa durumunu gönderiyoruz
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'business_{desk.business.id}',  # İşletmeye ait WebSocket kanalı
                {
                    'type': 'send_desk_update',
                    'desk_data': {
                        'desk_id': desk.id,
                        'desk_name': desk.name,
                        'order_item_count': 0,  # Masa boşaldığı için sipariş yok
                        'status': 'Müsait',  # Masa durumu tekrar kullanılabilir
                        'status_code': 0,  # Durum kodu normale döndü
                        'is_reserve': False  # Masa rezervasyonu kaldırıldı
                    }
                }
            )
        
        return "success"
    
    except Desk.DoesNotExist:
        return "error: desk not found"  # Masa bulunamadı hatası
    
    except Exception as e:
        print(f"An error occurred: {e}")  # Hataları logla
        return "error"


    
@login_required
@user_passes_test(isDesk)
def cart(req):
    cart_items = []
    cart = Cart.objects.get(desk__slug=req.user.username, isActive=True)
    cart_items_queryset = CartItem.objects.filter(cart=cart, isConfirm=False)
    cart_sum_price = 0
    sum_quantity=0

    for item in cart_items_queryset:
        # Her bir sepet öğesi için ayrı bir DTO (Data Transfer Object) oluştur
        item_sum_price = item.quantity * item.produce.price  # Öğenin toplam fiyatını hesapla
        cart_sum_price += item_sum_price  # Sepetin toplam fiyatını güncelle
        sum_quantity += item.quantity

        cart_dto = {
            'name': item.produce.name,
            'type': item.produce.produceType.name,
            'quantity': item.quantity,
            'image':item.produce.image,
            'price': item.produce.price,
            'sum_quantity':sum_quantity,
            'sum_price': item_sum_price  # Toplam fiyatı hesapla
        }
        cart_items.append(cart_dto)  # Oluşturulan DTO'yu listeye ekle
    context = {"cart_items": cart_items, "sum_price": cart_sum_price,"cart_id":cart.id}
    return render(req, "order/cart.html", context)


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
@user_passes_test(isDesk)
@log_performance('Order_Cart_to_Order')
def cart_to_order(req, cart_id):
    # Sepeti al
    cart = get_object_or_404(Cart, id=cart_id)
    is_not_confirm = CartItem.objects.filter(cart=cart, isConfirm=False)

    # Eğer sepette zaten bir sipariş varsa, yeni bir sipariş oluşturmaya gerek yok
    existing_order = Order.objects.filter(desk=cart.desk, isActive=True).first()
    
    if not existing_order:
        # Yeni bir sipariş oluştur
        order = Order.objects.create(desk=cart.desk, total_price=cart.calculate_total_price())
    else:
        order = existing_order  # Mevcut siparişe devam et
    
    # Onaylanmamış öğeleri siparişe ekleyen fonksiyon
    add_items_to_order(is_not_confirm, order)
    
    # Sipariş güncellemesini WebSocket aracılığıyla gönder
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'business_{cart.desk.business.id}',  # WebSocket grup adı
        {
            'type': 'send_order_update',
            'order_data': {
            'order_id': order.id,
            'status': order.status,  # Siparişin durumu
            'total_price': str(order.total_price),  # Decimal veriyi string olarak göndermek gerekebilir
            'items': list(order.orderitem_set.values('id', 'produce__name', 'quantity', 'unit_price','produce__image')),  # Sipariş öğeleri
            'desk_name': cart.desk.name,  # Masa ismi
            'desk_id':cart.desk.id,
        
        }
        }
    )
    
    return redirect("order_index")  # Siparişin gösterildiği sayfaya yönlendir

@log_performance('Order_add_items_order')
def add_items_to_order(cart_items, order):
    """
    Sepetteki onaylanmamış öğeleri siparişe ekler.
    """
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            produce=cart_item.produce,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price
        )
        cart_item.isConfirm = True
        cart_item.save()



        

        
        
