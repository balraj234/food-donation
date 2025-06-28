from django.urls import path
from . import views
from .views import impact_view
from .views import contact_view, message_history_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('donate/', views.donate_view, name='donate'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('food-safety/', views.food_safety_view, name='food_safety'),
    path('impact/', impact_view, name='impact'),
    path('contact/', contact_view, name='contact'),
    path('messages/', message_history_view, name='message_history'),
    path('admin-panel/messages/', views.admin_messages_view, name='admin_messages'),
    path('admin-panel/messages/reply/<int:message_id>/', views.admin_reply_message, name='admin_reply'),
  
    
    path('donation/update/<int:donation_id>/', views.update_donation, name='update_donation'),
    path('donation/delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
]
