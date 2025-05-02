from django.urls import path
from order.views.api_views import CartDetailView, DecreaseCartItemView, DeskInfoView, DeskReleaseView, ProduceListView, CreateCartView, AddToCartView, CartToOrderView

urlpatterns = [
    path('produces/', ProduceListView.as_view(), name='produce-list'),
    path('create-cart/', CreateCartView.as_view(), name='create-cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/<int:cart_id>/to-order/', CartToOrderView.as_view(), name='cart-to-order'),
    path('release-desk/', DeskReleaseView.as_view(), name='desk-release'),
    path("desk-info/", DeskInfoView.as_view(), name="desk-info"),
    path('api/decrease-cart-item/', DecreaseCartItemView.as_view(), name='decrease-cart-item'),
]
