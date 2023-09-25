from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('message', views.MessageViewSet, basename='message')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login', views.login),
    path('register', views.register),

]