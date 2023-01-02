from django.urls import path , include
from .views import OrdersDeleteGenericApiView, OrdersListGenericApiView

urlpatterns = [
    path("user/orders",OrdersListGenericApiView.as_view(),name= "user-orders-list-create"),
    path("user/orders/<int:pk>",OrdersDeleteGenericApiView.as_view(),name= "user-orders-delete"),
    
]
