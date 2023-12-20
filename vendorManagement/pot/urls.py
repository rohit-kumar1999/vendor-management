from django.urls import path

from . import views

urlpatterns = [
    path('', views.PurchaseOrderView.as_view(), name="purchase_orders"),
    path('<slug:order_id>', views.PurchaseOrderById.as_view(), name='purchase_order_by_id')
]
