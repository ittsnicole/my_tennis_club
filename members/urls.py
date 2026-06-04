from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='members'),
    path('about/', views.about, name='about'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('details/<int:id>/', views.details, name='details'),
    path('list/', views.members_list, name='members_list'),
    path('stats/', views.stats, name='stats'),
    path('courts/', views.courts, name='courts'),
    path('schedule/', views.schedule, name='schedule'),
    path('membership/', views.membership, name='membership'),
    path('announcements/', views.announcements, name='announcements'),
    path('register/', views.register, name='register'),
    path('payments/', views.payments, name='payments'),
    path('payments/add/', views.add_payment, name='add_payment'),
]

