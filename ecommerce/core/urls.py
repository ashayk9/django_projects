from django.urls import path
from . import views

urlpatterns = [
    #path('',views.item_list,name='item_list'),
    path('',views.ItemListView.as_view(), name='item_list'),
    #path('detail/<slug>/',views.DetailView.as_view(), name='detail'),
    path('detail/<slug>/',views.detail_view, name='detail'),
    path('add-to-cart/<slug>/',views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-summary', views.OrderSummaryView.as_view(), name='order_summary'),
    path('add-to-order-cart/<slug>/',views.add_to_order_cart, name='add_to_order_cart'),
    path('remove-from-order-cart/<slug>/', views.remove_from_order_cart, name='remove_from_order_cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment',views.Payment.as_view(), name='payment'),

]