from django.urls import path
from . import views
urlpatterns = [
    path('',views.buyer_home,name="buyer"),
    path('buy/<int:id>',views.buy,name="buy_share"),
    path('buy_success/<int:prop_id>/<int:buy_shares>',views.buyed_share,name="buy_success"),
    path('payment_success/<int:buyer_id>',views.payment_success, name = 'payment_success'),
    path('payment_failure/<int:prop_id>/<int:buy_shares>/<order_id>',views.payment_failure, name = 'payment_failure'),
]
