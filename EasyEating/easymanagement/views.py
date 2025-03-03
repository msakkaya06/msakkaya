from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.http import require_POST

from logging_helper.performance_logger import log_performance
from .forms import CreateProductForm, DeskCreateForm
from .models import Business, Cart,Desk, Order, OrderItem,Produce,EEUser, ProduceType, Payment
from django.contrib import messages
from django.core.paginator import Paginator

from easymanagement.services.sales_services import get_sales_for_business
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta



def isManager(user):
    return user.is_manager

# Create your views here.
def get_user_business(req):
    user_business=req.user.business
    return user_business

@login_required
@user_passes_test(isManager)
@log_performance('Kitchen_Management')
def index(req):
    user_business = req.user.business
    desk_list_queryset = Desk.objects.filter(business=user_business).order_by('-isReserve')  # isReserve alanına göre azalan sıralama
    desk_list = []
    for desk in desk_list_queryset:
        all_items_served = True 
        order_items = []
        order=None
        sum_order_count=0
        sum_price=0
        cart_exists = Cart.objects.filter(desk=desk, isActive=True).exists()
        order_exists = Order.objects.filter(desk=desk, isActive=True).exists()
        if desk.isReserve:
            if cart_exists:
                status=1
                status_text = "Sipariş Bekleniyor"
                if order_exists:
                    status=2
                    status_text = "Hazırlanıyor"
                    # Sipariş ID'sini ve siparişteki ürün sayısını al
                    order = Order.objects.get(desk=desk, isActive=True)
                    order_id = order.id
                    order_item_count = order.orderitem_set.count()
                    order_items_queryset = order.orderitem_set.all()
                    # Order varsa orderItem nesnelerini listelemek
                    for item in order_items_queryset:
                        existing_item = next((x for x in order_items if x['product_name'] == item.produce.name), None)
                        if existing_item:
                        # Eğer ürün listede zaten varsa, miktarı artır
                            existing_item['quantity'] += item.quantity
                        else:
                        # Eğer ürün listede yoksa, yeni bir kopya oluştur ve listeye ekle
                            order_item = {
                                'product_name': item.produce.name,
                                'quantity': item.quantity,
                                'price': item.produce.price,
                                'image':item.produce.image,
                                'is_service':item.is_service
                                             }
                            sum_order_count +=order_item["quantity"]
                            sum_price += order_item["price"]*order_item["quantity"]
                            order_items.append(order_item)
                            if not order_item['is_service']:
                                all_items_served = False  # Eğer bir öğe bile servis edilmemişse, global değişkeni False yap
# Bu noktada all_items_served değişkeni tüm öğelerin servis edilip edilmediğini belirler                            
        else:
            status_text = "Müsait"
            status=3
            order_id = None
            order_item_count = None

        desk_dto = {
            'id': desk.id,
            'name': desk.name,
            'isReserve': desk.isReserve,
            'status_code':status,
            'isActive': desk.isActive,
            'status': status_text,
            'order_id': order_id if order_exists else None,  # Siparişin varsa order_id, yoksa None
            'order_item_count': sum_order_count if order_exists else None,  # Siparişin varsa ürün sayısı, yoksa None
            'order_items': order_items if order_exists else None,  # Sipariş varsa ürünler, yoksa None
            'order': order if order_exists else None,  # Sipariş varsa ürünler, yoksa None
            'sum_price':sum_price * sum_order_count,
            'all_items_served':all_items_served
     
             }
        desk_list.append(desk_dto)
    return render(req, "easymanagement/desk_list.html", {"desk_list": desk_list, "business": user_business})



