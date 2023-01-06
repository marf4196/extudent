from django.urls import path , include
from .views import  OrdersListApiView

urlpatterns = [
    path("user/orders/",OrdersListApiView.as_view({"get":"list","post":"create"}),name= "user-orders-list-create"),
    path("user/orders/<int:pk>/",OrdersListApiView.as_view({"get":"retrive","delete":"destroy"}),name= "user-orders-list-create"),
    
    # path("user/orders/<int:pk>",OrdersDeleteGenericApiView.as_view(),name= "user-orders-delete"),
]
