from django.urls import path
from . import views
urlpatterns = [
    path('',views.buyer_home,name="buyer"),
]
