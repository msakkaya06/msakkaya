# order/views/api_views.py
from rest_framework import status
import uuid, base64
import qrcode
from io import BytesIO
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from easymanagement.models import Order, OrderItem, Produce, Desk, Cart,ProduceType,CartItem
from order.serializers import ProduceSerializer, CartSerializer, CartItemSerializer
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction

class ProduceListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        produces = Produce.objects.all()
        serializer = ProduceSerializer(produces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProduceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ürünleri çek
        produce_types = ProduceType.objects.filter(business=request.user.business)
        produce_dict = {}
        
        for produce_type in produce_types:
            produces = Produce.objects.filter(produceType=produce_type)
            produce_dict[produce_type.name] = ProduceSerializer(produces, many=True).data

        return Response({'produce_dict': produce_dict}, status=status.HTTP_200_OK)


class CreateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with transaction.atomic():  # Tüm işlem tek bir DB transaction içinde yapılır
                desk = Desk.objects.select_for_update().get(slug=request.user.username)
                print("TOKEN KULLANICI:", request.user.username," İşlem: CreateCartView")
                         # Masa rezerve ediliyor
                desk.isReserve = True
                desk.save(update_fields=['isReserve'])



                if Cart.objects.filter(desk=desk, isActive=True).exists():
                    return Response({'success': False, 'message': 'Cart already exists'}, status=status.HTTP_200_OK)

       
                # Sepet oluşturuluyor
                cart = Cart.objects.create(desk=desk)

                # WebSocket mesajı gönderiliyor
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'business_{desk.business.id}',
                    {
                        'type': 'send_desk_update',
                        'desk_data': {
                            'desk_id': desk.id,
                            'desk_name': desk.name,
                            'status_code': 2,
                            'is_reserve': desk.isReserve,
                        }
                    }
                )

                return Response({'success': True, 'message': 'Cart created and desk reserved.'}, status=status.HTTP_201_CREATED)

        except Desk.DoesNotExist:
            return Response({'success': False, 'message': 'Desk not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(desk__slug=request.user.username, isActive=True)
        product_id = request.data.get('produce_id')
        quantity = int(request.data.get('quantity'))
        print("TOKEN KULLANICI:", request.user.username," İşlem: AddToCartView")

        produce = Produce.objects.get(id=product_id)

        cart_item = CartItem.objects.filter(cart=cart, produce_id=product_id, isConfirm=False).first()

        if cart_item:
            # Eğer ürün varsa miktarı artır ve fiyatı güncelle
            cart_item.quantity += quantity
            cart_item.unit_price = produce.price
            cart_item.save()
        else:
            # Yeni ürün için hem fiyat hem miktar set edilmeli
            cart_item = CartItem.objects.create(
                cart=cart,
                produce=produce,
                quantity=quantity,
                unit_price=produce.price
            )

        # 🔥 Ürün eklendikten SONRA sepetin toplam fiyatını güncelleyelim
        cart.calculate_total_price()

        return Response({'success': True,'total_price': cart.total_price}, status=status.HTTP_200_OK)


class DecreaseCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get('cart_item_id')
        if not cart_item_id:
            return Response({"error": "cart_item_id gerekli."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__desk__slug=request.user.username, cart__isActive=True)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        # Sepetin toplam fiyatını yeniden hesapla
        cart_item.cart.calculate_total_price()

        return Response({'success': True,'total_price': cart_item.total_price}, status=status.HTTP_200_OK)


class CartToOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        desk = cart.desk
        print("TOKEN KULLANICI:", request.user.username," İşlem: CartToOrder")


        # Mevcut sipariş var mı kontrol et
        order = Order.objects.filter(desk=desk, isActive=True).first()
        if not order:
            order = Order.objects.create(desk=desk)

        # Sepetteki onaylanmamış ürünleri siparişe ekle
        for cart_item in CartItem.objects.filter(cart=cart, isConfirm=False):
            OrderItem.objects.create(
                order=order,
                produce=cart_item.produce,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price
            )
            cart_item.isConfirm = True
            cart_item.save()

        # Fiyat hesapla ve kaydet
        order.calculate_total_price()

        # WebSocket yayını yap
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'business_{desk.business.id}',
            {
                'type': 'send_order_update',
                'order_data': {
                    'order_id': order.id,
                    'status': order.status,
                    'total_price': str(order.total_price),
                    'items': list(order.orderitem_set.values('id', 'produce__name', 'quantity', 'unit_price', 'produce__image')),
                    'desk_name': desk.name,
                    'desk_id': desk.id,
                }
            }
        )

        return Response({'success': True, 'order_id': order.id}, status=status.HTTP_200_OK)

class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("TOKEN KULLANICI:", request.user.username," İşlem: CartDetailView")

        desk_slug = request.user.username
        try:
            cart = Cart.objects.get(desk__slug=desk_slug, isActive=True)

            # Onaylanmamış ve onaylanmış ürünleri ayır
            pending_items = CartItem.objects.filter(cart=cart, isConfirm=False)
            confirmed_items = CartItem.objects.filter(cart=cart, isConfirm=True)

            pending_data = CartItemSerializer(pending_items, many=True).data
            confirmed_data = CartItemSerializer(confirmed_items, many=True).data

            return Response({
                'cart_id': cart.id,
                'pending_items': pending_data,
                'confirmed_items': confirmed_data,
                'total_price': str(cart.total_price or 0)
            })
        except Cart.DoesNotExist:
            return Response({'error': 'Aktif sepet bulunamadı.'}, status=404)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from easymanagement.models import Desk, EEUser


class DeskReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("TOKEN KULLANICI:", request.user.username," İşlem: DeskReleaseView")

        try:
            
            desk = Desk.objects.get(slug=request.user.username)
            user = request.user

            desk.isReserve = False
            desk.save(update_fields=['isReserve'])

            # Yeni token üret
            while True:
                raw_token = f"{user.username}:{uuid.uuid4()}"
                encoded_token = base64.urlsafe_b64encode(raw_token.encode()).decode()
                if not EEUser.objects.filter(token=encoded_token).exists():
                    break

            user.token = encoded_token

            # QR kod yeniden oluştur
            login_url = f"http://192.168.137.1:3000/login-redirect?username={user.username}&token={user.token}"
            qr_image = qrcode.make(login_url)
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")

            qr_dir = os.path.join(settings.MEDIA_ROOT, "qr_codes")
            os.makedirs(qr_dir, exist_ok=True)
            file_path = os.path.join(qr_dir, f"{user.username}_qr.png")
            with open(file_path, "wb") as f:
                f.write(buffer.getvalue())

            user.save()

            return Response({"message": "Masa boşa çekildi ve yeni token oluşturuldu."}, status=200)

        except Desk.DoesNotExist:
            return Response({"error": "Masa bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=500)



class DeskInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            desk = Desk.objects.get(slug=request.user.username)
            return Response({
                "desk_name": desk.name,
                "business_name": desk.business.name,
                "desk_id": desk.id
            })
        except Desk.DoesNotExist:
            return Response({"error": "Masa bulunamadı"}, status=404)
