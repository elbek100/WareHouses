from django.urls import path

from warehouses.views import ProductMaterialsAPIView

urlpatterns = [
    path('warehouse/', ProductMaterialsAPIView.as_view(), name='warehouse')
]