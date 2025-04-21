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


@login_required
@user_passes_test(isDesk)
@log_performance('Order_Index')
def index(req):
    try:
        business = req.user.business
        username = Desk.objects.get(slug=req.user.username)
        produce_types = ProduceType.objects.filter(business=business)
        
        cart_exist = Cart.objects.filter(desk__slug=req.user.username, isActive=True).exists()
        if not cart_exist:  # Eğer mevcut bir sepet yoksa
            cart_result = create_cart(req)  # Sepeti oluştur
            if cart_result != "success":  # Sepet oluşturma başarısız olduysa
                return JsonResponse({'success': False, 'message': 'Sepet oluşturma işleminde hata oluştu. Restoran yetkilisi ile görüşün'})

        produce_dict = {}
        for produce_type in produce_types:
            produces = Produce.objects.filter(produceType=produce_type)
            produce_dict[produce_type.id] = list(produces.values('id', 'name', 'price', 'image'))

        return JsonResponse({
            'success': True,
            'produce_dict': produce_dict,
            'business': {
                'id': business.id,
                'name': business.name
            },
            'username': username.username
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@log_performance('Create_Cart')
def create_cart(req):
    try:
        desk = Desk.objects.get(slug=req.user.username)
        
        desk.isReserve = True
        cart_data = Cart(desk=desk)
        
        desk.save(update_fields=['isReserve'])
        cart_data.save()
        
        # WebSocket aracılığıyla masa güncellemesi gönder
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'business_{desk.business.id}', {
            'type': 'send_desk_update',
            'desk_data': {
                'desk_id': desk.id,
                'desk_name': desk.name,
                'status_code': 2,  # Masa rezerve edildi
                'is_reserve': desk.isReserve
            }
        })
        
        return JsonResponse({'success': True, 'message': 'Sepet başarıyla oluşturuldu.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {str(e)}'})



@login_required
@user_passes_test(isDesk)
@log_performance('Order_Add_To_Cart')
def add_to_cart(request):
    if request.method == "POST":
        try:
            # İsteğin AJAX olup olmadığını kontrol edin
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Sepete eklenecek ürün ve miktarını al
                product_id = request.POST.get("produce_id")
                quantity = request.POST.get("quantity")
                
                # Sepeti al
                cart = Cart.objects.get(desk__slug=request.user.username, isActive=True)
                
                # Sepette aynı ürün var mı kontrol et
                cart_item = CartItem.objects.filter(cart=cart, produce_id=product_id, isConfirm=False).first()
                
                if cart_item:
                    # Sepette aynı ürün varsa, miktarı güncelle
                    cart_item.quantity += int(quantity)
                    cart_item.unit_price = cart_item.produce.price
                    cart_item.save()
                else:
                    # Sepette aynı ürün yoksa, yeni bir öğe ekle
                    cart_item = CartItem(cart=cart, produce_id=product_id, quantity=quantity, unit_price=cart_item.produce.price)
                    cart_item.save()

                return JsonResponse({'success': True, 'message': 'Ürün sepete eklendi.'})

            else:
                return JsonResponse({'error': 'Bu görünüm yalnızca AJAX isteklerini destekler.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': 'Bir hata oluştu.', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Sadece POST istekleri kabul edilir.'}, status=405)


@login_required
@user_passes_test(isDesk)
def cart(req):
    try:
        cart = Cart.objects.get(desk__slug=req.user.username, isActive=True)
        cart_items_queryset = CartItem.objects.filter(cart=cart, isConfirm=False)
        
        cart_items = []
        cart_sum_price = 0
        sum_quantity = 0

        for item in cart_items_queryset:
            item_sum_price = item.quantity * item.produce.price
            cart_sum_price += item_sum_price
            sum_quantity += item.quantity
            
            cart_dto = {
                'name': item.produce.name,
                'type': item.produce.produceType.name,
                'quantity': item.quantity,
                'image': item.produce.image.url,
                'price': str(item.produce.price),
                'sum_quantity': sum_quantity,
                'sum_price': str(item_sum_price)
            }
            cart_items.append(cart_dto)
        
        return JsonResponse({
            'success': True,
            'cart_items': cart_items,
            'cart_sum_price': str(cart_sum_price),
            'cart_id': cart.id
        })

    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Sepet bulunamadı.'})


@login_required
@user_passes_test(isDesk)
@log_performance('Order_Cart_to_Order')
def cart_to_order(req, cart_id):
    try:
        cart = get_object_or_404(Cart, id=cart_id)
        is_not_confirm = CartItem.objects.filter(cart=cart, isConfirm=False)

        # Eğer sepette zaten bir sipariş varsa, yeni bir sipariş oluşturmaya gerek yok
        existing_order = Order.objects.filter(desk=cart.desk, isActive=True).first()

        if not existing_order:
            # Yeni bir sipariş oluştur
            order = Order.objects.create(desk=cart.desk, total_price=cart.calculate_total_price())
        else:
            order = existing_order  # Mevcut siparişe devam et

        add_items_to_order(is_not_confirm, order)
        
        # Siparişin toplam fiyatını güncelle
        order.calculate_total_price()

        # WebSocket güncellemesi gönder
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'business_{cart.desk.business.id}', {
            'type': 'send_order_update',
            'order_data': {
                'order_id': order.id,
                'status': order.status,
                'total_price': str(order.total_price),
                'items': list(order.orderitem_set.values('id', 'produce__name', 'quantity', 'unit_price', 'produce__image')),
                'desk_name': cart.desk.name,
                'desk_id': cart.desk.id
            }
        })

        return JsonResponse({'success': True, 'message': 'Sipariş başarıyla oluşturuldu.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {str(e)}'})


@log_performance('Order_add_items_order')
def add_items_to_order(cart_items, order):
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            produce=cart_item.produce,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price
        )
        cart_item.isConfirm = True
        cart_item.save()
