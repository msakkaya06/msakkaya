from easymanagement.models import Order, OrderItem
from django.db.models import Prefetch

def get_sales_for_business(business_id):
    orders = Order.objects.filter(desk__business_id=business_id).prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('produce'))
    ).order_by('-created_at')

    sales_data = []

    for order in orders:
        order_items = [
            {
                'product_name': item.produce.name,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.quantity * item.unit_price
            }
            for item in order.orderitem_set.all()
        ]
        
        sales_data.append({
            'order_id': order.id,
            'desk': order.desk.name,
            'created_at': order.created_at.strftime("%d-%m-%Y %H:%M"),
            'status': order.get_status_display(),
            'total_price': order.total_price,
            'items': order_items
        })
    
    return orders
