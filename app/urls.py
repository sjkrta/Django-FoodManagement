from django.urls import path
from . import views

urlpatterns = [
    # Accounts
    # url path, control garne view, name for shortcut
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
    # Manager
    path('', views.dashboard_view, name='dashboard_view'),
    path('dashboard/profile/', views.dashboard_profile_view, name='dashboard_profile_view'),
    path('supplies/', views.supplies_view, name='supplies_view'),
    path('supplies/use/<int:id>/', views.supplies_use_view, name='supplies_use_view'),
    path('chefs/', views.chefs_view, name='chefs_view'),
    path('chefs/<int:id>/', views.chefs_detail_view, name='chefs_detail_view'),
    path('notifications/', views.notifications_view, name='notifications_view'),
    path('history/', views.history_view, name='history_view'),
    path('inventory/', views.inventory_view, name='inventory_view'),
]