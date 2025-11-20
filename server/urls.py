from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register),
    path('login/', views.login),
    path('payment/create-checkout/', views.create_checkout_session),
    path('webhook/stripe/', views.stripe_webhook),
    path('users/', views.list_users),
]
