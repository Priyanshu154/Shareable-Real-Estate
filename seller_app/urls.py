from django.urls import path
from . import views
urlpatterns = [
    path('',views.seller_home,name="seller"),
    path('sell',views.sell_form,name="sell_form"),
    path('approve/<int:id>',views.approve_property,name="sell_form"),
]
