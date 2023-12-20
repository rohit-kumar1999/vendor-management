from django.urls import path

from . import views

urlpatterns = [
    path('', views.VendorView.as_view(), name="vendors"),
    path('<slug:vendor_id>', views.VendorById.as_view(), name="vendor_by_id"),
    path('<slug:vendor_id>/performance', views.PerformanceView.as_view(), name="vendor_performance")
]