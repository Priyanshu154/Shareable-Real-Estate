from django.urls import path
from . import views
urlpatterns = [
    path('',views.buyer_home,name="buyer"),
    path('buy/<int:id>',views.buy,name="buy"),
]