@login_required
@require_POST
def mark_item_as_served(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.is_service = True
    order_item.save()
    return JsonResponse({'success': True})

@login_required
@require_POST
def mark_all_items_as_served(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.orderitem_set.update(is_service=True)
    return JsonResponse({'success': True})

   
def orderList(req):
    pass


from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from collections import defaultdict

@login_required
@user_passes_test(isManager)
@log_performance('Dashboard_Load')
def management(req):
    # İlgili işletmeye ait tüm siparişleri al
    orders = Order.objects.filter(desk__business=req.user.business, isActive=True)
    desks_all = Desk.objects.filter(business=req.user.business, isActive=True)
    desk_reserve = desks_all.filter(isReserve=True)
    desk_availible = desks_all.count() - desk_reserve.count()
    total_desks_count = desks_all.count()
    reserved_desks_count = desk_reserve.count()

    # Doluluk yüzdesini hesapla
    occupancy_percentage = (reserved_desks_count / total_desks_count) * 100 if total_desks_count > 0 else 0
    occupancy_percentage = round(occupancy_percentage, 0)

    # Bu siparişlerin id'lerini bir liste olarak al
    order_ids = orders.values_list('id', flat=True)

    # Bu siparişlere ait tüm sipariş kalemlerini al
    order_items = OrderItem.objects.filter(order__id__in=order_ids)
    total_quantity = sum([item.quantity for item in order_items])
    sum_order_count = Order.objects.filter(desk__business=req.user.business).count()

    # Tüm siparişlere ait ürünlerin sayısını al
    sum_order_item_count = OrderItem.objects.filter(order__desk__business=req.user.business).count()


    # Aylara göre sipariş miktarı ve toplam ücreti hesapla
    one_year_ago = timezone.now() - timedelta(days=365)
    monthly_data = (
    Order.objects.filter(desk__business=req.user.business, created_at__gte=one_year_ago)
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(order_count=Count('id'), total_price=Sum('total_price'))
    .order_by('month')
)
    # Grafikte kullanılacak veri formatı
    order_counts = []
    total_prices = []
    labels = []
    for entry in monthly_data:
        labels.append(entry['month'].strftime('%Y-%m'))  # Yıl-Ay formatı
        order_counts.append(entry['order_count'])
        total_prices.append(float(entry['total_price']) if entry['total_price'] else 0)
        # En popüler ürünleri bul
    exclude_drink_types = ProduceType.objects.filter(name__icontains="içecek")
    popular_items = (
        OrderItem.objects.filter(order__desk__business=req.user.business)
        .exclude(produce__produceType__in=exclude_drink_types)
        .values('produce__name', 'produce__image')  # Ürün adı ve resmi
        .annotate(item_count=Sum('quantity'))  # Toplam miktar
        .order_by('-item_count')[:5]  # En çok satılan 5 ürünü al
    )

    # Toplam satılan ürün miktarını bul
    total_items_sold = OrderItem.objects.filter(order__desk__business=req.user.business).exclude(produce__produceType__in=exclude_drink_types).aggregate(total=Sum('quantity'))['total']
    
   
# Varsayılan değerler
    popular_items_data = []
    popular_item_names = []
    popular_item_percentages = []
    popular_item_count = []

    if total_items_sold:  # Eğer toplam satılan ürün varsa hesapla
        for item in popular_items:
            item_percentage = (item['item_count'] / total_items_sold) * 100 if total_items_sold > 0 else 0
            popular_items_data.append({
            'name': item['produce__name'],
            'image': item['produce__image'],
            'count': item['item_count'],
            'percentage': round(item_percentage, 2)
        })
        # Popüler ürünlerin isim ve yüzdelerini ayrı listeler olarak hazırlayalım
        popular_item_names = [item['name'] for item in popular_items_data]
        popular_item_percentages = [item['percentage'] for item in popular_items_data]
        popular_item_count = [item['count'] for item in popular_items_data]



    dashboard_dto = {
        'orders': orders,
        'order_count': orders.count(),
        'total_quantity': total_quantity,
        'desk_availible': desk_availible,
        'total_desks_count': total_desks_count,
        'reserved_desks_count': reserved_desks_count,
        'occupancy_percentage': occupancy_percentage,
        'sum_order_count': sum_order_count,
        'sum_order_item_count': sum_order_item_count,
        'monthly_labels': labels,  # Grafik için aylar
        'monthly_order_counts': order_counts,  # Grafik için sipariş 
        'monthly_total_prices': total_prices,  # Grafik için toplam fiyatlar
        'popular_item_names':popular_item_names,
        'popular_item_percentages':popular_item_percentages,
        'popular_item_count':popular_item_count,

    }

    context = {
        "data": dashboard_dto
    }
    return render(req, "easymanagement/dashboard.html", context)


@login_required
@user_passes_test(isManager)
@log_performance('Desk_Management')
def desk(req):
    if req.method == 'POST':
        form = DeskCreateForm(req.POST, user=req.user)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                 messages.add_message(req,messages.ERROR,"Eklemek istediğiniz masa sistemde mevcut")
            return redirect('management_desk')
    else:
        desks = Desk.objects.filter(business=get_user_business(req))
        chart_data=[]
        reserve_desks=desks.filter(isReserve=True)
        available_desks=desks.filter(isReserve=False)
        for desk in desks:
            desk.last_login = EEUser.objects.get(username=desk.slug).last_login
        
        chart_data={
            "reserve_count":reserve_desks.count(),
            "available_count":available_desks.count(),
            "reserved_desks":reserve_desks,
            "available_desks":available_desks
        }
        paginator=Paginator(desks,10)
        page=req.GET.get('page',1)
        page_obj=paginator.get_page(page)
        form = DeskCreateForm(user=req.user)
        context = {
        "desks": desks,
        "form": form,
        "page_obj":page_obj,
        "chart_data":chart_data
        }
        return render(req, "easymanagement/desk_management.html", context)


@login_required
@user_passes_test(isManager)
def produce(req):
    business=req.user.business
    produce_types=ProduceType.objects.filter(business=business)
    produce_dict = {}
    for produce_type in produce_types:
        produces = Produce.objects.filter(produceType=produce_type)
        produce_dict[produce_type] = produces
    
    context = {"produce_dict": produce_dict,"business":business}
    return render(req, "easymanagement/produce_management.html",context)


@login_required
@user_passes_test(isManager)
def produce_post_form(req):
    name = req.POST.get("name")
    description = req.POST.get("description")
    price_str = req.POST.get("price")
    if not name or not description or not price_str:
        return JsonResponse({'success': False, 'error_msg': 'Tüm alanları doldurmalısınız.'})
    if len(name) > 100 or len(description) > 100:
        return JsonResponse({'success': False, 'error_msg': 'Ad ve açıklama alanları en fazla 100 karakter olmalıdır.'})
    try:
        price = float(price_str.replace(",", "."))
    except ValueError:
        return JsonResponse({'success': False, 'error_msg': 'Fiyat alanı geçersiz bir değer içeriyor.'})
    
    if "image" in req.FILES:
            image = req.FILES["image"]

    return JsonResponse({'success': True, 'name': name, 'description': description, 'price': price, 'image': image})

@login_required
@user_passes_test(isManager)        
def produce_update(req, id):
    produce = get_object_or_404(Produce, pk=id)
    if req.method == "POST":
        name = req.POST.get("name")
        description = req.POST.get("description")
        price_str = req.POST.get("price")
        if not name or not description or not price_str:
            return JsonResponse({'success': False, 'error_msg': 'Tüm alanları doldurmalısınız.'})
        try:
            price = float(price_str.replace(",", "."))
        except ValueError:
            return JsonResponse({'success': False, 'error_msg': 'Fiyat alanı geçersiz bir değer içeriyor.'})
        produce.name = name
        produce.description = description
        produce.price = price
     
        if "image" in req.FILES:
            image = req.FILES["image"]
            produce.image = image
        produce.save()
        return JsonResponse({'success': True,'message':"Ürün Başarıyla Güncellendi"})
    else:
        form = CreateProductForm(instance=produce)
        return render(req, "easymanagement/produce_management.html", {"form": form, "id": id})



@login_required
@user_passes_test(isManager)
def create_produce(req,produce_type):
    produceType=ProduceType.objects.get(pk=produce_type)
    if req.method == "POST":
        if req.method == "POST":
            name = req.POST.get("name")
            description = req.POST.get("description")
            price_str = req.POST.get("price")
            if "image" in req.FILES:
                image = req.FILES["image"]
            
            if not name or not description or not price_str:
                return JsonResponse({'success': False, 'error_msg': 'Tüm alanları doldurmalısınız.'})

            try:
                price = float(price_str.replace(",", "."))
            except ValueError:
                return JsonResponse({'success': False, 'error_msg': 'Fiyat alanı geçersiz bir değer içeriyor.'})
            data=Produce(name=name,description=description,price=price,image=image,produceType=produceType)
            try:
                data.save()
                return render(req, "easymanagement/produce_management.html")
            except:
                print("hata oluştu")
    else:
        pass


def sales_management(request):
    # En çok satılan ürünler
    business = request.user.business  # Kullanıcının bağlı olduğu işletme modeli (örneğin: business modeli)

    # 1. Popüler ürünleri almak için sorgu
    popular_items = OrderItem.objects.filter(order__desk__business=business) \
        .values('produce__name', 'produce__price', 'produce__image') \
        .annotate(total_quantity=Sum('quantity')) \
        .order_by('-total_quantity')[:10]

    # 2. Toplam ciroyu almak için sorgu
    total_revenue = Order.objects.filter(desk__business=business) \
        .aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0

    # 3. Toplam sipariş sayısını almak için sorgu
    total_orders = Order.objects.filter(desk__business=business).count()

    #Toplam sipariş edilen ürün adedi için sorgu
    total_product_count = OrderItem.objects.filter(order__desk__business=business) \
        .aggregate(total_products=Sum('quantity'))['total_products'] or 0

    # En çok satan ürünü getir
    most_sold_item = popular_items[0] if popular_items else None
    today = timezone.now()
    first_day_of_month = today.replace(day=1)
    #Sorgulanan Dataları Template'ye gönderiyoruz
    context = {
        'popular_items': popular_items,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'most_sold_item': most_sold_item,
        'total_product_count':total_product_count
    }

    return render(request, 'easymanagement/sales_management.html', context)

def create_desk(req):
    pass


def desk_details(req,id):
    pass

def order_details(req,desk_id):
    pass

def checkout(req,order_id):
    pass



@login_required
@user_passes_test(isManager)
@log_performance('Sales_List')
def sales_view(request):
    orders = get_sales_for_business(request.user.business.id) # Siparişleri al ve tarih sırasına göre sırala
    paginator = Paginator(orders, 10)  # Her sayfada 10 sipariş gösterilecek
    page_number = request.GET.get('page')  # Sayfa numarasını al
    page_obj = paginator.get_page(page_number)  # Sayfa objesini oluştur
    return render(request, 'easymanagement/sales_list.html', {'orders': page_obj})


@login_required
@user_passes_test(isManager)
@log_performance('Finance_Dashboard')
def finance_dashboard(request):
    business=request.user.business
    today = now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    daily_revenue = Order.objects.filter(created_at__date=today,desk__business=business,payment_status=True).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_revenue = Order.objects.filter(created_at__date__gte=start_of_month,desk__business=business,payment_status=True).aggregate(total=Sum('total_price'))['total'] or 0
    yearly_revenue = Order.objects.filter(created_at__date__gte=start_of_year,desk__business=business,payment_status=True).aggregate(total=Sum('total_price'))['total'] or 0

    context = {
        'daily_revenue': daily_revenue,
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
    }
    return render(request, 'easymanagement/finance_dashboard.html',context)




def payment_screen(request):
    """Boş ve rezerve edilmiş masaları listeleyen view."""
    reserved_desks = Desk.objects.filter(isReserve=True, business=request.user.business)  # Rezerve masalar
    empty_desks = Desk.objects.filter(isReserve=False, business=request.user.business)  # Boş masalar
    
    # Sipariş bilgilerini içeren bir sözlük oluştur
    reserved_desk_data = []
    for desk in reserved_desks:
        order = Order.objects.filter(isActive=True, desk=desk).first()  # Sipariş olup olmadığını kontrol et
        if order:
            order_items = order.orderitem_set.all()  # Siparişe bağlı ürünleri al
            reserved_desk_data.append({
                'desk': desk,
                'order': order,
                'order_items': order_items,
                'total_price': order.total_price
            })

    context = {
        'reserved_desk_data': reserved_desk_data,
        'empty_desks': empty_desks,
    }
    return render(request, 'easymanagement/payment_view.html', context)



def payment_view(request, order_id):
    """Ödeme ekranını gösteren view."""
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
        'total_price': order.total_price,
    }
    return render(request, 'easymanagement/payment.html', context)

def process_payment(request, order_id):
    """Ödeme işlemini gerçekleştiren view."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id', None)  # Sadece kart ödemelerinde dolacak
        
        # Ödeme kaydı oluştur
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            method=payment_method,
            transaction_id=transaction_id,
            is_successful=True
        )
        order.isActive=False
        order.payment_status = True  # Siparişin ödeme durumunu güncelle
        order.status = 'completed'  # Sipariş tamamlandı
        order.save()
        
        return redirect('payment_screen')  # Ödeme tamamlandıktan sonra geri yönlendirme
    
    return redirect('payment_view', order_id=order.id)
