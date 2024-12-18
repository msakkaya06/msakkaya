from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib import messages
from easymanagement.models import Order,Payment




def isManager(user):
    return user.is_manager
# Create your views here.

def index(request):
    pass


def payment(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payment/payment.html", {"context":order})



@login_required
@user_passes_test(isManager)
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Ödeme işlemini burada gerçekleştir
        amount = sum(item.produce.price * item.quantity for item in order.orderitem_set.all())
        Payment.objects.create(order=order, amount=amount, is_successful=True)
        
        # Siparişin durumunu güncelle
        order.status = 'completed'
        order.save()
        
        # Masayı serbest bırak
        order.desk.isReserve = False
        order.desk.save()

        messages.success(request, 'Ödeme başarıyla tamamlandı ve masa serbest bırakıldı.')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'order': order,
    }
    return render(request, 'checkout.html', context)