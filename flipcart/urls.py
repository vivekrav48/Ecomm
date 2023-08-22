from django.contrib import admin
from django.urls import path, include
# api url
from rest_framework import routers, serializers, viewsets
# import rest_framework
from .import views 
 
router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)


urlpatterns = [
    path("", views.index,name="home"),
    path("Home", views.index,name="home"),
    path("about", views.about,name="about"),
    path("contact", views.contact,name="contact"),
    path("signup", views.signup  ,name="signup"),
    path("login", views.login,name="login"),
    path("logout", views.logout,name="logout"),
    path("cart/",views.cart_details,name="cart"),
    path("checkout",views.checkout,name="checkout"),
    path("order",views.Order_dtls,name="order"),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')    
          )
 
]