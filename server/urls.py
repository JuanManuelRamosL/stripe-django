from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),

    path('payment/create-checkout/', views.create_checkout_session, name="create-checkout"),
    path('webhook/stripe/', views.stripe_webhook, name="stripe-webhook"),
    path('users/', views.list_users, name="get_all_users"),
    path('anda/', views.anda, name="anda"),
]