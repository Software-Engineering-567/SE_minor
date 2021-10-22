from django.urls import path

from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('search/', views.search, name='search'),
    path('sort/', views.sort, name='sort'),
    path('filter/', views.bar_filter, name='filter'),
    path('<int:bar_id>/', views.details, name='detail'),
]
