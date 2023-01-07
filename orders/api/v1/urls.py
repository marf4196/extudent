from django.urls import path , include
from .views import  OrdersListApiView, UserCompletedOrders

urlpatterns = [
    path("user/orders/",OrdersListApiView.as_view({"get":"list","post":"create"}),name= "user-orders-list-create"),
    path("user/orders/<int:pk>/",OrdersListApiView.as_view({"get":"retrive","delete":"destroy"}),name= "user-orders-list-create"),
    path("user/complete_order_list", UserCompletedOrders.as_view({"get":"list"}, name= "complete_order_list")),
    path("user/complete_order/<int:pk>", UserCompletedOrders.as_view({"get":"retrive"}, name= "complete_order_")),
]
