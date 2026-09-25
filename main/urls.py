from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('home-page/', views.home_page_html, name='home_page_html'),
    path('explore/', views.explore_page, name='explore_page'),
    path('travel-plan/', views.travel_plan, name='travel_plan'),
    path('transport-booking/', views.transport_booking, name='transport_booking'),
    path('events/', views.events_page, name='events_page'),
    path('emergency/', views.emergency_page, name='emergency_page'),
    path('guest-home/', views.guest_home, name='guest_home'),
    path('logout/', views.logout_view, name='logout'),
]
