from django.urls import path
from . import views
urlpatterns = [
    path('',views.buyer_home,name="buyer"),
    # path('buy/<int:id>',views.buy,name="buy"),
    # path('buy_success/<int:prop_id>/<int:buy_shares>',views.buyed_share,name="buy_success"),
    path('payment_success/<int:buyer_id>',views.payment_success, name = 'payment_success'),
    path('payment_failure/<str:msg>',views.payment_failure, name = 'payment_failure'),
    path('buy_share/<int:prop_id>', views.buy_share, name="buy_share"),
]
